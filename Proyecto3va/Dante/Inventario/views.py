from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.generic import TemplateView,ListView,FormView,UpdateView, CreateView,DeleteView
from django.urls import reverse_lazy
from Inventario.forms import *
from Inventario.models import *

# Create your views here.
#VISTAS GENERALES PAGINAS PRINCIPALES
class Home(TemplateView):
    template_name='base.html'

class Categorias(ListView):
    model=Category
    template_name='inventario/Categorias.html'
    context_object_name='categorias'

class ListaProveedores(ListView):
    model=Suppliers
    template_name='inventario/proveedores.html'
    context_object_name='proveedores'
    
class ListaProductosView(ListView):
    template_name = 'inventario/listaProductos.html'
    context_object_name = 'productos'  # Nombre de la variable de contexto que contendrá la lista de productos

    def get_queryset(self):
        # Obtener el parámetro de la URL (nombre de la categoría)
        nombre_categoria = self.kwargs['nombre']
        
        # Obtener la categoría correspondiente
        categoria = Category.objects.get(name=nombre_categoria)

        # Filtrar productos por la categoría
        return Product.objects.filter(name_category=categoria)

    def get_context_data(self, **kwargs):
        # Agregar la categoría al contexto
        context = super().get_context_data(**kwargs)
        nombre_categoria = self.kwargs['nombre']
        context['categorias'] = Category.objects.get(name=nombre_categoria)
        return context


#METODOS CREATES
class CategoriaCrear(CreateView):
    model=Category
    template_name='inventario/categoriasAdd.html'
    form_class=CategoryForm
    success_url=reverse_lazy('categorias')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Creado Correctamente")
        return response

class ProductoCrear(CreateView):
    model = Product
    template_name = 'inventario/productosAdd.html'
    form_class = ProductForm
    success_url = reverse_lazy('listaProductos', kwargs={'nombre': ''})  # Ajusta la URL según tu configuración de URL

    def form_valid(self, form):
        # Accede al valor del campo name_category directamente desde el formulario
        name_category_value = form.cleaned_data.get('name_category')
        
        messages.success(self.request, "Producto Creado Correctamente")
        self.success_url = reverse_lazy('listaProductos', kwargs={'nombre': name_category_value})
        
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Error al modificar el producto")  # Mensaje de error en caso de formulario no válido
        return super().form_invalid(form)


class ProveedorCrear(CreateView):
    model=Suppliers
    template_name='inventario/proveedorAdd.html'
    form_class=SuppliersForm
    success_url=reverse_lazy('proveedores')

    def form_valid(self, form):
        messages.success(self.request, "Proveedor Creado Correctamente")
        return super().form_valid(form)
    

#METODOS EDITAR

class CategoriaEdicion(UpdateView):
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
    
class ProductoEdicion(UpdateView):
    model = Product
    template_name = 'inventario/mantenedorProducto.html'
    form_class = ProductForm
    success_url = reverse_lazy('listaProductos', kwargs={'nombre': ''})  # Ajusta la URL según tu configuración de URL

    def form_valid(self, form):
        messages.success(self.request, "Modificado Correctamente")
        self.success_url = reverse_lazy('listaProductos', kwargs={'nombre': self.object.name_category.name})
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Error al modificar el producto")  # Mensaje de error en caso de formulario no válido
        return super().form_invalid(form)

class ProveedorEdicion(UpdateView):
    model=Suppliers
    template_name='inventario/mantenedorProveedor.html'
    form_class=SuppliersForm
    success_url= reverse_lazy('proveedores')

    def form_valid(self, form):
        messages.success(self.request, "Proveedor Modificado Correctamente")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Error al modificar al Proveedor")  # Mensaje de error en caso de formulario no válido
        return super().form_invalid(form)



#METODOS ELIMINAR

class ProductoEliminar(DeleteView):
    model=Product
    success_url=reverse_lazy('listarProducto', kwargs={'nombre': ''})

    def form_valid(self,form):
        messages.success(self.request, "Eliminado Correctamente")
        self.success_url = reverse_lazy('listaProductos', kwargs={'nombre': self.object.name_category.name})
        return super().form_valid(form)



class CategoriaEliminar(DeleteView):
    model=Category
    success_url=reverse_lazy('categorias')

    def form_valid(self,form):
        messages.success(self.request, "Eliminado Correctamente")
        return super().form_valid(form)

class ProveedorEliminar(DeleteView):
    model=Suppliers
    success_url = reverse_lazy('proveedores')

    def form_valid(self,form):
        messages.success(self.request, "Eliminado Correctamente")
        return super().form_valid(form)

