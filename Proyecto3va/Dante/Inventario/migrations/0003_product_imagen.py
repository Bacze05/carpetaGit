# Generated by Django 4.2.7 on 2023-11-18 15:30

import Inventario.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Inventario', '0002_category_descripcion_category_foto_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='imagen',
            field=models.ImageField(default='productos/producto.png', null=True, upload_to=Inventario.models.Product.generarNombre),
        ),
    ]
