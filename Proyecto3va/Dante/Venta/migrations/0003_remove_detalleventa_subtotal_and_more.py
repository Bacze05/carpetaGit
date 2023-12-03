# Generated by Django 4.2.7 on 2023-11-30 23:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Venta', '0002_detalleventa_subtotal'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='detalleventa',
            name='subtotal',
        ),
        migrations.AlterField(
            model_name='detalleventa',
            name='venta',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='detalles', to='Venta.venta'),
        ),
    ]