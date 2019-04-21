from django.db import models
from django.contrib.auth.models import User
from django.core.validators import int_list_validator
from django_mysql.models import ListCharField
# Create your models here.

class Stock(models.Model):

	name = models.CharField(max_length=30)
	# link = models.CharField(max_length=50)
	ticker = models.CharField(max_length=10)
	# meta = models.CharField(max_length=500)
	meta = ListCharField(
		base_field=models.CharField(max_length=20),
        size=500,
        max_length=(500 * 21),
        blank=True
    )

	meta_predict = ListCharField(
		base_field=models.CharField(max_length=20),
        size=500,
        max_length=(500 * 21),
        blank=True
    )

	updated_at = models.DateTimeField(auto_now=True)

	def __str__(self):
            return self.name

class Wishlist(object):
	user = models.ForeignKey(User, related_name='wishlist')
	stock = models.ManyToManyField(Stock, related_name='wishlist')
