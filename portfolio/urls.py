from django.contrib import admin
from django.conf.urls import url, include
from . import views
urlpatterns=[
        url('', views.portfolio, name='portfolio'),
        #path('csv_done', views.csv_done, name='csv_done'),
]
