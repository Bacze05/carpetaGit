from django.shortcuts import render, redirect
from Inventario.forms import *
from Inventario.models import *


# Create your views here.
def home(request):
    return render(request,"base.html")

def categorias(request):
    categorias=Category.objects.all()
    return render(request,'inventario/Categorias.html',{'categorias':categorias})

def crear_categoria(request):
    if request.method=="POST":
        form=CategoryForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return redirect('categorias')
    else:
        form=CategoryForm()
    return render(request,'inventario/CategoriasAdd.html',{'form':form})

def listaProductos(request, nombre):
    categoria = Category.objects.get(name=nombre)
    productos = Product.objects.filter(name_category=categoria)
    return render(request, 'inventario/listaProductos.html', {'categorias': categoria, 'productos': productos})

# def crear_producto(request):
#     if request.method=="POST":
#         form=ProductForm(request.POST,request.FILES)
#         if form.is_valid():
#             form.save()
#             return redirect('home')
#     else:
#         form=ProductForm()
#     return render(request,'inventario/productosAdd.html',{'form':form})
def crear_producto(request):
    if request.method == "POST":
        form_producto = ProductForm(request.POST, request.FILES)
        form_categoria = CategoryForm(request.POST, request.FILES)
        if form_producto.is_valid():
            producto = form_producto.save(commit=False)
            # Aquí puedes realizar operaciones adicionales con el objeto del producto si es necesario
            producto.save()

            # Si también necesitas guardar la categoría, puedes hacer lo mismo con el formulario de categoría
            if form_categoria.is_valid():
                categoria = form_categoria.save(commit=False)
                # Realiza las operaciones adicionales con el objeto de categoría si es necesario
                categoria.save()

            return redirect('home')
    else:
        form_producto = ProductForm()
        form_categoria = CategoryForm()

    return render(request, 'inventario/productosAdd.html', {'form_producto': form_producto, 'form_categoria': form_categoria})

def crear_proveedor(request):
    if request.method=="POST":
        form=SuppliersForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form=SuppliersForm()
    return render(request,'inventario/proveedorAdd.html',{'form':form})