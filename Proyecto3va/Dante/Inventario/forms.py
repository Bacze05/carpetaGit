from django import forms
from .models import Category, Suppliers, Product

from django import forms


class CategoryForm(forms.ModelForm):
    name = forms.CharField(
        label='Nombre Categoria',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese el nombre de la categoría'}),
        max_length=50,
        required=True,
        help_text='Ingrese el nombre de la categoría.',
    )

    descripcion = forms.CharField(
        label='Descripción general',
        widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Ingrese una descripción'}),
        max_length=255,
        required=True,
        help_text='Ingrese una descripción general para la categoría.',
    )

    foto = forms.ImageField(
        required=False,
        widget=forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
        help_text='Seleccione una imagen para la categoría (opcional).',
    )

    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre')
        if nombre.strip() == '':
            raise forms.ValidationError("El nombre no puede consistir solo de espacios en blanco.")
        return nombre

    class Meta:
        model = Category
        fields = '__all__'


class SuppliersForm(forms.ModelForm):
    class Meta:
        model = Suppliers
        fields = ['name', 'run', 'cellphone', 'email']

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'name_category', 'price_sold', 'buy_price', 'stock', 'bar_code', 'minimum_amount', 'suppliers', 'imagen']
