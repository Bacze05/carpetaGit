from django.shortcuts import render, redirect, get_object_or_404
from Inventario.forms import *
from Inventario.models import *
from django.contrib import messages


# Create your views here.
#VISTAS GENERALES PAGINAS PRINCIPALES
def home(request):
    return render(request,"base.html")

def categorias(request):
    categorias=Category.objects.all()
    return render(request,'inventario/Categorias.html',{'categorias':categorias})

def listaProductos(request, nombre):
    categoria = Category.objects.get(name=nombre)
    productos = Product.objects.filter(name_category=categoria)
    return render(request, 'inventario/listaProductos.html', {'categorias': categoria, 'productos': productos})

def listaProveedores(request):
    proveedores = Suppliers.objects.all()
   
    return render(request, 'inventario/proveedores.html',{'proveedores': proveedores})



#METODOS CREATES

def crear_categoria(request):
    if request.method=="POST":
        form=CategoryForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request,"Creado Correctamente")
            return redirect('categorias')
    else:
        form=CategoryForm()
    return render(request,'inventario/CategoriasAdd.html',{'form':form})

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
        if form_producto.is_valid():
            producto = form_producto.save(commit=False)
            
            # Guarda el producto y obtén la categoría asociada
            producto.save()

            # Asumo que el campo que almacena la categoría se llama 'name_category'
            nombre_categoria = producto.name_category.name
            
            # Redirige a la página de la lista de productos de la categoría asociada
            return redirect('listaProductos', nombre=nombre_categoria)
    else:
        form_producto = ProductForm()

    return render(request, 'inventario/productosAdd.html', {'form_producto': form_producto})

def crear_proveedor(request):
    if request.method=="POST":
        form=SuppliersForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request,"Creado Correctamente")
            return redirect('proveedores')
    else:
        form=SuppliersForm()
    return render(request,'inventario/proveedorAdd.html',{'form':form})


#METODOS EDITAR

def editar_categoria(request,categoria_id):
     categoria = get_object_or_404(Category, id=categoria_id)
    
     if request.method == "POST":
        form = CategoryForm(request.POST, request.FILES, instance=categoria)
        if form.is_valid():
            form.save()
            messages.success(request,"Modificado Correctamente")
            return redirect('categorias')
     else:
        form = CategoryForm(instance=categoria)
    
     return render(request, 'inventario/mantenedorCategoria.html', {'form': form})

def editar_producto(request,producto_id):
     producto = get_object_or_404(Product, id=producto_id)
    
     if request.method == "POST":
        form = ProductForm(request.POST, request.FILES, instance=producto)
        if form.is_valid():
            form.save()
            messages.success(request,"Modificado Correctamente")

            return redirect('listaProductos', nombre=producto.name_category.name)
     else:
        form = ProductForm(instance=producto)
    
     return render(request, 'inventario/mantenedorProducto.html', {'form': form})

def editar_proveedor(request,proveedor_id):
     proveedor = get_object_or_404(Suppliers, id=proveedor_id)
    
     if request.method == "POST":
        form = SuppliersForm(request.POST, request.FILES, instance=proveedor)
        if form.is_valid():
            form.save()
            messages.success(request,"Modificado Correctamente")
            return redirect('proveedores')
     else:
        form = SuppliersForm(instance=proveedor)
    
     return render(request, 'inventario/mantenedorProveedor.html', {'form': form})


#METODOS ELIMINAR

def eliminar_producto(request, id):
    producto = get_object_or_404(Product, id=id)

    # Obtener la imagen asociada al producto (si existe)
    
    producto.delete()
    messages.success(request,"Eliminado correctamente")
    # Obtener la URL referer (página anterior)
    redirect_url = request.META.get('HTTP_REFERER', '/')

    return redirect(redirect_url)

def eliminar_categoria(request, id):
    categoria = get_object_or_404(Category, id=id)

    # Obtener la imagen asociada al producto (si existe)
    
    categoria.delete()
    messages.success(request,"Eliminado correctamente")
    # Obtener la URL referer (página anterior)
    

    return redirect('categorias')

def eliminar_proveedor(request, id):
    proveedor = get_object_or_404(Suppliers, id=id)

    # Obtener la imagen asociada al producto (si existe)
    
    proveedor.delete()
    messages.success(request,"Eliminado correctamente")
    # Obtener la URL referer (página anterior)
    

    return redirect('proveedores')
