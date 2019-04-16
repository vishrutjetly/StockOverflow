from django import forms
from . import models

class csv_upload(forms.ModelForm):
    class Meta:
        model = models.portfolio
        fields = {'csv_file'}
 
