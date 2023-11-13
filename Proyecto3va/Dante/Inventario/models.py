from django.db import models

# Create your models here.
class Category(models.Model):
    name=models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
class Suppliers(models.Model):
    name=models.CharField(max_length=100)
    run=models.CharField(max_length=10)
    cellphone=models.PositiveIntegerField()
    email=models.EmailField()

    def __str__(self):
        return self.name

class Product(models.Model):
    name=models.CharField(max_length=100,verbose_name=("Name"))
    name_category=models.ForeignKey("Inventario.Category", verbose_name=("Name Category"), on_delete=models.PROTECT)
    price_sold=models.PositiveIntegerField(verbose_name=("Price Sold"))
    buy_price=models.PositiveIntegerField(verbose_name=("Buy Price"))
    stock=models.PositiveIntegerField(verbose_name=("Stock"))
    bar_code=models.IntegerField(verbose_name=("Bar Code"))
    minimum_amount=models.PositiveIntegerField(verbose_name=("Minimum Amount"))
    suppliers=models.ForeignKey("Inventario.Suppliers", verbose_name=("Suppliers"), on_delete=models.PROTECT)

    def __str__(self):
        return self.name