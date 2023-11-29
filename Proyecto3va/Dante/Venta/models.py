from django.db import models
from django.contrib.auth.models import AbstractUser,User
from django.conf import settings
from django.db.models.signals import post_save
from django.utils import timezone
from Inventario.models import Product, Descuento



# Create your models here.


class Cajas(models.Model):
    vendedor = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    monto_inicial = models.DecimalField(default=0, max_digits=10, decimal_places=2, verbose_name="Monto Inicial")
    cantidad_vendida = models.DecimalField(default=0, max_digits=10, decimal_places=2, verbose_name="Cantidad Vendida")
    fecha_apertura = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Apertura")
    fecha_cierre = models.DateTimeField(null=True, blank=True, verbose_name="Fecha de Cierre")
    cerrada = models.BooleanField(default=False, verbose_name="Caja Cerrada")

    def __str__(self):
        return f"Caja {self.id} - {self.vendedor.username}"

    def abrir_caja(self):
        self.cerrada = False
        self.save()

    def cerrar_caja(self):
        self.cerrada = True
        self.fecha_cierre = timezone.now()  # Establecer la fecha de cierre en el momento real
        self.save()

class Venta(models.Model):
    fecha = models.DateTimeField(auto_now_add=True)
    caja = models.ForeignKey(Cajas, on_delete=models.CASCADE, default=1)
    total_venta = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def calcular_total_venta(self):
        detalles_venta = DetalleVenta.objects.filter(venta=self)
        total = sum([detalle.calcular_subtotal() for detalle in detalles_venta])
        self.total_venta = total
        self.save()

    def __str__(self):
        return f"Venta {self.id} - {self.fecha}"

class DetalleVenta(models.Model):
    venta = models.ForeignKey(Venta, on_delete=models.CASCADE)
    producto = models.ForeignKey(Product, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    descuento = models.ForeignKey(Descuento, on_delete=models.SET_NULL, null=True, blank=True)

    def calcular_subtotal(self):
        if self.descuento:
            subtotal = (self.cantidad * self.precio) - ((self.cantidad * self.precio * self.descuento.valor_descuento) / 100)
        else:
            subtotal = self.cantidad * self.precio
        return subtotal

class Reporte(models.Model):
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    nombre = models.CharField(max_length=100, verbose_name="Nombre del Reporte", db_index=True)
    descripcion = models.TextField(null=True, blank=True, verbose_name="Descripción del Reporte")
    datos = models.JSONField(default=dict, verbose_name="Datos del Reporte")

    class Meta:
        indexes = [
            models.Index(fields=['nombre'], name='idx_nombre_length'),
        ]

    def __str__(self):
        return self.nombre


   
class User(AbstractUser):
    fecha_nacimiento = models.DateField(null=True, blank=True)
    rut = models.CharField(max_length=12, unique=True, null=True, blank=True)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,related_name='profile')
    class Meta:
        verbose_name= 'Perfil'
        verbose_name_plural= 'Perfiles'
        ordering = ['-id']

    def __str__(self):
        return self.user.username

def create_user_profile(sender,instance,created, **kwargs):
    if created :
        Profile.objects.create(user=instance)
    
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

post_save.connect(create_user_profile,sender=User)
post_save.connect(save_user_profile,sender=User)