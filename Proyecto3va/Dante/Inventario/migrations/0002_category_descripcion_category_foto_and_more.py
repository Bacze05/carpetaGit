# Generated by Django 4.2.7 on 2023-11-18 15:24

import Inventario.models
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Inventario', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='descripcion',
            field=models.TextField(default=None, null=True, validators=[django.core.validators.MinLengthValidator(limit_value=1)]),
        ),
        migrations.AddField(
            model_name='category',
            name='foto',
            field=models.ImageField(default='categorias/categoria.png', null=True, upload_to=Inventario.models.Category.generarNombre),
        ),
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(max_length=100, validators=[django.core.validators.MinLengthValidator(limit_value=1, message='El nombre no puede estar vacío.')]),
        ),
    ]
