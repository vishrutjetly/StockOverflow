from django.contrib.auth import login, authenticate, update_session_auth_hash
from django.shortcuts import render, redirect
from .forms import SignUpForm
from django.http import HttpResponse
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from decouple import config
import requests
from stocks.models import Stock

URL_BASIC = config('URL_BASIC')

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.is_active = False
            # user.save()
            user.refresh_from_db()  # load the profile instance created by the signal
            username = form.cleaned_data.get('username')
            user.first_name = form.cleaned_data.get('first_name')
            user.last_name = form.cleaned_data.get('last_name')
            user.email = form.cleaned_data.get('email')
            user.save()
            # raw_password = form.cleaned_data.get('password1')
            # user = authenticate(username=username, password=raw_password)
            # login(request, user)
            # return redirect('home')

            current_site = get_current_site(request)
            mail_subject = 'Activate your StockOverflow account.'
            message = render_to_string('activate_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(mail_subject, message, to=[to_email])
            email.send()
            return render(request, 'email_sent.html')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

def activate(request, uidb64, token, backend='django.contrib.auth.backends.ModelBackend'):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user,backend='django.contrib.auth.backends.ModelBackend')
        # return redirect('home')
        # return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
        return render(request, 'email_confirm.html')
    else:
        return HttpResponse('Activation link is invalid!')

def change_password(request):
	if request.user.is_authenticated():
	    if request.method == 'POST':
	        form = PasswordChangeForm(request.user, request.POST)
	        if form.is_valid():
	            user = form.save()
	            update_session_auth_hash(request, user) 
	            messages.success(request, 'Your password was successfully updated!')
	            return redirect('home')
	        else:
	            messages.error(request, 'Please correct the error below.')
	    else:
	        form = PasswordChangeForm(request.user)
	    return render(request, 'change_password_new.html', {
	        'form': form
	    })
	else:
		return redirect('/login/?next=/passchange/')

def user_profile(request):
	if request.user.is_authenticated():
		data_mostviewed = requests.get(URL_BASIC + 'logapi/user/{!s}/event/stock/view/?limit=5&agg_type=terms&agg_field=stock-id'.format(request.user.id)).json()

		stocks=[]
		status = 'found'
		if 'status code' in list(data_mostviewed.keys()) and data_mostviewed['status code'] == 200:
			stocks_keys = []
			for item in data_mostviewed['result']:
				stocks_keys.append(item['key'])
			if len(stocks_keys) == 0:
				status = 'not found'
			else:
				for key in stocks_keys:
					try:
						stock_name = Stock.objects.filter(id=key).first().name
						stocks.append({'stock_id':key,'stock_name':stock_name})
					except:
						continue
		else:
			status = 'not found'

		print("\n\n\n\n",stocks,"\n\n\n\n")
		stocks_recent=[]
		recently_viewed = []

		recently_viewed = requests.get(URL_BASIC + 'logapi/user/{!s}/event/stock/view/?after=1970-1-1T0:0:0&limit=1000'.format(request.user.id)).json()

		status2 = 'found'
		if 'status code' in list(recently_viewed.keys()) and recently_viewed['status code'] == 200:
			stocks_keys = []
			for item in recently_viewed['result']:
				stocks_keys.append(item['event']['stock-id'])
			if len(stocks_keys) == 0:
				status2 = 'not found'
			else:
				used = set()
				stocks_keys = [x for x in stocks_keys  if x not in used and (used.add(x) or True)]
				if len(stocks_keys)>5:
					stocks_keys=stocks_keys[:5]
				print(stocks_keys)
				for key in stocks_keys:
					try:
						stock_name = Stock.objects.filter(id=key).first().name
						stocks_recent.append({'stock_id':key,'stock_name':stock_name})
					except:
						continue
		else:
			status2 = 'not found'

		stocks_trending=[]

		trending = requests.get(URL_BASIC + 'logapi/event/stock/view/?after=1970-1-1T0:0:0&limit=10').json()

		status3 = 'found'
		if 'status code' in list(trending.keys()) and trending['status code'] == 200:
			stocks_keys = []
			for item in trending['result']:
				stocks_keys.append(item['event']['stock-id'])
			if len(stocks_keys) == 0:
				status3 = 'not found'
			else:
				used = set()
				stocks_keys = [x for x in stocks_keys  if x not in used and (used.add(x) or True)]
				if len(stocks_keys)>5:
					stocks_keys=stocks_keys[:5]
				print(stocks_keys)
				for key in stocks_keys:
					try:
						stock_name = Stock.objects.filter(id=key).first().name
						stocks_trending.append({'stock_id':key,'stock_name':stock_name})
					except:
						continue
		else:
			status3 = 'not found'


		return render(request, 'profile.html',{'stocks':stocks, 'stocks_recent': stocks_recent, 'status2':status2, 'status3': status3, 'stocks_trending': stocks_trending})

	else:
		return redirect('/login/?next=/profile/')

def del_user_direct(request):
	if request.user.is_authenticated():
		return render(request, 'deluser.html')
	else:
		return redirect('home')

def del_user(request):
	if request.user.is_authenticated():
		user = request.user
		print(user)
		user.delete()
		return render(request, 'delsucc.html')
	else:
		return redirect('home')
