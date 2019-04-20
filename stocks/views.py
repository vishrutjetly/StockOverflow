from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from stocks.models import Stock
from graphs import create
from stocks.models import Stock,Wishlist
from .forms import SearchStock, SearchStockCompare
import requests
import os
from decouple import config
import json
from .forms import SearchStock, SearchStockCompare
from datetime import datetime, timezone
import collections

URL_BASIC = config('URL_BASIC')

def get_url(ticker):
	url = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol='+ticker+'&apikey=WURUTBFP9P5F15BQ&datatype=csv'
	return url


def new_dataset(dataset, step_size):
    data_X, data_Y = [], []
    for i in range(len(dataset)-step_size-1):
        a = dataset[i:(i+step_size), 0]
        data_X.append(a)
        data_Y.append(dataset[i + step_size, 0])
    return np.array(data_X), np.array(data_Y)

# IMPORTING LIBRARIES
import datetime
import pandas as pd
import numpy as np 
import math
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error
from keras.models import Sequential
from keras.layers import Dense, Activation
from keras.layers import LSTM
from keras import backend as K
import tensorflow as tf


# FOR REPRODUCIBILITY
def mainfunc_view(tick):
	K.clear_session()
	np.random.seed(7)

	ticker=tick

	# IMPORTING DATASET 
	dataset=pd.read_csv('https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol='+ticker+'&apikey=WURUTBFP9P5F15BQ&datatype=csv',usecols=[1,2,3,4])
	dataset = dataset.reindex(index = dataset.index[::-1])

	# CREATING OWN INDEX FOR FLEXIBILITY
	obs = np.arange(1, len(dataset) + 1, 1)

	# TAKING DIFFERENT INDICATORS FOR PREDICTION
	OHLC_avg = dataset.mean(axis = 1)
	HLC_avg = dataset[['high', 'low', 'close']].mean(axis = 1)
	close_val = dataset[['close']]
	return close_val.values.tolist()


def stock_view(request,pk):
	# get_stock_data()
	stock_all = Stock.objects.all()
	stock_name_actual = []
	for item in stock_all:
		stock_name_actual	.append(str(item))
	if request.method == "POST":
		form = SearchStock(request.POST)
		if form.is_valid():
			stockname = form.cleaned_data['stock_name']
			if stockname not in stock_name_actual:
				not_found = stockname
				if request.user.is_authenticated():
					color = ['#95b7ed', '#ffe2a0', '#ffbfe6']
					data_mostviewed = requests.get(URL_BASIC + 'logapi/user/{!s}/event/stock/view/?limit=3&agg_type=terms&agg_field=stock-id'.format(request.user.id)).json()

					stocks=[]
					status = 'found'
					if 'status code' in list(data_mostviewed.keys()) and data_mostviewed['status code'] == 200:
						stocks_keys = []
						for item in data_mostviewed['result']:
							stocks_keys.append(item['key'])
						if len(stocks_keys) == 0:
							status = 'not found'
						else:
							i = 0
							for key in stocks_keys:
								try:
									stock_name = Stock.objects.filter(id=key).first().name
									stocks.append({'stock_id':key,'stock_name':stock_name, 'stock_color': color[i]})
									i = i + 1
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
							# counts = collections.Counter(stocks_keys)
							# stocks_keys = sorted(stocks_keys, key=lambda x: counts[x])
							used = set()
							stocks_keys = [x for x in stocks_keys  if x not in used and (used.add(x) or True)]
							if len(stocks_keys)>5:
								stocks_keys=stocks_keys[:5]
							print(stocks_keys)
							i = 0
							for key in stocks_keys:
								try:
									stock_name = Stock.objects.filter(id=key).first().name
									stocks_recent.append({'stock_id':key,'stock_name':stock_name, 'stock_color': color[i]})
									i=i+1
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
							counts = collections.Counter(stocks_keys)
							stocks_keys = sorted(stocks_keys, key=lambda x: counts[x])
							used = set()
							stocks_keys = [x for x in stocks_keys  if x not in used and (used.add(x) or True)]
							if len(stocks_keys)>5:
								stocks_keys=stocks_keys[:5]
							print(stocks_keys)
							i = 0
							for key in stocks_keys:
								try:
									stock_name = Stock.objects.filter(id=key).first().name
									stocks_trending.append({'stock_id':key,'stock_name':stock_name,'stock_color': color[i]})
									i = i +1
								except:
									continue
					else:
						status3 = 'not found'

					return render(request, 'search_stock_notfound.html',{'form': form, 'stock_name': stock_name_actual, 'stocks':stocks, 'stocks_recent': stocks_recent, 'status2':status2, 'status3': status3, 'stocks_trending': stocks_trending, 'not_found': not_found})
				else:
					return render(request, 'search_stock_notfound.html',{'form': form, 'stock_name': stock_name_actual, 'not_found': not_found})

			else:
				stock = Stock.objects.filter(name = stockname)
				# print(stock[0].pk)
				return redirect('/stock-view/'+ str(stock[0].pk))
	else:
		form = SearchStock()
		stock = get_object_or_404(Stock, pk = pk)
		ticker = stock.ticker
		# url = get_url(ticker)


		# data = np.random.normal(1, 0.001, 100).tolist()

		# if not data_stock:
		# 	data = mainfunc_view(ticker)
		# 	data_stock = data
		# else:
		# 	pass

		if not stock.meta:
			stock.meta = mainfunc_view(stock.ticker)
			stock.save()
			data = stock.meta
			print("Saved")
		elif (datetime.datetime.now(timezone.utc)-stock.updated_at).days != 0:
			stock.meta = mainfunc_view(stock.ticker)
			stock.save()
			data = stock.meta
			print("Updated Stock prices")
		else:
			data = []
			print("Exists")
			for item in stock.meta:
				data.append(json.loads(item))

		# num = request.session.get('num')
		# if not num:
		# 	num = 1
		# 	print("Set num to 1")
		# 	request.session['num'] = num
		# else:
		# 	print("Exists")

		# print(num)

		# data = 0

		d = datetime.datetime.today()
		TRAINDATES=[]
		TESTDATES=[]
		TRAINDATES.append(d.strftime('%Y-%m-%d'))
		# print(TRAINDATES)
		for j in range(100):
		    d -= datetime.timedelta(days=1)
		    TRAINDATES.append(d.strftime('%Y-%m-%d'))
		TRAINDATES.reverse()

		val = []
		val.append(TRAINDATES)
		val.append(data)
		price = data[-1][0]
		prev_price = data[-2][0]
		print(price, prev_price)
		abs_change = price - prev_price
		if prev_price != 0:
			cent_change = abs_change/prev_price*100
		else:
			cent_change = 0
					

		if abs_change<0:
			col = 'red'
		else:
			col = 'green'

		data_label = ['x', stock.name]
		xlabel = "Time"
		ylabel = "Stock Price"
		div_id = "mygraph1"

		view = create.data_plot(div_id, 'linechart', val, data_label, xlabel, ylabel)

		stockurl = "https://www.nasdaq.com/symbol/" + stock.ticker
		if round(abs_change,2) == 0:
			abs_change = round(abs_change,3)
		else:
			abs_change = round(abs_change,2)
		
		if round(abs_change,2) == 0:
			cent_change = round(cent_change,3)
		else:
			cent_change = round(cent_change,2)
		abs(cent_change)

		return render(request, 'stockview.html',{'stockview':view, 'pk':pk, 'form': form, 'stock_name': stock_name_actual, 'stock': stock.name, 'price': price, 'abs_change': abs_change, 'cent_change': cent_change, 'col': col, 'url': stockurl, 'showon': '1' })

def stock_predict(request,pk):
	if request.user.is_authenticated():
		stock_all = Stock.objects.all()
		stock_name = []
		for item in stock_all:
			stock_name.append(str(item))
		if request.method == "POST":
			form = SearchStock(request.POST)
			if form.is_valid():
				stockname = form.cleaned_data['stock_name']
				if stockname not in stock_name:
					# print(stockname)
					not_found = stockname
					return render(request, 'search_stock_notfound2.html', {'form': form, 'stock_name': stock_name, 'not_found': not_found })
				else:
					stock = Stock.objects.filter(name = stockname)
					# print(stock[0].pk)
					return redirect('/stock-view/'+ str(stock[0].pk))
		else:
			form = SearchStock()
			stock = get_object_or_404(Stock, pk = pk)
			ticker = stock.ticker
			url = get_url(ticker)

			if not stock.meta_predict or (datetime.datetime.now(timezone.utc)-stock.updated_at).days != 0:
				K.clear_session()
				np.random.seed(7)

				# IMPORTING DATASET 
				dataset=pd.read_csv('https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol='+ticker+'&apikey=WURUTBFP9P5F15BQ&datatype=csv',usecols=[1,2,3,4])
				dataset = dataset.reindex(index = dataset.index[::-1])

				# CREATING OWN INDEX FOR FLEXIBILITY
				obs = np.arange(1, len(dataset) + 1, 1)

				# TAKING DIFFERENT INDICATORS FOR PREDICTION
				OHLC_avg = dataset.mean(axis = 1)
				HLC_avg = dataset[['high', 'low', 'close']].mean(axis = 1)
				close_val = dataset[['close']]
				print(close_val)

				# # PLOTTING ALL INDICATORS IN ONE PLOT
				# plt.plot(obs, OHLC_avg, 'r', label = 'OHLC avg')
				# plt.plot(obs, HLC_avg, 'b', label = 'HLC avg')
				# plt.plot(obs, close_val, 'g', label = 'Closing price')
				# plt.legend(loc = 'upper right')
				# plt.show()

				# PREPARATION OF TIME SERIES DATASE
				OHLC_avg = np.reshape(OHLC_avg.values, (len(OHLC_avg),1)) # 1664
				scaler = MinMaxScaler(feature_range=(0, 1))
				OHLC_avg = scaler.fit_transform(OHLC_avg)

				# TRAIN-TEST SPLIT
				train_OHLC = int(len(OHLC_avg) * 0.75)
				test_OHLC = len(OHLC_avg) - train_OHLC
				train_OHLC, test_OHLC = OHLC_avg[0:train_OHLC,:], OHLC_avg[train_OHLC:len(OHLC_avg),:]

				# TIME-SERIES DATASET (FOR TIME T, VALUES FOR TIME T+1)
				trainX, trainY = new_dataset(train_OHLC, 1)
				testX, testY = new_dataset(test_OHLC, 1)

				# RESHAPING TRAIN AND TEST DATA
				trainX = np.reshape(trainX, (trainX.shape[0], 1, trainX.shape[1]))
				testX = np.reshape(testX, (testX.shape[0], 1, testX.shape[1]))
				step_size = 1

				# LSTM MODEL
				model = Sequential()
				model.add(LSTM(32, input_shape=(1, step_size), return_sequences = True))
				model.add(LSTM(16))
				model.add(Dense(1))
				model.add(Activation('linear'))

				# K.clear_session()
				# MODEL COMPILING AND TRAINING
				model.compile(loss='mean_squared_error', optimizer='adagrad') # Try SGD, adam, adagrad and compare!!!
				model.fit(trainX, trainY, epochs=5, batch_size=1, verbose=2)
				print("Model fit done")

				# PREDICTION
				trainPredict = model.predict(trainX)
				testPredict = model.predict(testX)

				# DE-NORMALIZING FOR PLOTTING
				trainPredict = scaler.inverse_transform(trainPredict)
				trainY = scaler.inverse_transform([trainY])
				testPredict = scaler.inverse_transform(testPredict)
				testY = scaler.inverse_transform([testY])

				# TRAINING RMSE
				trainScore = math.sqrt(mean_squared_error(trainY[0], trainPredict[:,0]))
				print('Train RMSE: %.2f' % (trainScore))

				# TEST RMSE
				testScore = math.sqrt(mean_squared_error(testY[0], testPredict[:,0]))
				print('Test RMSE: %.2f' % (testScore))

				# CREATING SIMILAR DATASET TO PLOT TRAINING PREDICTIONS
				trainPredictPlot = np.empty_like(OHLC_avg)
				trainPredictPlot[:, :] = np.nan
				trainPredictPlot[step_size:len(trainPredict)+step_size, :] = trainPredict

				# CREATING SIMILAR DATASSET TO PLOT TEST PREDICTIONS
				testPredictPlot = np.empty_like(OHLC_avg)
				testPredictPlot[:, :] = np.nan
				testPredictPlot[len(trainPredict)+(step_size*2)+1:len(OHLC_avg)-1, :] = testPredict

				# DE-NORMALIZING MAIN DATASET 
				OHLC_avg = scaler.inverse_transform(OHLC_avg)

				last_val = testPredict[-1]
				last_val_scaled = last_val/last_val
				next_val = model.predict(np.reshape(last_val_scaled, (1,1,1)))
				print ("Last Day Value:", np.asscalar(last_val))
				print ("Next Day Value:", np.asscalar(last_val+next_val))


				RETURN_Y1=trainPredictPlot[0:75]
				RETURN_Y2=testPredictPlot[75:100]
				RETURN_NEXTDAYSVALUE = next_val

				# print(RETURN_Y1)
				# print("\n\n\n")
				# print(RETURN_Y2)

				return_y1 = []
				return_y2 = []

				for item in RETURN_Y1:
					if np.isnan(item[0]):
						pass
					else:
						return_y1.append(round(item[0],3))
						return_y2.append(round(item[0],3))

				for item in RETURN_Y2:
					if np.isnan(item[0]):
						pass
					else:
						return_y1.append(round(item[0],3))
				
				print(return_y1)

				stock.meta_predict = return_y1
				stock.save()
				data = stock.meta_predict

				print("Saved")

			else:
				data = []
				print("Exists")
				for item in stock.meta_predict:
					data.append(json.loads(item))

			# import datetime
			d = datetime.datetime.today()
			TRAINDATES=[]
			TESTDATES=[]
			TRAINDATES.append(d.strftime('%Y-%m-%d'))
			# print(TRAINDATES)
			for j in range(74):
			    d -= datetime.timedelta(days=1)
			    TRAINDATES.append(d.strftime('%Y-%m-%d'))
			TRAINDATES.reverse()
			# print(TRAINDATES)
			d = datetime.datetime.today()
			for i in range(len(data)-75):
			    d += datetime.timedelta(1)
			    TRAINDATES.append(d.strftime('%Y-%m-%d'))
			print(len(TRAINDATES),len(data))



			X_1=TRAINDATES
			X_2=TESTDATES

			data1 = data
			data2 = data[:75]
			val = []
			val.append(TRAINDATES)
			val.append(data1)
			val.append(data2)
			data_label = ['x','Predicted', 'Actual']
			xlabel = "Time"
			ylabel = "Stock Price"
			div_id = "mygraph1"

			view = create.data_plot(div_id, 'linechart', val, data_label, xlabel, ylabel)
			print("\n\n\n\n",view,"\n\n\n\n")
			return render(request, 'predict.html',{'stockview':view, 'pk':pk, 'form': form, 'stock_name': stock_name, 'stock': stock.name})

	else:
		return redirect('/login/?next=/stock-predict/'+str(pk)+'/')

def add_wishlist(request):
	if request.user.is_authenticated():
		if request.method == 'POST':
			pass
			# print("\n\n\n\n\nOKAY!!\n\n\n\n")
			# status = request.POST['status']
			# pk = request.POST['stock-id']
			# stock = get_object_or_404(Stock, pk = pk)
			# # a1 = Wishlist(user = request.user)
			# # a1.save()
			# # a1.stock.add(stock)
			# # a1.save()
			# wishlist = Wishlist.objects.create(user = request.user, stock = stock)
			# return redirect('userprofile')
	else:
		return redirect('login')

def rem_wishlist(request):
	if request.user.is_authenticated():
		if request.method == "POST":
			status = request.POST['status']
			pk = request.POST['wishlist-id']
			wishlist = get_object_or_404(Wishlist, pk)
			wishlist.delete()
			return redirect('userprofile')
	else:
		return redirect('login')

def find_stock(request):
	stock_all = Stock.objects.all()
	stock_name_actual = []
	for item in stock_all:
		stock_name_actual.append(str(item))
	if request.method == "POST":
		form = SearchStock(request.POST)
		if form.is_valid():
			stockname = form.cleaned_data['stock_name']
			if stockname not in stock_name_actual:
				not_found = stockname
				if request.user.is_authenticated():
					color = ['#95b7ed', '#ffe2a0', '#ffbfe6']
					data_mostviewed = requests.get(URL_BASIC + 'logapi/user/{!s}/event/stock/view/?limit=3&agg_type=terms&agg_field=stock-id'.format(request.user.id)).json()

					stocks=[]
					status = 'found'
					if 'status code' in list(data_mostviewed.keys()) and data_mostviewed['status code'] == 200:
						stocks_keys = []
						for item in data_mostviewed['result']:
							stocks_keys.append(item['key'])
						if len(stocks_keys) == 0:
							status = 'not found'
						else:
							i = 0
							for key in stocks_keys:
								try:
									stock_name = Stock.objects.filter(id=key).first().name
									stocks.append({'stock_id':key,'stock_name':stock_name, 'stock_color':color[i]})
									i = i + 1
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
							if len(stocks_keys)>3:
								stocks_keys=stocks_keys[:3]
							print(stocks_keys)
							i = 0
							for key in stocks_keys:
								try:
									stock_name = Stock.objects.filter(id=key).first().name
									stocks_recent.append({'stock_id':key,'stock_name':stock_name, 'stock_color':color[i]})
									i = i + 1
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
							counts = collections.Counter(stocks_keys)
							stocks_keys = sorted(stocks_keys, key=lambda x: -counts[x])
							used = set()
							stocks_keys = [x for x in stocks_keys  if x not in used and (used.add(x) or True)]
							if len(stocks_keys)>3:
								stocks_keys=stocks_keys[:3]
							print(stocks_keys)
							i = 0
							for key in stocks_keys:
								try:
									stock_name = Stock.objects.filter(id=key).first().name
									stocks_trending.append({'stock_id':key,'stock_name':stock_name,'stock_color': color[i]})
									i = i +1
								except:
									continue
					else:
						status3 = 'not found'

					return render(request, 'search_stock_notfound.html',{'form': form, 'stock_name': stock_name_actual, 'stocks':stocks, 'stocks_recent': stocks_recent, 'status2':status2, 'status3': status3, 'stocks_trending': stocks_trending, 'not_found': not_found})
				else:
					return render(request, 'search_stock_notfound.html', {'form': form, 'stock_name': stock_name_actual, 'not_found': not_found })
			else:
				stock = Stock.objects.filter(name = stockname)
				# print(stock[0].pk)
				return redirect('/stock-view/'+ str(stock[0].pk))
	else:
		form = SearchStock()
		if request.user.is_authenticated():
			color = ['#95b7ed', '#ffe2a0', '#ffbfe6']
			data_mostviewed = requests.get(URL_BASIC + 'logapi/user/{!s}/event/stock/view/?limit=3&agg_type=terms&agg_field=stock-id'.format(request.user.id)).json()

			stocks=[]
			status = 'found'
			if 'status code' in list(data_mostviewed.keys()) and data_mostviewed['status code'] == 200:
				stocks_keys = []
				for item in data_mostviewed['result']:
					stocks_keys.append(item['key'])
				if len(stocks_keys) == 0:
					status = 'not found'
				else:
					i = 0 
					for key in stocks_keys:
						try:
							stock_name = Stock.objects.filter(id=key).first().name
							stocks.append({'stock_id':key,'stock_name':stock_name, 'stock_color': color[i]})
							i = i + 1
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
					# counts = collections.Counter(stocks_keys)
					# stocks_keys = sorted(stocks_keys, key=lambda x: counts[x])
					used = set()
					stocks_keys = [x for x in stocks_keys  if x not in used and (used.add(x) or True)]
					if len(stocks_keys)>3:
						stocks_keys=stocks_keys[:3]
					print(stocks_keys)
					i = 0
					for key in stocks_keys:
						try:
							stock_name = Stock.objects.filter(id=key).first().name
							stocks_recent.append({'stock_id':key,'stock_name':stock_name, 'stock_color': color[i]})
							i = i + 1
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
					counts = collections.Counter(stocks_keys)
					stocks_keys = sorted(stocks_keys, key=lambda x: -counts[x])
					used = set()
					stocks_keys = [x for x in stocks_keys  if x not in used and (used.add(x) or True)]
					if len(stocks_keys)>3:
						stocks_keys=stocks_keys[:3]
					print(stocks_keys)
					i = 0
					for key in stocks_keys:
						try:
							stock_name = Stock.objects.filter(id=key).first().name
							stocks_trending.append({'stock_id':key,'stock_name':stock_name,'stock_color': color[i]})
							i = i +1
						except:
							continue
			else:
				status3 = 'not found'

			return render(request, 'search_stock.html',{'form': form, 'stock_name': stock_name_actual, 'stocks':stocks, 'stocks_recent': stocks_recent, 'status2':status2, 'status3': status3, 'stocks_trending': stocks_trending})
		else:
			return render(request, 'search_stock.html', {'form': form, 'stock_name': stock_name_actual	})

def find_stock_compare(request):
	if request.user.is_authenticated():
		stock_all = Stock.objects.all()
		stock_name = []
		for item in stock_all:
			stock_name.append(str(item))
		if request.method == "POST":
			form = SearchStockCompare(request.POST)
			if form.is_valid():
				stockname1 = form.cleaned_data['stock_name1']
				stockname2 = form.cleaned_data['stock_name2']
				if stockname1 not in stock_name:
					not_found = stockname1
					error = "Stock of company "+not_found+" does not exist"
					return render(request, 'search_stock_notfound_compare.html', {'form': form, 'stock_name': stock_name, 'not_found': error })
				elif stockname2 not in stock_name:
					not_found = stockname2
					error = "Stock of company "+not_found+" does not exist"
					return render(request, 'search_stock_notfound_compare.html', {'form': form, 'stock_name': stock_name, 'not_found': error })
				elif stockname1 == stockname2:
					error = "Stocks of same company are selected"
					return render(request, 'search_stock_notfound_compare.html', {'form': form, 'stock_name': stock_name, 'not_found': error })

				else:
					stock1 = Stock.objects.filter(name = stockname1)
					stock2 = Stock.objects.filter(name = stockname2)
					# print(stock[0].pk)
					return redirect('/stock-compare/'+ str(stock1[0].pk)+'/'+str(stock2[0].pk))
		else:
			form = SearchStockCompare()
		return render(request, 'search_stock_compare.html', {'form': form, 'stock_name': stock_name	})
	else:
		return redirect('/login/?next=/stock-compare/')

def stock_view_compare(request,pk1,pk2):
	# get_stock_data()
	if request.user.is_authenticated():
		stock_all = Stock.objects.all()
		stock_name = []
		for item in stock_all:
			stock_name.append(str(item))
		if request.method == "POST":
			form = SearchStockCompare(request.POST)
			if form.is_valid():
				stockname1 = form.cleaned_data['stock_name1']
				stockname2 = form.cleaned_data['stock_name2']
				if stockname1 not in stock_name:
					not_found = stockname1
					error = "Stock of company "+not_found+" does not exist"
					return render(request, 'search_stock_notfound_compare.html', {'form': form, 'stock_name': stock_name, 'not_found': error })
				elif stockname2 not in stock_name:
					not_found = stockname2
					error = "Stock of company "+not_found+" does not exist"
					return render(request, 'search_stock_notfound_compare.html', {'form': form, 'stock_name': stock_name, 'not_found': error })
				elif stockname1 == stockname2:
					error = "Stocks of same company are selected"
					return render(request, 'search_stock_notfound_compare.html', {'form': form, 'stock_name': stock_name, 'not_found': error })

				else:
					stock1 = Stock.objects.filter(name = stockname1)
					stock2 = Stock.objects.filter(name = stockname2)
					# print(stock[0].pk)
					return redirect('/stock-compare/'+ str(stock1[0].pk)+'/'+str(stock2[0].pk))
		else:
			form = SearchStockCompare()
			stock1 = get_object_or_404(Stock, pk = pk1)
			stock2 = get_object_or_404(Stock, pk = pk2)
			ticker1 = stock1.ticker
			ticker2 = stock2.ticker

			url = get_url(ticker1)

			# data1 = np.random.normal(1, 0.001, 100).tolist()
			# data2 = np.random.normal(1, 0.001, 100).tolist()

			data1 = mainfunc_view(ticker1)
			data2 = mainfunc_view(ticker2)

			# data = 0
			val = []
			val.append(data1)
			val.append(data2)
			data_label = [stock1.name, stock2.name]
			xlabel = "Time"
			ylabel = "Stock Price"
			div_id = "mygraph1"

			view = create.data_plot(div_id, 'linechart', val, data_label, xlabel, ylabel)
			return render(request, 'search_stock_with_graph_compare.html',{'stockview':view, 'pk':pk1, 'form': form, 'stock_name': stock_name, 'stock': stock1.name})

		return render(request, 'search_stock_compare.html', {'form': form, 'stock_name': stock_name	})
	else:
		return redirect('/login/?next=/stock-compare/')