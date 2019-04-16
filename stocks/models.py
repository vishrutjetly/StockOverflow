from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Stock(models.Model):

	name = models.CharField(max_length=30)
	# link = models.CharField(max_length=50)
	ticker = models.CharField(max_length=10)

	def __str__(self):
            return self.name

class Wishlist(object):
	user = models.ForeignKey(User, related_name='wishlist')
	stock = models.ManyToManyField(Stock, related_name='wishlist')