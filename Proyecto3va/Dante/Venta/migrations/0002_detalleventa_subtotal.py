# Generated by Django 4.2.7 on 2023-11-30 23:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Venta', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='detalleventa',
            name='subtotal',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
    ]