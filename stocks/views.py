from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from stocks.models import Stock
from graphs import create
from stocks.models import Stock,Wishlist

import pandas as pd
import numpy as np
import requests

# import matplotlib.pyplot as plt
# import matplotlib.dates as mdates
import os

from sklearn.metrics import mean_squared_error, r2_score
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import PolynomialFeatures

from sklearn import preprocessing;
# from sklearn import cross_validation;
from sklearn import linear_model;
from sklearn.linear_model import LinearRegression
# from sklearn import preprocessing, cross_validation, svm

from decouple import config
from .forms import SearchStock

URL_BASIC = config('URL_BASIC')

# Create your views here.

def get_url(ticker):
	url = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol='+ticker+'&apikey=WURUTBFP9P5F15BQ&datatype=csv'
	return url

def get_all_tickers():
	stock_all = Stock.objects.all()
	stock_ticker = []
	for item in stock_all:
		stock_ticker.append(item.ticker)
	return stock_ticker

def get_stock_data():
	data_stock = [] 
	i = 0
	tickers = get_all_tickers()
	for item in tickers:
		data_stock.append(pd.read_csv(get_url(item)))
	for item in tickers:
		data_stock[i]['ticker'] = [item]*len(data_stock[i])
		i = i + 1
	i = 0
	for item in tickers:
		if i == 0:
			df = data_stock[i]
		else:
			df = df.append(data_stock[i], sort = False)

	df=df.rename(columns={'timestamp':'date'})
	df['date'] = pd.to_datetime(df['date'])
	df["intdate"] = df['date'].dt.strftime("%Y%m%d")

	data=df
	n = data.shape[0]
	c = data.shape[1]

	flags=np.zeros(len(tickers))
	flags[0]=1
	flags[1]=1
	legnames=[]
	stock_price = []
	for i in range(len(tickers)):
	    if flags[i]==1:
	        legnames.append(tickers[i])
	        x=data[data['ticker']==tickers[i]]
	        # plt.plot(x['date'],x['close'])
	        stock_price.append(x['close'])
	print(len(stock_price))
	return stock_price

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
		url = get_url(ticker)

		data = np.random.normal(1, 0.001, 100).tolist()
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
	return render(request, 'search_stock.html', {'form': form, 'stock_name': stock_name	})
