from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from . import forms
import csv
import pandas as pd
from datetime import date
import numpy as np
from .models import pf_inst
from .models import blogs
import os
from graphs import create

def find(name, path):
    print("finding")
    for root, dirs, files in os.walk(path):
        for f in files:
            if f==str(name):
            	return os.path.join(root,str(name))
    return "nulll"

@login_required(login_url='login')
def portfolio(request):
    if request.method=="POST":
        form = forms.csv_upload(request.POST, request.FILES)
        if form.is_valid():
            namee=(find(request.user, "portfolio/"))
            if namee!="nulll":
            	os.remove(namee)
            for filename in request.FILES:
            	request.FILES[filename].name=str(request.user)
            form=forms.csv_upload(request.POST, request.FILES)
            form.save()
            for filename in request.FILES:
                name = request.FILES[filename].name
            with open('portfolio/'+name) as csv_file:
                csv_reader=csv.reader(csv_file,delimiter=',')
                comps=[]
                dates=[]
                quant=[]
                ansy=[]
                try:
                    for row in csv_reader:
                        comps.append(row[0])
                        dates.append(row[1])
                        quant.append(float(row[2]))
                except:
                    return render(request,'invalid.html')
                tickers=['AAPL','BANF','CASH','FCEL','JNJ']
                AAPL=pd.read_csv('https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=AAPL&apikey=WURUTBFP9P5F15BQ&datatype=csv')
                BANF=pd.read_csv('https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=BANF&apikey=WURUTBFP9P5F15BQ&datatype=csv')
                CASH=pd.read_csv('https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=CASH&apikey=WURUTBFP9P5F15BQ&datatype=csv')
                FCEL=pd.read_csv('https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=FCEL&apikey=WURUTBFP9P5F15BQ&datatype=csv')
                JNJ=pd.read_csv('https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=JNJ&apikey=WURUTBFP9P5F15BQ&datatype=csv')
                for i in range(0,len(comps)):
                	dates_parsed=dates[i].split("-")
                	try:
                		d0=date(int(dates_parsed[0]),int(dates_parsed[1]),int(dates_parsed[2]))
                	except:
                		return render(request,'invalid.html')
                	if i==0:
                		maxd=d0-d0
                	dtemp=AAPL.at[0,'timestamp']
                	dtemp_parsed=dtemp.split("-")
                	dtemp=date(int(dtemp_parsed[0]),int(dtemp_parsed[1]),int(dtemp_parsed[2]))
                	if dtemp-d0>maxd:
                		maxd=dtemp-d0
                dtemp=AAPL.at[0,'timestamp']
                dtemp_parsed=dtemp.split("-")
                dtemp=date(int(dtemp_parsed[0]),int(dtemp_parsed[1]),int(dtemp_parsed[2]))
                d0=dtemp-maxd
                ind=99
                for j in range(0,100):
                    dtemp=AAPL.at[j,'timestamp']
                    dtemp_parsed=dtemp.split("-")
                    dtemp=date(int(dtemp_parsed[0]),int(dtemp_parsed[1]),int(dtemp_parsed[2]))
                    if dtemp<d0:
                        ind=j-1
                        break
                ansx=np.zeros(ind+1)
                for l in range(0,ind+1):
                    ansy.append(AAPL.at[l,'timestamp'])
                for i in range(0,len(comps)):
                    if comps[i]=="AAPL":
                        dates_parsed=dates[i].split("-")
                        try:
                        	d0=date(int(dates_parsed[0]),int(dates_parsed[1]),int(dates_parsed[2]))
                        except:
                        	return render(request,'invalid.html')
                        ind=99
                        for j in range(0,100):
                            dtemp=AAPL.at[j,'timestamp']
                            dtemp_parsed=dtemp.split("-")
                            dtemp=date(int(dtemp_parsed[0]),int(dtemp_parsed[1]),int(dtemp_parsed[2]))
                            if dtemp<d0:
                                ind=j-1
                                break
                        #if i==0:
                        #    ansx=np.zeros(ind+1)
                        #    for l in range(0,ind+1):
                        #        ansy.append(AAPL.at[l,'timestamp'])
                        try:
                        	if float(quant[i])<0:
                        		return render(request, 'invalid.html')
                        except:
                        	return render(request, 'invalid.html')
                        for l in range(0,ind+1):
                            ansx[l]=ansx[l]+(float(AAPL.at[l,'close'])*float(quant[i]))
                    elif comps[i]=="BANF":
                        dates_parsed=dates[i].split("-")
                        try:
                        	d0=date(int(dates_parsed[0]),int(dates_parsed[1]),int(dates_parsed[2]))
                        except:
                        	return render(request,'invalid.html')
                        ind=99
                        for j in range(0,100):
                            dtemp=AAPL.at[j,'timestamp']
                            dtemp_parsed=dtemp.split("-")
                            dtemp=date(int(dtemp_parsed[0]),int(dtemp_parsed[1]),int(dtemp_parsed[2]))
                            if dtemp<d0:
                                ind=j-1
                                break
                        #if i==0:
                        #    ansx=np.zeros(ind+1)
                        #    for l in range(0,ind+1):
                        #        ansy.append(BANF.at[l,'timestamp'])
                        try:
                        	if float(quant[i])<0:
                        		return render(request, 'invalid.html')
                        except:
                        	return render(request, 'invalid.html')
                        for l in range(0,ind+1):
                            ansx[l]=ansx[l]+(float(BANF.at[l,'close'])*float(quant[i]))
                    elif comps[i]=="CASH":
                        dates_parsed=dates[i].split("-")
                        try:
                        	d0=date(int(dates_parsed[0]),int(dates_parsed[1]),int(dates_parsed[2]))
                        except:
                        	return render(request,'invalid.html')
                        ind=99
                        for j in range(0,100):
                            dtemp=CASH.at[j,'timestamp']
                            dtemp_parsed=dtemp.split("-")
                            dtemp=date(int(dtemp_parsed[0]),int(dtemp_parsed[1]),int(dtemp_parsed[2]))
                            if dtemp<d0:
                                ind=j-1
                                break
                        #if i==0:
                        #    ansx=np.zeros(ind+1)
                        #    for l in range(0,ind+1):
                        #        ansy.append(CASH.at[l,'timestamp'])
                        try:
                        	if float(quant[i])<0:
                        		return render(request, 'invalid.html')
                        except:
                        	return render(request, 'invalid.html')
                        for l in range(0,ind+1):
                            ansx[l]=ansx[l]+(float(CASH.at[l,'close'])*float(quant[i]))
                    elif comps[i]=="FCEL":
                        dates_parsed=dates[i].split("-")
                        try:
                        	d0=date(int(dates_parsed[0]),int(dates_parsed[1]),int(dates_parsed[2]))
                        except:
                        	return render(request, 'invalid.html')
                        ind=99
                        for j in range(0,100):
                            dtemp=AAPL.at[j,'timestamp']
                            dtemp_parsed=dtemp.split("-")
                            dtemp=date(int(dtemp_parsed[0]),int(dtemp_parsed[1]),int(dtemp_parsed[2]))
                            if dtemp<d0:
                                ind=j-1
                                break
                        #if i==0:
                        #    ansx=np.zeros(ind+1)
                        #    for l in range(0,ind+1):
                        #        ansy.append(FCEL.at[l,'timestamp'])
                        try:
                        	if float(quant[i])<0:
                        		return render(request, 'invalid.html')
                        except:
                        	return render(request, 'invalid.html')
                        for l in range(0,ind+1):
                            ansx[l]=ansx[l]+(float(FCEL.at[l,'close'])*float(quant[i]))
                    elif comps[i]=="JNJ":
                        dates_parsed=dates[i].split("-")
                        try:
                        	d0=date(int(dates_parsed[0]),int(dates_parsed[1]),int(dates_parsed[2]))
                        except:
                        	return render(request,'invalid.html')
                        ind=99
                        for j in range(0,100):
                            dtemp=JNJ.at[j,'timestamp']
                            dtemp_parsed=dtemp.split("-")
                            dtemp=date(int(dtemp_parsed[0]),int(dtemp_parsed[1]),int(dtemp_parsed[2]))
                            if dtemp<d0:
                                ind=j-1
                                break
                        try:
                        	if float(quant[i])<0:
                        		return render(request, 'invalid.html')
                        except:
                        	return render(request, 'invalid.html')
                        #if i==0:
                        #    ansx=np.zeros(ind+1)
                        #    for l in range(0,ind+1):
                        #        ansy.append(JNJ.at[l,'timestamp'])
                        for l in range(0,ind+1):
                            ansx[l]=ansx[l]+(float(JNJ.at[l,'close'])*float(quant[i]))
            print("ansy=")
            print(ansx)
            print(ansy)
            form = forms.csv_upload()
            data = ansx.tolist()
            data.reverse()
            val = []
            val.append(data)
            data_label = ["Portfolio"]
            xlabel = "Time"
            ylabel = "Portfolio Value"
            div_id = "mygraph1"

            view = create.data_plot(div_id, 'linechart', val, data_label, xlabel, ylabel)
            return render(request,'csv_done.html', {'r1': ansx, 'r2':ansy, 'stockview':view, 'form':form})

#            return render(request,'csv_done.html', {'r1': ansx, 'r2':ansy, 'form':form})
        else:
            return render(request,'invalid.html')
    else:
        if find(request.user,"portfolio/")=="nulll":
        	form = forms.csv_upload()
        	return render(request, "csv_upload.html", {'form': form})
        else:
            name = request.user
            form = forms.csv_upload()
            with open('portfolio/'+str(name)) as csv_file:
                csv_reader=csv.reader(csv_file,delimiter=',')
                comps=[]
                dates=[]
                quant=[]
                ansy=[]
                try:
                    for row in csv_reader:
                        comps.append(row[0])
                        dates.append(row[1])
                        quant.append(float(row[2]))
                except:
                    return render(request,'invalid.html')
                tickers=['AAPL','BANF','CASH','FCEL','JNJ']
                AAPL=pd.read_csv('https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=AAPL&apikey=WURUTBFP9P5F15BQ&datatype=csv')
                BANF=pd.read_csv('https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=BANF&apikey=WURUTBFP9P5F15BQ&datatype=csv')
                CASH=pd.read_csv('https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=CASH&apikey=WURUTBFP9P5F15BQ&datatype=csv')
                FCEL=pd.read_csv('https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=FCEL&apikey=WURUTBFP9P5F15BQ&datatype=csv')
                JNJ=pd.read_csv('https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=JNJ&apikey=WURUTBFP9P5F15BQ&datatype=csv')
                for i in range(0,len(comps)):
                	dates_parsed=dates[i].split("-")
                	try:
                		d0=date(int(dates_parsed[0]),int(dates_parsed[1]),int(dates_parsed[2]))
                	except:
                		return render(request,'invalid.html')
                	if i==0:
                		maxd=d0-d0
                	dtemp=AAPL.at[0,'timestamp']
                	dtemp_parsed=dtemp.split("-")
                	dtemp=date(int(dtemp_parsed[0]),int(dtemp_parsed[1]),int(dtemp_parsed[2]))
                	if dtemp-d0>maxd:
                		maxd=dtemp-d0
                dtemp=AAPL.at[0,'timestamp']
                dtemp_parsed=dtemp.split("-")
                dtemp=date(int(dtemp_parsed[0]),int(dtemp_parsed[1]),int(dtemp_parsed[2]))
                d0=dtemp-maxd
                ind=99
                for j in range(0,100):
                    dtemp=AAPL.at[j,'timestamp']
                    dtemp_parsed=dtemp.split("-")
                    dtemp=date(int(dtemp_parsed[0]),int(dtemp_parsed[1]),int(dtemp_parsed[2]))
                    if dtemp<d0:
                        ind=j-1
                        break
                ansx=np.zeros(ind+1)
                for l in range(0,ind+1):
                    ansy.append(AAPL.at[l,'timestamp'])
                for i in range(0,len(comps)):
                    if comps[i]=="AAPL":
                        dates_parsed=dates[i].split("-")
                        try:
                        	d0=date(int(dates_parsed[0]),int(dates_parsed[1]),int(dates_parsed[2]))
                        except:
                        	return render(request,'invalid.html')
                        ind=99
                        for j in range(0,100):
                            dtemp=AAPL.at[j,'timestamp']
                            dtemp_parsed=dtemp.split("-")
                            dtemp=date(int(dtemp_parsed[0]),int(dtemp_parsed[1]),int(dtemp_parsed[2]))
                            if dtemp<d0:
                                ind=j-1
                                break
                        #if i==0:
                        #    ansx=np.zeros(ind+1)
                        #    for l in range(0,ind+1):
                        #        ansy.append(AAPL.at[l,'timestamp'])
                        try:
                        	if float(quant[i])<0:
                        		return render(request, 'invalid.html')
                        except:
                        	return render(request, 'invalid.html')
                        for l in range(0,ind+1):
                            ansx[l]=ansx[l]+(float(AAPL.at[l,'close'])*float(quant[i]))
                    elif comps[i]=="BANF":
                        dates_parsed=dates[i].split("-")
                        try:
                        	d0=date(int(dates_parsed[0]),int(dates_parsed[1]),int(dates_parsed[2]))
                        except:
                        	return render(request,'invalid.html')
                        ind=99
                        for j in range(0,100):
                            dtemp=AAPL.at[j,'timestamp']
                            dtemp_parsed=dtemp.split("-")
                            dtemp=date(int(dtemp_parsed[0]),int(dtemp_parsed[1]),int(dtemp_parsed[2]))
                            if dtemp<d0:
                                ind=j-1
                                break
                        #if i==0:
                        #    ansx=np.zeros(ind+1)
                        #    for l in range(0,ind+1):
                        #        ansy.append(BANF.at[l,'timestamp'])
                        try:
                        	if float(quant[i])<0:
                        		return render(request, 'invalid.html')
                        except:
                        	return render(request, 'invalid.html')
                        for l in range(0,ind+1):
                            ansx[l]=ansx[l]+(float(BANF.at[l,'close'])*float(quant[i]))
                    elif comps[i]=="CASH":
                        dates_parsed=dates[i].split("-")
                        try:
                        	d0=date(int(dates_parsed[0]),int(dates_parsed[1]),int(dates_parsed[2]))
                        except:
                        	return render(request,'invalid.html')
                        ind=99
                        for j in range(0,100):
                            dtemp=CASH.at[j,'timestamp']
                            dtemp_parsed=dtemp.split("-")
                            dtemp=date(int(dtemp_parsed[0]),int(dtemp_parsed[1]),int(dtemp_parsed[2]))
                            if dtemp<d0:
                                ind=j-1
                                break
                        #if i==0:
                        #    ansx=np.zeros(ind+1)
                        #    for l in range(0,ind+1):
                        #        ansy.append(CASH.at[l,'timestamp'])
                        try:
                        	if float(quant[i])<0:
                        		return render(request, 'invalid.html')
                        except:
                        	return render(request, 'invalid.html')
                        for l in range(0,ind+1):
                            ansx[l]=ansx[l]+(float(CASH.at[l,'close'])*float(quant[i]))
                    elif comps[i]=="FCEL":
                        dates_parsed=dates[i].split("-")
                        try:
                        	d0=date(int(dates_parsed[0]),int(dates_parsed[1]),int(dates_parsed[2]))
                        except:
                        	return render(request, 'invalid.html')
                        ind=99
                        for j in range(0,100):
                            dtemp=AAPL.at[j,'timestamp']
                            dtemp_parsed=dtemp.split("-")
                            dtemp=date(int(dtemp_parsed[0]),int(dtemp_parsed[1]),int(dtemp_parsed[2]))
                            if dtemp<d0:
                                ind=j-1
                                break
                        #if i==0:
                        #    ansx=np.zeros(ind+1)
                        #    for l in range(0,ind+1):
                        #        ansy.append(FCEL.at[l,'timestamp'])
                        try:
                        	if float(quant[i])<0:
                        		return render(request, 'invalid.html')
                        except:
                        	return render(request, 'invalid.html')
                        for l in range(0,ind+1):
                            ansx[l]=ansx[l]+(float(FCEL.at[l,'close'])*float(quant[i]))
                    elif comps[i]=="JNJ":
                        dates_parsed=dates[i].split("-")
                        try:
                        	d0=date(int(dates_parsed[0]),int(dates_parsed[1]),int(dates_parsed[2]))
                        except:
                        	return render(request,'invalid.html')
                        ind=99
                        for j in range(0,100):
                            dtemp=JNJ.at[j,'timestamp']
                            dtemp_parsed=dtemp.split("-")
                            dtemp=date(int(dtemp_parsed[0]),int(dtemp_parsed[1]),int(dtemp_parsed[2]))
                            if dtemp<d0:
                                ind=j-1
                                break

                        try:
                        	if float(quant[i])<0:
                        		return render(request, 'invalid.html')
                        except:
                        	return render(request, 'invalid.html')
                        #if i==0:
                        #    ansx=np.zeros(ind+1)
                        #    for l in range(0,ind+1):
                        #        ansy.append(JNJ.at[l,'timestamp'])
                        for l in range(0,ind+1):
                            ansx[l]=ansx[l]+(float(JNJ.at[l,'close'])*float(quant[i]))
            print("ansy=")
            print(ansx)
            print(ansy)
            data = ansx.tolist()
            data.reverse()
            val = []
            val.append(data)
            data_label = ["Portfolio"]
            xlabel = "Time"
            ylabel = "Portfolio Value"
            div_id = "mygraph1"

            view = create.data_plot(div_id, 'linechart', val, data_label, xlabel, ylabel)
            return render(request,'csv_done.html', {'r1': ansx, 'r2':ansy, 'stockview':view, 'form':form})

#            return render(request,'csv_done.html', {'r1': ansx, 'r2':ansy, 'form':form})


@login_required(login_url='login')
def manually(request):
    if request.method=="POST":
        comps=[]
        dates=[]
        quant=[]
        comps.append(request.POST['company'])
        dates.append(request.POST['date'])
        quant.append(request.POST['quantity'])
        if float(quant[0]) < 0:
            return render(request,'invalid.html')
        print("comps=")
        print(comps)
        ansy=[]
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
            pf=pf_inst()
            pf.company=comps[0]
            pf.idy=np.random.uniform()
            pf.pf_user=request.user
            x=""
            y=""
            for i in range(0,len(ansx)):
            	x=x+str(ansx[i])+" "
            	y=y+ansy[i]+" "
            pf.x=x
            pf.y=y
            pf.save()
            data = ansx.tolist()
            data.reverse()
            val = []
            val.append(data)
            data_label = ["Portfolio"]
            xlabel = "Time"
            ylabel = "Portfolio Value"
            div_id = "mygraph1"

            view = create.data_plot(div_id, 'linechart', val, data_label, xlabel, ylabel)
            return render(request,'csv_done.html', {'r1': ansx, 'r2':ansy, 'stockview':view})

#            return render(request,'csv_done.html', {'r1': ansx, 'r2':ansy})
    else:
        return render(request, "add_portfolio.html")
'''
@login_required(login_url='login')
def my_pf(request):
	pfs=pf_inst.objects.filter(pf_user=request.user)
	return render(request, 'portfolio/pf_list.html',{'pfs': pfs})
'''
@login_required(login_url='login')
def my_pf(request):
	pfs=pf_inst.objects.filter(pf_user=request.user)
	if len(pfs)==0:
		return HttpResponse('<p>no portfolio!</p>')
	print(len(pfs))
	x=pfs[0].x.split(" ")
	y=pfs[0].y.split(" ")
	ansx=[]
	ansy=[]
	for i in range(0,len(x)):
		if x[i]!=" " and x[i]!="":
			ansx.append(float(x[i]))
		if y[i]!=" " and y[i]!="":
			ansy.append(y[i])
	print(ansx)
	for i in range(1,len(pfs)):
		x=pfs[i].x.split(" ")
		print(len(x))
		for j in range(0,len(x)):
			if x[j]!=" " and x[j]!="":
				ansx[j]=ansx[j]+float(x[j])
		print(ansx)
	return render(request,'csv_done.html', {'r1': ansx, 'r2':ansy})

def pf_clear(request):
	pfs=pf_inst.objects.filter(pf_user=request.user).delete()
	return render(request, 'invalid.html')

def blog(request):
	b=blogs.objects.all()
	return render(request, 'myblog.html', {'blogs': b})
'''
def pf_details(request,idy):
	pfs=pf_inst.objects.get(idy=idy)
	ansx=[]
	ansy=[]
	x=pfs.x.split(" ")
	y=pfs.y.split(" ")
	for i in range(0,len(x)):
		if x[i]!=" " and x[i]!="":
			ansx.append(float(x[i]))
		if y[i]!=" " and y[i]!="":
			ansy.append(float(y[i]))
	return render(request,'portfolio/csv_done.html', {'r1': ansx, 'r2':ansy})
'''
'''
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
'''
