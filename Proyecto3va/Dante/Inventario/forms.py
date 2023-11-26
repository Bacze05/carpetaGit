from django import forms
from .models import Category, Suppliers, Product




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
    name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre del proveedor'}),
        max_length=100,
    )
    run = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'RUN'}),
        max_length=10,
    )
    cellphone = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Número de teléfono'}),
        max_length=15,
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Correo electrónico'}),
    )

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if name.strip() == '':
            raise forms.ValidationError("El nombre no puede consistir solo de espacios en blanco.")
        return name

    class Meta:
        model = Suppliers
        fields = ['name', 'run', 'cellphone', 'email']


class ProductForm(forms.ModelForm):
    name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre del Producto'}),
        max_length=100,
    )
    name_category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
    )
    price_sold = forms.IntegerField(
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Precio de Venta'}),
    )
    buy_price = forms.IntegerField(
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Precio de Compra'}),
    )
    stock = forms.IntegerField(
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Stock'}),
    )
    bar_code = forms.IntegerField(
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Código de Barras'}),
    )
    minimum_amount = forms.IntegerField(
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Cantidad Mínima'}),
    )
    suppliers = forms.ModelChoiceField(
        queryset=Suppliers.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
    )
    imagen = forms.ImageField(
        required=False,
        widget=forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
    )

    class Meta:
        model = Product
        fields = ['name', 'name_category', 'price_sold', 'buy_price', 'stock', 'bar_code', 'minimum_amount', 'suppliers', 'imagen']
