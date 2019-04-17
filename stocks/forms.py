from django import forms

class SearchStock(forms.Form):
	stock_name = forms.CharField(label='stock_name',max_length=50)

class SearchStockCompare(forms.Form):
	stock_name1 = forms.CharField(label='stock_name1',max_length=50)
	stock_name2 = forms.CharField(label='stock_name2',max_length=50)