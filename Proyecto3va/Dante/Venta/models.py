from django.db import models
from django.contrib.auth.models import AbstractUser,User
from django.db.models.signals import post_save

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