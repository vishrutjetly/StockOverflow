from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class portfolio(models.Model):
    csv_file=models.FileField(upload_to='')
