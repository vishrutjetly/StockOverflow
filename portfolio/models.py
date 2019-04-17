from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class portfolio(models.Model):
    csv_file=models.FileField(upload_to='')

class pf_inst(models.Model):
    company=models.TextField()
    idy=models.FloatField()
    date=models.DateTimeField(auto_now_add=True)
    pf_user=models.ForeignKey(User, default=None, on_delete=models.CASCADE)
    x=models.TextField()
    y=models.TextField()
