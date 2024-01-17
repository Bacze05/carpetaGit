import pytest
from django.core.exceptions import ValidationError
from Inventario.models import *

@pytest.mark.django_db
def test_precio_venta_mayor_que_compra():
    # Prueba para el método clean() del modelo Product
    with pytest.raises(ValidationError, match='El precio de venta debe ser mayor que el precio de compra.'):
        product = Product(
            name='Producto de prueba',
            name_category=Category.objects.create(name='Categoria de prueba'),
            price_sold=10,
            buy_price=20,  # Aquí establecemos un precio de compra mayor al precio de venta a propósito
            stock=100,
            bar_code=123456789,
            minimum_amount=10,
            suppliers=Suppliers.objects.create(name='Proveedor de prueba', run='1234567890', cellphone=123456789, email='proveedor@example.com')
        )
        product.full_clean()  # Llama al método clean() del modelo

@pytest.mark.django_db
def test_actualizar_stock_venta_suficiente():
    # Prueba para el método actualizar_stock_venta() del modelo Product
    product = Product.objects.create(
        name='Producto de prueba',
        name_category=Category.objects.create(name='Categoria de prueba'),
        price_sold=20,
        buy_price=10,
        stock=100,
        bar_code=123456789,
        minimum_amount=10,
        suppliers=Suppliers.objects.create(name='Proveedor de prueba', run='1234567890', cellphone=123456789, email='proveedor@example.com')
    )

    product.actualizar_stock_venta(5)  # Intenta actualizar el stock con una cantidad que no agota el stock

    assert product.stock == 95  # Verifica que el stock se haya actualizado correctamente

@pytest.mark.django_db
def test_actualizar_stock_venta_insuficiente():
    # Prueba para el método actualizar_stock_venta() del modelo Product
    product = Product.objects.create(
        name='Producto de prueba',
        name_category=Category.objects.create(name='Categoria de prueba'),
        price_sold=20,
        buy_price=10,
        stock=5,  # Establecemos un stock bajo a propósito
        bar_code=123456789,
        minimum_amount=10,
        suppliers=Suppliers.objects.create(name='Proveedor de prueba', run='1234567890', cellphone=123456789, email='proveedor@example.com')
    )

    with pytest.raises(ValidationError, match='No hay suficiente stock disponible para realizar la venta.'):
        product.actualizar_stock_venta(10)  # Intenta actualizar el stock con una cantidad mayor al stock disponible


# from django.urls import reverse
# from Venta.models import User
# @pytest.fixture
# def logged_in_client(client):
#     # Inicia sesión como un usuario válido para las pruebas
#     user = User.objects.create_user(username='testuser', password='testpassword', rut=2098881,first_name="kantra")
#     client.login(username='testuser', password='testpassword')
#     return client

# @pytest.fixture
# def category():
#     return Category.objects.create(name='Electronics', descripcion='Category for electronics')

# @pytest.mark.django_db
# def test_product_registration(logged_in_client, category):
#     # Datos de prueba
#     product_data = {
#         'name': 'Test Product',
#         'name_category': category.id,
#         'price_sold': 2050,
#         'buy_price': 150,
#         'stock': 100,
#         'bar_code': 1234567890,
#         'minimum_amount': 10,
#         'suppliers': 1,  # Reemplaza con el ID real del proveedor
#     }

#     # Construir la URL con el argumento 'nombre' utilizando el nombre de la categoría creada en la fixture
#     url = f'/categorias/list/{category.name}/'

#     # Envía una solicitud POST para registrar el producto
#     response = logged_in_client.post(url, data=product_data, follow=True)

#     # Impresiones para depuración
#     print(f'Categoría en la prueba: {category.name}')

#     # Reversión de la URL con el argumento necesario
#     lista_productos_url = reverse('listaProductos', kwargs={'nombre': category.name})

#     # Impresiones para depuración
#     print(f'URL construida: {lista_productos_url}')
#     print(f'Redirección real: {response.redirect_chain[-1][0]}')

#     # Normaliza las URLs antes de compararlas
#     assert response.redirect_chain[-1][0].rstrip('/') == f'http://testserver{lista_productos_url}'.rstrip('/')


# Archivo test_views.py

import pytest
from django.urls import reverse
from Venta.models import User
from django.test import Client
from faker import Faker

fake = Faker()

@pytest.fixture
def cliente():
    return Client()

@pytest.fixture
def usuario_regular():
    return User.objects.create_user(
        username=fake.user_name(),
        rut=fake.unique.random_number(9),
        first_name=fake.first_name(),
        password=fake.password()
    )
@pytest.fixture
def usuario_admin():
    return User.objects.create_superuser(
        username=fake.user_name(),
        rut=fake.unique.random_number(9),
        first_name=fake.first_name(),
        password=fake.password()
    )

@pytest.mark.django_db
def test_agregar_trabajador(cliente, usuario_regular):
    fake = Faker()
    cliente.force_login(usuario_regular)

    url = reverse('usuarios') 
    datos_trabajador = {
        'username': fake.user_name(),
        'rut': fake.unique.random_number(9),
        'first_name': fake.first_name(),
        'password': 'brunoPtah300',
        
    }

    print(f"Datos del trabajador antes de la creación: {datos_trabajador}")

    response = cliente.post(url, datos_trabajador, follow=True)

    print(f"Respuesta del servidor: {response.content.decode()}")
    print(f"Código de estado de la respuesta: {response.status_code}")

    assert response.status_code == 200  # Ajusta el código de estado esperado

    # Verifica que el trabajador esté registrado en el sistema
    print(f"Usuarios en la base de datos después de la prueba: {User.objects.all()}")
    assert User.objects.filter(username=datos_trabajador['username']).exists()