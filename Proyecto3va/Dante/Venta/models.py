from django.db import models

# Create your models here.

class Venta(models.Model):
    fecha = models.DateTimeField(auto_now_add=True)
    

class DetalleVenta(models.Model):
    venta = models.ForeignKey(Venta, on_delete=models.CASCADE)
    producto = models.ForeignKey('Inventario.Product', on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
   