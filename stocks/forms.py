from django import forms

class SearchStock(forms.Form):
	stock_name = forms.CharField(label='stock_name',max_length=50,)
