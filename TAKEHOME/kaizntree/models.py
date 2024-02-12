from django.db import models

# Create your models here.

class Items(models.Model):
    sku = models.CharField(max_length=20, primary_key=True)
    name = models.CharField(max_length=50)
    category = models.CharField(max_length=50)
    stock_status = models.IntegerField()
    available_stock = models.IntegerField()