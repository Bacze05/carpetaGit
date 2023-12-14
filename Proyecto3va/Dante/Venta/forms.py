from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Div, Submit, Button
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from .models import *
from django.contrib.auth.models import  Group


# class CustomUserCreationForm(UserCreationForm):
#     fecha_nacimiento = forms.DateField(widget=forms.DateInput(format='%d/%m/%Y', attrs={'placeholder': 'dd/mm/aaaa'}))
#     groups = forms.ModelMultipleChoiceField(
#         queryset=Group.objects.all(),
#         widget=forms.SelectMultiple(attrs={'class': 'form-control'}),
#         required=True  # Hace que la selección no sea obligatoria
#     )
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields['username'].widget.attrs['autofocus'] = True
#         self.fields['username'].help_text = ''
#         self.fields['password1'].help_text = ''  # Elimina las instrucciones de 'password1'
#         self.fields['password2'].help_text = ''
#         self.fields['fecha_nacimiento'].label = 'Fecha de nacimiento'  
#         self.fields.pop('password')
#         self.helper = FormHelper()
#         self.helper.layout = Layout(
#             Row(
#                 Div('username', css_class='col-md-12'),
#             ),
#             Row(
#                 Div('first_name', css_class='col-md-6'),
#                 Div('last_name', css_class='col-md-6'),
#             ),
#             Row(
#                 Div('rut', css_class='col-md-6'),
#                 Div('email', css_class='col-md-6'),
#             ),
#             Row(
#                 Div('password1', css_class='col-md-6'),
#                 Div('password2', css_class='col-md-6'),
#             ),
#             Row(
#                 Div('fecha_nacimiento', css_class='col-md-12'),
#             ),
#             Row(
#                 Div('groups', css_class='col-md-12'),  # Agregamos el campo 'groups'
#             ),
#             Row(
#                 Div(Submit('enviar', 'Enviar', css_class='btn btn-primary'), css_class='col-md-6'),
#                 Div(Button('cancelar', 'Cancelar', css_class='btn btn-secondary', onclick='window.location.href="/usuarios/"; return false;'), css_class='col-md-6'),
#             )
#         )

#         self.fields['fecha_nacimiento'].label = 'Fecha de nacimiento'

#     def clean(self):
#         cleaned_data = super().clean()

#         # Elimina los errores predeterminados para 'password1' y 'password2'
#         self.errors.pop('password1', None)
#         self.errors.pop('password2', None)

#         # Validación personalizada para 'password1'
#         password1 = cleaned_data.get('password1')
#         if len(password1) < 8:
#             self.add_error('password1', ValidationError('Su contraseña debe contener al menos 8 caracteres.'))

#         # Más validaciones según tus requisitos

#         # Validación predeterminada de Django para 'password1'
#         try:
#             validate_password(password1, self.instance)
#         except ValidationError as e:
#             self.add_error('password1', e.messages)

#         # Validación personalizada para 'password2'
#         password2 = cleaned_data.get('password2')
#         if password1 and password2 and password1 != password2:
#             self.add_error('password2', ValidationError('Las contraseñas no coinciden.'))

#         return cleaned_data
    
    

#     class Meta:
#         model = User
#         fields = '__all__'
#         exclude = ['user_permissions', 'last_login', 'date_joined','is_active','is_superuser','is_staff']

from django.contrib.auth import password_validation


# class CustomUserEditForm(forms.ModelForm):
#     # Campo para la nueva contraseña, no requerido en la edición
#     # groups = forms.ModelMultipleChoiceField(
#     #     queryset=Group.objects.all(),
#     #     widget=forms.SelectMultiple(attrs={'class': 'form-control'}),
#     #     required=True  # Hace que la selección no sea obligatoria
#     # )
#     password = forms.CharField(
#         label="Contraseña",
#         widget=forms.PasswordInput(render_value=True, attrs={'placeholder': 'Deje en blanco para mantener la contraseña actual'}),
#         required=False,
#         help_text="Deje en blanco para mantener la contraseña actual."
#     )

#     class Meta:
#         model = User
#         fields = ['username', 'first_name', 'last_name', 'email', 'fecha_nacimiento', 'groups']

#         # Excluye 'password' ya que se maneja de manera personalizada

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.helper = FormHelper()
#         self.helper.layout = Layout(
#             'username',
#             'first_name',
#             'last_name',
#             'email',
#             'fecha_nacimiento',
#             'groups',
#             'password',  # Agrega el campo de contraseña aquí
#             Div(
#                 Submit('enviar', 'Guardar', css_class='btn btn-primary'),
#                 Button('cancelar', 'Cancelar', css_class='btn btn-secondary', onclick='window.location.href="/usuarios/"; return false;'),
#                 css_class='row'
#             )
#         )

#     def clean_password(self):
#         # Validar la nueva contraseña solo si se proporciona
#         password = self.cleaned_data.get('password')
#         if password:
#             password_validation.validate_password(password, self.instance)
#         return password

#     def clean(self):
#         cleaned_data = super().clean()
#         password = cleaned_data.get('password')
#         # Si el campo de contraseña está vacío, asigna la contraseña actual del usuario
#         if not password:
#             cleaned_data['password'] = self.instance.password

#         return cleaned_data

#     def save(self, commit=True):
#         user = super().save(commit=False)
#         password = self.cleaned_data.get('password')

#         if password:
#             user.set_password(password)
#         if commit:
#             user.save()
#             # Imprime los grupos antes y después de guardar
#             print("Grupos antes de guardar:", self.instance.groups.all())
#             print("Grupos después de guardar:", user.groups.all())
#         return user

from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, ReadOnlyPasswordHashField
from django.contrib.auth.models import Group
from django.core.exceptions import ValidationError
# from django.core.validators import validate_password
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Div, Submit, Button


class CustomUserCreationForm(UserCreationForm):
    fecha_nacimiento = forms.DateField(widget=forms.DateInput(format='%d/%m/%Y', attrs={'placeholder': 'dd/mm/aaaa'}))
    groups = forms.ModelMultipleChoiceField(
        queryset=Group.objects.all(),
        widget=forms.SelectMultiple(attrs={'class': 'form-control'}),
        required=True
    )

    class Meta:
        model = User
        fields = '__all__'
        exclude = ['user_permissions', 'last_login', 'date_joined', 'is_active', 'is_superuser', 'is_staff', 'password']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['autofocus'] = True
        self.fields['username'].help_text = ''
        self.fields['password1'].help_text = ''
        self.fields['password2'].help_text = ''
        self.fields['fecha_nacimiento'].label = 'Fecha de nacimiento'
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
                Div('groups', css_class='col-md-12'),
            ),
            Row(
                Div(Submit('enviar', 'Enviar', css_class='btn btn-primary'), css_class='col-md-6'),
                Div(Button('cancelar', 'Cancelar', css_class='btn btn-secondary', onclick='window.location.href="/usuarios/"; return false;'), css_class='col-md-6'),
            )
        )

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


from django import forms
from django.contrib.auth.forms import UserChangeForm, ReadOnlyPasswordHashField
from django.contrib.auth.models import Group
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Div, Submit, Button

class CustomUserEditForm(UserChangeForm):
    password = ReadOnlyPasswordHashField(
        label=("Contraseña"),
        help_text=(
            "No podemos mostrar la contraseña actual. "
            "Si desea cambiar la contraseña, puede hacerlo desde el "
            "<a href=\"../password/\">página de cambio de contraseña</a>."
        ),
    )

    class Meta:
        model = User
        fields = '__all__'
        exclude = ['user_permissions', 'last_login', 'date_joined', 'is_active', 'is_superuser', 'is_staff']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
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
                Div('fecha_nacimiento', css_class='col-md-12'),
            ),
            Row(
                Div('groups', css_class='col-md-12'),
            ),
            Row(
                Div(Submit('enviar', 'Enviar', css_class='btn btn-primary'), css_class='col-md-6'),
                Div(Button('cancelar', 'Cancelar', css_class='btn btn-secondary', onclick='window.location.href="/usuarios/"; return false;'), css_class='col-md-6'),
            )
        )

    # Si se desea ocultar el campo de contraseña, descomentar las siguientes líneas
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields['password'].widget = forms.HiddenInput()
    #     self.fields['password'].label = ''
    #     self.fields['password'].help_text = ''




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

class CustomUserDeletionForm(forms.ModelForm):
    class Meta:
        model = User
        fields = []



