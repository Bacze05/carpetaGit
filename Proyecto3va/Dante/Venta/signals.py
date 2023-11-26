from django.contrib.auth.models import Group
from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import Profile

@receiver(post_save, sender=Profile)
def add_user_to_vendedor_group(sender, instance, created, **kwargs):
    if created:
        try:
            vendedor= Group.objects.get(name='Vendedor')
        except Group.DoesNotExist:
            vendedor=Group.objects.create(name='Vendedor')
        instance.user.groups.add(vendedor)