"""
URL configuration for Dante project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from Inventario import views as inventario 
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    #INVENTARIO
    #VISTAS GENERALES
    path('admin/', admin.site.urls),
    path('', inventario.home, name="home"),
    path('categorias/', inventario.categorias, name="categorias"),
    path('proveedores/',inventario.listaProveedores, name='proveedores'),
    path('categorias/list/<str:nombre>/', inventario.listaProductos, name="listaProductos"),
    #Creacion
    path('categorias/add/', inventario.crear_categoria, name="crearCategorias"),
    path('productos/Add/',inventario.crear_producto,name='crearProducto'),
    path('proveedor/Add/',inventario.crear_proveedor,name='crearProveedor'),
    #Modificar
    path('productos/edit/<int:producto_id>',inventario.editar_producto,name='editarProducto'),
    path('categorias/edit/<int:categoria_id>',inventario.editar_categoria,name='editarCategoria'),
    path('proveedor/edit/<int:proveedor_id>',inventario.editar_proveedor,name='editarProveedor'),
    #Eliminar
    path('productos/eliminado/<int:id>/',inventario.eliminar_producto,name='eliminarProducto'),
    path('categorias/eliminado/<int:id>/',inventario.eliminar_categoria,name='eliminarCategoria'),
    path('proveedor/eliminado/<int:id>/',inventario.eliminar_proveedor,name='elimminarProveedor'),

    #VENTA
    
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)