from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class Venta(models.Model):
    fecha = models.DateTimeField(auto_now_add=True)
    

class DetalleVenta(models.Model):
    venta = models.ForeignKey(Venta, on_delete=models.CASCADE)
    producto = models.ForeignKey('Inventario.Product', on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
   
class User(AbstractUser):
    fecha_nacimiento = models.DateField(null=True, blank=True)
    rut = models.CharField(max_length=12, unique=True, null=True, blank=True)
