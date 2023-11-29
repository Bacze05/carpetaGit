# Generated by Django 4.2.7 on 2023-11-29 22:14

import Inventario.models
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, validators=[django.core.validators.MinLengthValidator(limit_value=1, message='El nombre no puede estar vacío.')])),
                ('descripcion', models.TextField(default=None, null=True, validators=[django.core.validators.MinLengthValidator(limit_value=1)])),
                ('foto', models.ImageField(default='categorias/categoria.png', null=True, upload_to=Inventario.models.Category.generarNombre)),
            ],
        ),
        migrations.CreateModel(
            name='Suppliers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('run', models.CharField(max_length=10)),
                ('cellphone', models.PositiveIntegerField()),
                ('email', models.EmailField(max_length=254)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Name')),
                ('price_sold', models.PositiveIntegerField(verbose_name='Price Sold')),
                ('buy_price', models.PositiveIntegerField(verbose_name='Buy Price')),
                ('stock', models.PositiveIntegerField(verbose_name='Stock')),
                ('bar_code', models.IntegerField(verbose_name='Bar Code')),
                ('minimum_amount', models.PositiveIntegerField(verbose_name='Minimum Amount')),
                ('imagen', models.ImageField(default='productos/producto.png', null=True, upload_to=Inventario.models.Product.generarNombre)),
                ('name_category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Inventario.category', verbose_name='Name Category')),
                ('suppliers', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='Inventario.suppliers', verbose_name='Suppliers')),
            ],
        ),
        migrations.CreateModel(
            name='Descuento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_descuento', models.CharField(max_length=100, verbose_name='Nombre Descuento')),
                ('valor_descuento', models.DecimalField(decimal_places=2, help_text='Porcentaje de descuento', max_digits=5)),
                ('producto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Inventario.product')),
            ],
            options={
                'verbose_name': 'Descuento',
                'verbose_name_plural': 'Descuentos',
                'ordering': ['id'],
            },
        ),
    ]
