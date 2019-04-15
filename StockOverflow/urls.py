
"""StockOverflow URL Configuration
The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.views.generic.base import TemplateView
from UserRegistration import views as user_views
from stocks import views as stockview

urlpatterns = [
	url(r'^$', TemplateView.as_view(template_name='homepage.html'), name='home'),
    url(r'^admin/', admin.site.urls),
    url(r'^login/$', auth_views.LoginView.as_view(template_name='login.html', redirect_authenticated_user=True), name='login'),
    url(r'^login/reset/$', auth_views.LoginView.as_view(template_name='login_static.html', redirect_authenticated_user=True), name='login_static'),
    url(r'^logout/$', auth_views.LogoutView.as_view(), name='logout'),
    url(r'^signup/$', user_views.signup, name ='signup' ),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',user_views.activate, name='activate'),
    url(r'^passchange/$', user_views.change_password, name='change_password'),
    url(r'^auth/', include('social_django.urls', namespace='social')),
    url(r'session_security/', include('session_security.urls')),
    url(r'^password_reset/$', auth_views.password_reset, {'template_name': 'login_static.html', 'email_template_name':'password_reset_email.html'}, name='password_reset'),
    url(r'^password_reset/done/$', auth_views.password_reset_done, {'template_name':'password_reset_done.html'}, name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', auth_views.password_reset_confirm, {'template_name':'password_reset_confirm.html'}, name='password_reset_confirm'),
    url(r'^reset/done/$', auth_views.password_reset_complete, {'template_name':'password_reset_complete.html'}, name='password_reset_complete'),
    url(r'^trial/',TemplateView.as_view(template_name='change_password_new.html'), name='trial'),
    url(r'^trial1/',TemplateView.as_view(template_name='trial1.html'), name='trial1'),
    url(r'^blogs/',TemplateView.as_view(template_name='blogs.html'), name='blogs'),
    url(r'^compare/',TemplateView.as_view(template_name='compare.html'), name='compare'),
    url(r'^stock-view/(?P<pk>\d+)/$',stockview.stock_view,name='stockview'),
    url(r'^stock-view/$',TemplateView.as_view(template_name='compare.html'), name='default-stockview'),
    url(r'^stock-view/(?P<pk>\d+)/$',stockview.stock_view,name='stockview'),
    url(r'^stock-predict/(?P<pk>\d+)/$',stockview.stock_predict,name='stockpredict'),
    url(r'^logapi/', include('eventlog.api.urls', namespace="api-log")),
    url(r'^profile/$', user_views.user_profile, name ='userprofile' ),
    url(r'^portfolio/',include('portfolio.urls')),
]
