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

def stock_view(request,pk):
	stock = get_object_or_404(Stock, pk = pk)
	ticker = stock.ticker
	url = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol='+ticker+'&apikey=WURUTBFP9P5F15BQ&datatype=csv'
	print(url)
	print(URL_BASIC)

	data = np.random.normal(1, 0.001, 100).tolist()
	val = []
	val.append(data)
	data_label = [stock.name]
	xlabel = "Time"
	ylabel = "Stock Price"
	div_id = "mygraph1"

	view = create.data_plot(div_id, 'linechart', val, data_label, xlabel, ylabel)
	return render(request, 'stockview.html',{'stockview':view, 'pk':pk})

def stock_predict(request,pk):
	if request.user.is_authenticated():
		stock = get_object_or_404(Stock, pk = pk)
		ticker = stock.ticker
		url = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol='+ticker+'&apikey=WURUTBFP9P5F15BQ&datatype=csv'
		print(url)

		data = np.random.normal(1, 0.001, 1000).tolist()
		val = []
		val.append(data)
		data_label = [stock.name]
		xlabel = "Time"
		ylabel = "Stock Price"
		div_id = "mygraph1"

		view = create.data_plot(div_id, 'linechart', val, data_label, xlabel, ylabel)
		return render(request, 'predict.html',{'stockview':view})

	else:
		return redirect('/login/?next=/stock-predict/'+str(pk)+'/')

def add_wishlist(request):
	if request.user.is_authenticated():
		if request.method == 'POST':
			print("\n\n\n\n\nOKAY!!\n\n\n\n")
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
				print(stockname)
				not_found = stockname
				return render(request, 'search_stock_notfound.html', {'form': form, 'stock_name': stock_name, 'not_found': not_found })
			else:
				stock = Stock.objects.filter(name = stockname)
				# print(stock[0].pk)
				return redirect('/stock-view/'+ str(stock[0].pk))
	else:
		form = SearchStock()
		print("Norm")
	return render(request, 'search_stock.html', {'form': form, 'stock_name': stock_name	})
