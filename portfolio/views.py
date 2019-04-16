from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from . import forms
import csv
import pandas as pd
from datetime import date
import numpy as np

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
                comps=[]
                dates=[]
                quant=[]
                ansy=[]
                for row in csv_reader:
                    comps.append(row[0])
                    dates.append(row[1])
                    quant.append(float(row[2]))
                tickers=['AAPL','BANF','CASH','FCEL','JNJ']
                AAPL=pd.read_csv('https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=AAPL&apikey=WURUTBFP9P5F15BQ&datatype=csv')
                BANF=pd.read_csv('https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=BANF&apikey=WURUTBFP9P5F15BQ&datatype=csv')
                CASH=pd.read_csv('https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=CASH&apikey=WURUTBFP9P5F15BQ&datatype=csv')
                FCEL=pd.read_csv('https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=FCEL&apikey=WURUTBFP9P5F15BQ&datatype=csv')
                JNJ=pd.read_csv('https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=JNJ&apikey=WURUTBFP9P5F15BQ&datatype=csv')
                for i in range(0,len(comps)):
                    if comps[i]=="AAPL":
                        dates_parsed=dates[i].split("-")
                        d0=date(int(dates_parsed[0]),int(dates_parsed[1]),int(dates_parsed[2]))
                        ind=99
                        for j in range(0,100):
                            dtemp=AAPL.at[j,'timestamp']
                            dtemp_parsed=dtemp.split("-")
                            dtemp=date(int(dtemp_parsed[0]),int(dtemp_parsed[1]),int(dtemp_parsed[2]))
                            if dtemp<=d0:
                                ind=j
                                break
                        if i==0:
                            ansx=np.zeros(ind+1)
                            for l in range(0,ind+1):
                                ansy.append(AAPL.at[l,'timestamp'])
                        for l in range(0,ind+1):
                            ansx[l]=ansx[l]+(float(AAPL.at[l,'close'])*float(quant[i]))
                    elif comps[i]=="BANF":
                        dates_parsed=dates[i].split("-")
                        d0=date(int(dates_parsed[0]),int(dates_parsed[1]),int(dates_parsed[2]))
                        ind=99
                        for j in range(0,100):
                            dtemp=AAPL.at[j,'timestamp']
                            dtemp_parsed=dtemp.split("-")
                            dtemp=date(int(dtemp_parsed[0]),int(dtemp_parsed[1]),int(dtemp_parsed[2]))
                            if dtemp<=d0:
                                ind=j
                                break
                        if i==0:
                            ansx=np.zeros(ind+1)
                            for l in range(0,ind+1):
                                ansy.append(BANF.at[l,'timestamp'])
                        for l in range(0,ind+1):
                            ansx[l]=ansx[l]+(float(BANF.at[l,'close'])*float(quant[i]))
                    elif comps[i]=="CASH":
                        dates_parsed=dates[i].split("-")
                        d0=date(int(dates_parsed[0]),int(dates_parsed[1]),int(dates_parsed[2]))
                        ind=99
                        for j in range(0,100):
                            dtemp=CASH.at[j,'timestamp']
                            dtemp_parsed=dtemp.split("-")
                            dtemp=date(int(dtemp_parsed[0]),int(dtemp_parsed[1]),int(dtemp_parsed[2]))
                            if dtemp<=d0:
                                ind=j
                                break
                        if i==0:
                            ansx=np.zeros(ind+1)
                            for l in range(0,ind+1):
                                ansy.append(CASH.at[l,'timestamp'])
                        for l in range(0,ind+1):
                            ansx[l]=ansx[l]+(float(CASH.at[l,'close'])*float(quant[i]))
                    elif comps[i]=="FCEL":
                        dates_parsed=dates[i].split("-")
                        d0=date(int(dates_parsed[0]),int(dates_parsed[1]),int(dates_parsed[2]))
                        ind=99
                        for j in range(0,100):
                            dtemp=AAPL.at[j,'timestamp']
                            dtemp_parsed=dtemp.split("-")
                            dtemp=date(int(dtemp_parsed[0]),int(dtemp_parsed[1]),int(dtemp_parsed[2]))
                            if dtemp<=d0:
                                ind=j
                                break
                        if i==0:
                            ansx=np.zeros(ind+1)
                            for l in range(0,ind+1):
                                ansy.append(FCEL.at[l,'timestamp'])
                        for l in range(0,ind+1):
                            ansx[l]=ansx[l]+(float(FCEL.at[l,'close'])*float(quant[i]))
                    elif comps[i]=="JNJ":
                        dates_parsed=dates[i].split("-")
                        d0=date(int(dates_parsed[0]),int(dates_parsed[1]),int(dates_parsed[2]))
                        ind=99
                        for j in range(0,100):
                            dtemp=JNJ.at[j,'timestamp']
                            dtemp_parsed=dtemp.split("-")
                            dtemp=date(int(dtemp_parsed[0]),int(dtemp_parsed[1]),int(dtemp_parsed[2]))
                            if dtemp<=d0:
                                ind=j
                                break
                        if i==0:
                            ansx=np.zeros(ind+1)
                            for l in range(0,ind+1):
                                ansy.append(JNJ.at[l,'timestamp'])
                        for l in range(0,ind+1):
                            ansx[l]=ansx[l]+(float(JNJ.at[l,'close'])*float(quant[i]))
            print("ansy=")
            print(ansx)
            print(ansy)
            return render(request,'portfolio/csv_done.html', {'r1': ansx, 'r2':ansy})
    else:
        form = forms.csv_upload()
        return render(request, "portfolio/csv_upload.html", {'form': form})

@login_required(login_url='login')
def manually(request):
	if request.method=="POST":
		comps=[]
		dates=[]
		quant=[]
		ansy=[]
		comps.append(request.POST['company'])
		dates.append(request.POST['date'])
		quant.append(request.POST['quantity'])
		tickers=['AAPL','BANF','CASH','FCEL','JNJ']
		AAPL=pd.read_csv('https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=AAPL&apikey=WURUTBFP9P5F15BQ&datatype=csv')
		BANF=pd.read_csv('https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=BANF&apikey=WURUTBFP9P5F15BQ&datatype=csv')
		CASH=pd.read_csv('https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=CASH&apikey=WURUTBFP9P5F15BQ&datatype=csv')
		FCEL=pd.read_csv('https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=FCEL&apikey=WURUTBFP9P5F15BQ&datatype=csv')
		JNJ=pd.read_csv('https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=JNJ&apikey=WURUTBFP9P5F15BQ&datatype=csv')
		for i in range(0,len(comps)):
			if comps[i]=="AAPL":
				dates_parsed=dates[i].split("-")
				d0=date(int(dates_parsed[0]),int(dates_parsed[1]),int(dates_parsed[2]))
				ind=99
				for j in range(0,100):
					dtemp=AAPL.at[j,'timestamp']
					dtemp_parsed=dtemp.split("/")
					dtemp=date(int(dtemp_parsed[0]),int(dtemp_parsed[1]),int(dtemp_parsed[2]))
					if dtemp<=d0:
						ind=j
						break
				if i==0:
					ansx=np.zeros(ind+1)
					for l in range(0,ind+1):
						ansy.append(AAPL.at[l,'timestamp'])
				for l in range(0,ind+1):
					ansx[l]=ansx[l]+(float(AAPL.at[l,'close'])*float(quant[i]))
			elif comps[i]=="BANF":
				dates_parsed=dates[i].split("/")
				d0=date(int(dates_parsed[0]),int(dates_parsed[1]),int(dates_parsed[2]))
				ind=99
				for j in range(0,100):
					dtemp=AAPL.at[j,'timestamp']
					dtemp_parsed=dtemp.split("-")
					dtemp=date(int(dtemp_parsed[0]),int(dtemp_parsed[1]),int(dtemp_parsed[2]))
					if dtemp<=d0:
						ind=j
						break
				if i==0:
				    ansx=np.zeros(ind+1)
				    for l in range(0,ind+1):
					ansy.append(BANF.at[l,'timestamp'])
				for l in range(0,ind+1):
				    ansx[l]=ansx[l]+(float(BANF.at[l,'close'])*float(quant[i]))
		    elif comps[i]=="CASH":
			dates_parsed=dates[i].split("/")
			d0=date(int(dates_parsed[0]),int(dates_parsed[1]),int(dates_parsed[2]))
			ind=99
			for j in range(0,100):
			    dtemp=CASH.at[j,'timestamp']
			    dtemp_parsed=dtemp.split("-")
			    dtemp=date(int(dtemp_parsed[0]),int(dtemp_parsed[1]),int(dtemp_parsed[2]))
			    if dtemp<=d0:
				ind=j
				break
			if i==0:
			    ansx=np.zeros(ind+1)
			    for l in range(0,ind+1):
				ansy.append(CASH.at[l,'timestamp'])
			for l in range(0,ind+1):
			    ansx[l]=ansx[l]+(float(CASH.at[l,'close'])*float(quant[i]))
		    elif comps[i]=="FCEL":
			dates_parsed=dates[i].split("/")
			d0=date(int(dates_parsed[0]),int(dates_parsed[1]),int(dates_parsed[2]))
			ind=99
			for j in range(0,100):
			dtemp=AAPL.at[j,'timestamp']
			dtemp_parsed=dtemp.split("-")
			dtemp=date(int(dtemp_parsed[0]),int(dtemp_parsed[1]),int(dtemp_parsed[2]))
			if dtemp<=d0:
				ind=j
				break
			if i==0:
			    ansx=np.zeros(ind+1)
			    for l in range(0,ind+1):
				ansy.append(FCEL.at[l,'timestamp'])
			for l in range(0,ind+1):
			    ansx[l]=ansx[l]+(float(FCEL.at[l,'close'])*float(quant[i]))
		    elif comps[i]=="JNJ":
			dates_parsed=dates[i].split("/")
			d0=date(int(dates_parsed[0]),int(dates_parsed[1]),int(dates_parsed[2]))
			ind=99
			for j in range(0,100):
			    dtemp=JNJ.at[j,'timestamp']
			    dtemp_parsed=dtemp.split("-")
			    dtemp=date(int(dtemp_parsed[0]),int(dtemp_parsed[1]),int(dtemp_parsed[2]))
			    if dtemp<=d0:
				ind=j
				break
			if i==0:
			    ansx=np.zeros(ind+1)
			    for l in range(0,ind+1):
				ansy.append(JNJ.at[l,'timestamp'])
			for l in range(0,ind+1):
			    ansx[l]=ansx[l]+(float(JNJ.at[l,'close'])*float(quant[i]))
			print("ansy=")
			print(ansx)
			print(ansy)
			return render(request,'portfolio/csv_done.html', {'r1': ansx, 'r2':ansy})
	else:
		form = forms.csv_upload()
		return render(request, "add_portfolio.html")
