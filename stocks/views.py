from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from stocks.models import Stock
from graphs import create

import pandas as pd
import numpy as np
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

# Create your views here.

def stock_view(request,pk):
	stock = get_object_or_404(Stock, pk = pk)
	ticker = stock.ticker
	url = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol='+ticker+'&apikey=WURUTBFP9P5F15BQ&datatype=csv'
	print(url)

	data = np.random.normal(1, 0.001, 100).tolist()
	val = []
	val.append(data)
	data_label = ['Stock Prices']
	xlabel = "Time"
	ylabel = "Stock Price"
	div_id = "mygraph1"

	view = create.data_plot(div_id, 'linechart', val, data_label, xlabel, ylabel)
	return render(request, 'compare.html',{'stockview':view})