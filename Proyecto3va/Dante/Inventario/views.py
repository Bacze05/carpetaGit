from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.serializers import serialize
from django.views.generic import TemplateView,ListView,UpdateView, CreateView,DeleteView, View
from django.urls import reverse_lazy
from Inventario.forms import *
from Inventario.models import *
from .mixins import *


#VISTAS GENERALES PAGINAS PRINCIPALES

class Home(TemplateView):
    template_name='base.html'

class Categorias(LoginRequiredMixin,View):
    model=Category
    form_class= CategoryForm
    template_name='inventario/Categorias.html'
    def get_queryset(self):
        return self.model.objects.all()
    
    def get_context_data(self, **kwargs):
        context = {}
        context["categorias"] = self.get_queryset()
        context["form"] = self.form_class 
        return context
    
    def get(self,request,*args, **kwargs):  
        return render(request,self.template_name,self.get_context_data())
    
    def post(self,request,*args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            return redirect('categorias')
     

class ListaProveedores(LoginRequiredMixin,View):
    model=Suppliers
    form_class= SuppliersForm
    template_name='inventario/proveedores.html'
    def get_queryset(self):
        return self.model.objects.all()
    
    def get_context_data(self, **kwargs):
        context = {}
        context["proveedores"] = self.get_queryset()
        context["form"] = self.form_class
        return context
    
    
    def get(self, request, *args, **kwargs):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            data = serialize('json', self.get_queryset())
            return HttpResponse(data, 'application/json')
        else:
            return render(request,self.template_name,self.get_context_data())   
    
    def post(self,request,*args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            return redirect('proveedores')
    
class ListaProductosView(LoginRequiredMixin, ListView, View):
    model=Product
    form_class= ProductForm
    template_name = 'inventario/listaProductos.html'
    def get_context_data(self, **kwargs):
        context = {}
        nombre_categoria = kwargs.get('nombre')
        
        try:
            context['categorias'] = Category.objects.get(name=nombre_categoria)
        except Category.DoesNotExist:
            # Manejar la categoría que no existe, por ejemplo, redirigir a una página de error
            print(f"Categoría '{nombre_categoria}' no encontrada.")
            context['categorias'] = None  # Puedes establecerlo en None o cualquier otro valor por defecto

        context["form"] = self.form_class
        return context

    def get(self, request, *args, **kwargs):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            data = serialize('json', self.get_queryset())
            return HttpResponse(data, 'application/json')
        else:
            nombre_categoria = kwargs.get('nombre')
            context = self.get_context_data(nombre_categoria=nombre_categoria)
            return render(request, self.template_name, context)
    def get_queryset(self):
        try:
            nombre_categoria = self.kwargs.get('nombre')
            categoria = Category.objects.get(name=nombre_categoria)
            return Product.objects.filter(name_category=categoria)
        except Category.DoesNotExist as e:
            # Manejar la categoría que no existe e imprimir detalles
            print(f"Error: {e}")
            return Product.objects.none()

    def post(self, request, *args, **kwargs):
        # Manejar la creación de productos aquí
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()

        nombre_categoria = kwargs.get('nombre')
        return redirect('listaProductos', nombre=nombre_categoria)



    

#METODOS EDITAR

class CategoriaEdicion(LoginRequiredMixin,UpdateView):
    model = Category
    template_name = 'inventario/mantenedorCategoria.html'
    form_class = CategoryForm
    success_url = reverse_lazy('categorias')

    def form_valid(self, form):
        # Llamamos al método form_valid de la clase base
        response = super().form_valid(form)
        # Agregamos el mensaje de éxito
        messages.success(self.request, "Modificado Correctamente")
        # Retornamos la respuesta
        return response
    
class ProductoEdicion(LoginRequiredMixin,UpdateView):
    model = Product
    template_name = 'inventario/mantenedorProducto.html'
    form_class = ProductForm
    success_url = reverse_lazy('listaProductos', kwargs={'nombre': ''})  # Ajusta la URL según tu configuración de URL

    def form_valid(self, form):
        name_category_value = form.cleaned_data.get('name_category')
        messages.success(self.request, "Modificado Correctamente")
        self.success_url = reverse_lazy('listaProductos', kwargs={'nombre': name_category_value})
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Error al modificar el producto")  # Mensaje de error en caso de formulario no válido
        return super().form_invalid(form)

class ProveedorEdicion(LoginRequiredMixin,UpdateView):
    model=Suppliers
    form_class=SuppliersForm
    template_name='inventario/mantenedorProveedor.html'
    success_url= reverse_lazy('proveedores')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["proveedores"] = Suppliers.objects.all()
        return context
    
   


#METODOS ELIMINAR

class ProductoEliminar(LoginRequiredMixin,DeleteView):
    model=Product
    success_url=reverse_lazy('listarProducto', kwargs={'nombre': ''})

    def form_valid(self,form):
        messages.success(self.request, "Eliminado Correctamente")
        self.success_url = reverse_lazy('listaProductos', kwargs={'nombre': self.object.name_category.name})
        return super().form_valid(form)

class CategoriaEliminar(LoginRequiredMixin,DeleteView):
    model=Category
    success_url=reverse_lazy('categorias')

    def form_valid(self,form):
        messages.success(self.request, "Eliminado Correctamente")
        return super().form_valid(form)

class ProveedorEliminar(LoginRequiredMixin,DeleteView):
    model=Suppliers
    success_url = reverse_lazy('proveedores')

    def form_valid(self,form):
        messages.success(self.request, "Eliminado Correctamente")
        return super().form_valid(form)

