from django.contrib import admin
from django.conf.urls import url, include
from . import views

app_name="portfolio_app"

urlpatterns=[
	url(r'^$', views.portfolio, name='portfolio'),
	url(r'^manually/', views.manually, name='manually'),
	url(r'^my_pf/', views.my_pf, name='my_pf'),
	url(r'^pf_clear/',views.pf_clear, name='pf_clear'),
	url(r'^blog/',views.blog, name='blog'),


        #url(r'^details/(?P<idy>\d+)/$', views.pf_details, name='details'),
]
