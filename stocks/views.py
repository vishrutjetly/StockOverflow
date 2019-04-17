from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from stocks.models import Stock
from graphs import create
from stocks.models import Stock,Wishlist
from .forms import SearchStock, SearchStockCompare
import requests

from decouple import config
from .forms import SearchStock, SearchStockCompare

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

# FOR REPRODUCIBILITY
def mainfunc_view(tick):
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
	return close_val

def stock_view(request,pk):
	# get_stock_data()
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
		# url = get_url(ticker)


		# data = np.random.normal(1, 0.001, 100).tolist()
		data = mainfunc_view(ticker)
		# data = 0
		val = []
		val.append(data)
		data_label = [stock.name]
		xlabel = "Time"
		ylabel = "Stock Price"
		div_id = "mygraph1"

		view = create.data_plot(div_id, 'linechart', val, data_label, xlabel, ylabel)
		return render(request, 'stockview.html',{'stockview':view, 'pk':pk, 'form': form, 'stock_name': stock_name, 'stock': stock.name})

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
			
			# print(url)

			data = np.random.normal(1, 0.001, 1000).tolist()
			val = []
			val.append(data)
			data_label = [stock.name]
			xlabel = "Time"
			ylabel = "Stock Price"
			div_id = "mygraph1"

			view = create.data_plot(div_id, 'linechart', val, data_label, xlabel, ylabel)
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
	stock_name = []
	for item in stock_all:
		stock_name.append(str(item))
	if request.method == "POST":
		form = SearchStock(request.POST)
		if form.is_valid():
			stockname = form.cleaned_data['stock_name']
			if stockname not in stock_name:
				not_found = stockname
				return render(request, 'search_stock_notfound.html', {'form': form, 'stock_name': stock_name, 'not_found': not_found })
			else:
				stock = Stock.objects.filter(name = stockname)
				# print(stock[0].pk)
				return redirect('/stock-view/'+ str(stock[0].pk))
	else:
		form = SearchStock()
		print(form)
	return render(request, 'search_stock.html', {'form': form, 'stock_name': stock_name	})

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

			data1 = np.random.normal(1, 0.001, 100).tolist()
			data2 = np.random.normal(1, 0.001, 100).tolist()

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