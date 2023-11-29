import os
from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator,MinLengthValidator
from django.core.exceptions import ValidationError

# Create your models here.
class Category(models.Model):
    name=models.CharField(max_length=100, validators=[MinLengthValidator(limit_value=1, message="El nombre no puede estar vacío.")])
    descripcion = models.TextField(null=True, default=None, validators=[MinLengthValidator(limit_value=1)])

    def generarNombre(instance, filename):
        extension = os.path.splitext(filename)[1][1:]
        ruta = 'categorias'
        fecha = timezone.now().strftime("%d%m%Y_%H%M%S")
        nombre = "{}.{}".format(fecha, extension)
        return os.path.join(ruta, nombre)

    foto = models.ImageField(upload_to=generarNombre, null=True, default='categorias/categoria.png')

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
    name_category=models.ForeignKey("Inventario.Category", verbose_name=("Name Category"), on_delete=models.CASCADE)
    price_sold=models.PositiveIntegerField(verbose_name=("Price Sold"))
    buy_price=models.PositiveIntegerField(verbose_name=("Buy Price"))
    stock=models.PositiveIntegerField(verbose_name=("Stock"))
    bar_code=models.IntegerField(verbose_name=("Bar Code"))
    minimum_amount=models.PositiveIntegerField(verbose_name=("Minimum Amount"))
    suppliers=models.ForeignKey("Inventario.Suppliers", verbose_name=("Suppliers"), on_delete=models.PROTECT)

    def generarNombre(instance, filename):
        extension = os.path.splitext(filename)[1][1:]
        ruta = 'productos'
        fecha = timezone.now().strftime("%d%m%Y_%H%M%S")
        nombre = "{}.{}".format(fecha, extension)
        return os.path.join(ruta, nombre)

    imagen = models.ImageField(upload_to=generarNombre, null=True, default='productos/producto.png')
    def clean(self):
         
        # Realiza validaciones adicionales al limpiar los datos del modelo.
        # En este caso, asegura que el precio de venta sea mayor que el precio de compra.
    
        if self.price_sold <= self.buy_price:
            raise ValidationError('El precio de venta debe ser mayor que el precio de compra.')
    
    def actualizar_stock_venta(self, cantidad):
        if self.stock >= cantidad:
            self.stock -= cantidad
            self.save()
        else:
            raise ValidationError('No hay suficiente stock disponible para realizar la venta.')

    def __str__(self):
        return self.name
    
class Descuento(models.Model):
    producto = models.ForeignKey('Product', on_delete=models.CASCADE)
    name_descuento = models.CharField(max_length=100, verbose_name="Nombre Descuento")
    valor_descuento = models.DecimalField(max_digits=5, decimal_places=2, help_text="Porcentaje de descuento")

    def __str__(self):
        return self.name_descuento

    class Meta:
        verbose_name = "Descuento"
        verbose_name_plural = "Descuentos"
        ordering = ["id"]