# Generated by Django 4.2.7 on 2023-11-30 23:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Venta', '0003_remove_detalleventa_subtotal_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='venta',
            name='total_venta',
        ),
    ]