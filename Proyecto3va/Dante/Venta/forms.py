from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Div, Submit, Button
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from .models import *


class CustomUserCreationForm(UserCreationForm):
    fecha_nacimiento = forms.DateField(widget=forms.DateInput(format='%d/%m/%Y', attrs={'placeholder': 'dd/mm/aaaa'}))
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['autofocus'] = True
        self.fields['username'].help_text = ''
        self.fields['password1'].help_text = ''  # Elimina las instrucciones de 'password1'
        self.fields['password2'].help_text = ''
        self.fields['fecha_nacimiento'].label = 'Fecha de nacimiento'  
        self.fields.pop('password')
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Div('username', css_class='col-md-12'),
            ),
            Row(
                Div('first_name', css_class='col-md-6'),
                Div('last_name', css_class='col-md-6'),
            ),
            Row(
                Div('rut', css_class='col-md-6'),
                Div('email', css_class='col-md-6'),
            ),
            Row(
                Div('password1', css_class='col-md-6'),
                Div('password2', css_class='col-md-6'),
            ),
            Row(
                Div('fecha_nacimiento', css_class='col-md-12'),
            ),
            Row(
                Div('groups', css_class='col-md-12'),  # Agregamos el campo 'groups'
            ),
            Row(
                Div(Submit('enviar', 'Enviar', css_class='btn btn-primary'), css_class='col-md-6'),
                Div(Button('cancelar', 'Cancelar', css_class='btn btn-secondary', onclick='window.location.href="/"; return false;'), css_class='col-md-6'),
            )
        )

        self.fields['fecha_nacimiento'].label = 'Fecha de nacimiento'

    def clean(self):
        cleaned_data = super().clean()

        # Elimina los errores predeterminados para 'password1' y 'password2'
        self.errors.pop('password1', None)
        self.errors.pop('password2', None)

        # Validación personalizada para 'password1'
        password1 = cleaned_data.get('password1')
        if len(password1) < 8:
            self.add_error('password1', ValidationError('Su contraseña debe contener al menos 8 caracteres.'))

        # Más validaciones según tus requisitos

        # Validación predeterminada de Django para 'password1'
        try:
            validate_password(password1, self.instance)
        except ValidationError as e:
            self.add_error('password1', e.messages)

        # Validación personalizada para 'password2'
        password2 = cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            self.add_error('password2', ValidationError('Las contraseñas no coinciden.'))

        return cleaned_data

    class Meta:
        model = User
        fields = '__all__'
        exclude = ['user_permissions', 'last_login', 'date_joined','is_active','is_superuser','is_staff']



class DetalleVentaForm(forms.ModelForm):
    class Meta:
        model = DetalleVenta
        fields = ['venta', 'producto', 'cantidad', 'precio', 'descuento']

    def clean(self):
        cleaned_data = super().clean()
        cantidad = cleaned_data.get('cantidad')
        precio = cleaned_data.get('precio')

        # Realiza validaciones adicionales según tu lógica de negocio
        if cantidad and cantidad <= 0:
            raise forms.ValidationError("La cantidad debe ser mayor que cero.")

        if precio and precio <= 0:
            raise forms.ValidationError("El precio debe ser mayor que cero.")

        return cleaned_data
