from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from . import forms
import csv
#import pandas as pd

@login_required(login_url='login')
def portfolio(request):
    if request.method=="POST":
        form = forms.csv_upload(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            for filename in request.FILES:
                name = request.FILES[filename].name
            with open('portfolio/'+name) as csv_file:
                csv_reader=csv.reader(csv_file,delimiter=',')
                r1=[]
                r2=[]
                for row in csv_reader:
                    r1.append(float(row[0]))
                    r2.append(float(row[1]))
                print(r1)
                print(r2)
#                tickers=['AAPL','BANF','CASH','FCEL','JNJ']
#                AAPL=pd.read_csv('https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=AAPL&apikey=WURUTBFP9P5F15BQ&datatype=csv')
#                BANF=pd.read_csv('https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=BANF&apikey=WURUTBFP9P5F15BQ&datatype=csv')
#                CASH=pd.read_csv('https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=CASH&apikey=WURUTBFP9P5F15BQ&datatype=csv')
#                FCEL=pd.read_csv('https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=FCEL&apikey=WURUTBFP9P5F15BQ&datatype=csv')
#                JNJ=pd.read_csv('https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=JNJ&apikey=WURUTBFP9P5F15BQ&datatype=csv')
#                print(JNJ)
                return render(request,'portfolio/csv_done.html', {'r1': r1}, {'r2':r2})
    else:
        form = forms.csv_upload()
        return render(request, "portfolio/csv_upload.html", {'form': form})
