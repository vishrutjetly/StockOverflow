from django.db import models

# Create your models here.

class Stock(models.Model):

	name = models.CharField(max_length=30)
	# link = models.CharField(max_length=50)
	ticker = models.CharField(max_length=10)

	def __str__(self):
            return self.name