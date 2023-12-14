from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import Group
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.serializers import serialize
from django.views.generic import TemplateView,ListView,UpdateView, CreateView,DeleteView, View
from django.urls import reverse_lazy
from Inventario.forms import *
from Inventario.models import *
from Venta.models import *
from Venta.forms import *
from .mixins import *


#VISTAS GENERALES PAGINAS PRINCIPALES

class Home(TemplateView):
    template_name='base.html'

# Categorias CRUD

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
    
class CategoriaEliminar(LoginRequiredMixin,DeleteView):
    model=Category
    success_url=reverse_lazy('categorias')

    def form_valid(self,form):
        messages.success(self.request, "Eliminado Correctamente")
        return super().form_valid(form)
    
# PROVEEDORES CRUD

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
        
class ProveedorEdicion(LoginRequiredMixin,UpdateView):
    model=Suppliers
    form_class=SuppliersForm
    template_name='inventario/mantenedorProveedor.html'
    success_url= reverse_lazy('proveedores')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["proveedores"] = Suppliers.objects.all()
        return context
    
class ProveedorEliminar(LoginRequiredMixin,DeleteView):
    model=Suppliers
    success_url = reverse_lazy('proveedores')

    def form_valid(self,form):
        messages.success(self.request, "Eliminado Correctamente")
        return super().form_valid(form)

# PRODUCTOS CRUD

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
            context['categorias'] = None  

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
    
class ProductoEdicion(LoginRequiredMixin,UpdateView):
    model = Product
    template_name = 'inventario/mantenedorProducto.html'
    form_class = ProductForm
    success_url = reverse_lazy('listaProductos', kwargs={'nombre': ''})  

    def form_valid(self, form):
        name_category_value = form.cleaned_data.get('name_category')
        messages.success(self.request, "Modificado Correctamente")
        self.success_url = reverse_lazy('listaProductos', kwargs={'nombre': name_category_value})
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Error al modificar el producto")  # Mensaje de error en caso de formulario no válido
        return super().form_invalid(form)
    

class ProductoEliminar(LoginRequiredMixin,DeleteView):
    model=Product
    success_url=reverse_lazy('listarProducto', kwargs={'nombre': ''})

    def form_valid(self,form):
        messages.success(self.request, "Eliminado Correctamente")
        self.success_url = reverse_lazy('listaProductos', kwargs={'nombre': self.object.name_category.name})
        return super().form_valid(form)


# USUARIOS CRUD

class Usuarios(LoginRequiredMixin,View):
    model=User
    form_class= CustomUserCreationForm
    template_name='inventario/UserList.html'

    def get_queryset(self):
        return self.model.objects.filter(is_active=1)
    def get_context_data(self, **kwargs):
        context = {}
        context["usuarios"] = self.get_queryset()
        context["form"] = self.form_class 
        return context
    
    def get(self,request,*args, **kwargs):  
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            data = serialize('json', self.get_queryset())
            return HttpResponse(data, 'application/json')
        else:
            return render(request,self.template_name,self.get_context_data())   
    
    def post(self,request,*args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            return redirect('usuarios')
        else:
            # Si el formulario no es válido, renderiza la página nuevamente con el formulario y los errores
            context = self.get_context_data()
            context['form'] = form  # Agrega el formulario con errores al contexto
            return render(request, self.template_name, context)
        

class UsuarioEdicion(LoginRequiredMixin, UpdateView):
    model = User
    template_name = 'inventario/mantenedorUsuario.html'
    form_class = CustomUserEditForm
    success_url = reverse_lazy('usuarios')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, instance=self.get_object())
        if form.is_valid():
            form.save()
            messages.success(self.request, "Modificado Correctamente")
            return redirect('usuarios')
        else:
            print("Formulario no válido:", form.errors.as_data())
            context = self.get_context_data()
            context['form'] = form
            return render(request, self.template_name, context)
        
class UsuariosDeletes(LoginRequiredMixin,View):
    model=User
    form_class= CustomUserDeletionForm
    template_name='inventario/UserDeleteList.html'
    def get_queryset(self):
        return self.model.objects.filter(is_active=0)
    def get_context_data(self, **kwargs):
        context = {}
        context["usuarios"] = self.get_queryset()
        context["form"] = self.form_class 
        return context
    
    def get(self,request,*args, **kwargs):  
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            data = serialize('json', self.get_queryset())
            return HttpResponse(data, 'application/json')
        else:
            return render(request,self.template_name,self.get_context_data())   
    
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            # Procesar el formulario solo si es válido
            usuario_id = form.cleaned_data.get('usuario_id')
            usuario = get_object_or_404(User, id=usuario_id)
            usuario.delete()
            return redirect('usuariosDelete')
        else:
            # Si el formulario no es válido, renderiza la página nuevamente con el formulario y los errores
            context = self.get_context_data()
            context['form'] = form  # Agrega el formulario con errores al contexto
            return render(request, self.template_name, context)

# FUNCIONES PARA USUARIO
def obtener_nombre_grupo(request, group_id):
    try:
        grupo = Group.objects.get(pk=group_id)
        nombre_grupo = grupo.name
        return JsonResponse({'nombre_grupo': nombre_grupo})
    except Group.DoesNotExist:
        return JsonResponse({'nombre_grupo': 'Grupo no encontrado'}, status=404)

def desactivar_usuario(request, pk):
    usuario = get_object_or_404(User, pk=pk)
    usuario.is_active = False
    usuario.save()

    return redirect('usuariosDelete')

def activar_usuario(request, pk):
    usuario = get_object_or_404(User, pk=pk)
    usuario.is_active = True
    usuario.save()

    return redirect('usuariosDelete')

     


    








