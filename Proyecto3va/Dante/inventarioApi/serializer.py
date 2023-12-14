from rest_framework import serializers
from Venta.models import User 
from Inventario.models import Product

class UsuariosSerializados(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class productosSerializados(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'