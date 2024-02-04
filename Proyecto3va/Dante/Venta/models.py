from django.db import models
from django.contrib.auth.models import  AbstractUser,User, BaseUserManager
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
        self.fecha_cierre = timezone.now()
        self.save()
    @property
    def turno_abierto(self):
        return not self.cerrada
class Venta(models.Model):
    fecha = models.DateTimeField(auto_now_add=True)
    caja = models.ForeignKey(Cajas, on_delete=models.CASCADE, default=1)
    # total_venta = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    def __str__(self):
        return f"Venta {self.id} - {self.fecha}"

class DetalleVenta(models.Model):
    venta = models.ForeignKey(Venta, on_delete=models.CASCADE, related_name='detalles')
    producto = models.ForeignKey(Product, related_name='detalles', on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    descuento = models.ForeignKey(Descuento, on_delete=models.SET_NULL, null=True, blank=True)


    def calcular_subtotal(self):
        
        return self.precio * self.cantidad


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


class UserManager(BaseUserManager):
    def _create_user(self, username, rut, first_name,password,is_staff,is_superuser,**extra_fields): 
        user= self.model(
            username=username,
            rut=rut,
            first_name=first_name,
            is_staff=is_staff,
            is_superuser=is_superuser,
            **extra_fields

        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_user(self,username,rut,first_name,password=None,**extra_fields):
        return self._create_user(username,rut,first_name,password,False,False,**extra_fields)
    
    def create_superuser(self,username,rut,first_name,password=None,**extra_fields):
        return self._create_user(username,rut,first_name,password,True,True,**extra_fields)
     


class User(AbstractUser):
    username= models.CharField('Nombre de Usuario', unique=True, max_length=100)
    first_name= models.CharField('Nombres', max_length=200, blank=True, null=True)
    last_name= models.CharField('Apellidos', max_length=200, blank=True, null=True)
    is_active= models.BooleanField(default=True)
    is_staff=models.BooleanField(default=False)
    fecha_nacimiento = models.DateField(null=True, blank=True)
    rut = models.CharField(max_length=12, unique=True, null=True, blank=True)
    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['rut', 'first_name', 'last_name']

    def __str__(self) :
        return f'{self.first_name}, {self.last_name}'
    
    
    

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,related_name='profile')
    class Meta:
        verbose_name= 'Perfil'
        verbose_name_plural= 'Perfiles'
        ordering = ['-id']

    def __str__(self):
        return self.user.username

def create_user_profile(sender,instance,created, **kwargs):
    if created and not hasattr(instance, 'profile'):
        Profile.objects.create(user=instance)
        # Verifica si ya hay una caja abierta
        if not Cajas.objects.filter(vendedor=instance, cerrada=False).exists():
            Cajas.objects.create(vendedor=instance)

    
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

post_save.connect(create_user_profile,sender=User)
post_save.connect(save_user_profile,sender=User)


