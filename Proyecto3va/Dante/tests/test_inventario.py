import pytest
from django.core.exceptions import ValidationError
from Inventario.models import *
from Venta.models import *






class TestUserManager:

    # create a user with valid username, rut, first_name, and password
    def test_create_user_with_valid_fields(self):
        user_manager = UserManager()
        user = user_manager.create_user(username='test_user', rut='1234567890', first_name='John', password='password')
        assert user.username == 'test_user'
        assert user.rut == '1234567890'
        assert user.first_name == 'John'
        assert user.is_staff == False
        assert user.is_superuser == False

    # create a superuser with valid username, rut, first_name, and password
    def test_create_superuser_with_valid_fields(self):
        user_manager = UserManager()
        superuser = user_manager.create_superuser(username='test_superuser', rut='1234567890', first_name='Admin', password='password')
        assert superuser.username == 'test_superuser'
        assert superuser.rut == '1234567890'
        assert superuser.first_name == 'Admin'
        assert superuser.is_staff == True
        assert superuser.is_superuser == True

    # create a user with extra fields
    def test_create_user_with_extra_fields(self):
        user_manager = UserManager()
        extra_fields = {'fecha_nacimiento': '1990-01-01', 'last_name': 'Doe'}
        user = user_manager.create_user(username='test_user', rut='1234567890', first_name='John', password='password', **extra_fields)
        assert user.username == 'test_user'
        assert user.rut == '1234567890'
        assert user.first_name == 'John'
        assert user.is_staff == False
        assert user.is_superuser == False
        assert user.fecha_nacimiento == '1990-01-01'
        assert user.last_name == 'Doe'

    # create a user with empty username
    def test_create_user_with_empty_username(self):
        user_manager = UserManager()
        with pytest.raises(ValueError):
            user_manager.create_user(username='', rut='1234567890', first_name='John', password='password')

    # create a user with empty rut
    def test_create_user_with_empty_rut(self):
        user_manager = UserManager()
        with pytest.raises(ValueError):
            user_manager.create_user(username='test_user', rut='', first_name='John', password='password')

    # create a user with empty first_name
    def test_create_user_with_empty_first_name(self):
        user_manager = UserManager()
        with pytest.raises(ValueError):
            user_manager.create_user(username='test_user', rut='1234567890', first_name='', password='password')