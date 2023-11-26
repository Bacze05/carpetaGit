from django.apps import AppConfig


class VentaConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Venta'
    verbose_name='perfiles'

    def ready(self):
        import Venta.signals
