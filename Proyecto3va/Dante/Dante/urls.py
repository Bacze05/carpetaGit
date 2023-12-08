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
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from Inventario import views as inventario 
from Venta import views as venta

urlpatterns = [
    #LOGIN
    path('accounts/', include('django.contrib.auth.urls')),
    path('register/', venta.Register.as_view(), name="register"),
    #INVENTARIO
    #VISTAS GENERALES
    path('admin/', admin.site.urls),
    path('', inventario.Home.as_view(), name="home"),
    path('categorias/', inventario.Categorias.as_view(), name="categorias"),
    path('proveedores/',inventario.ListaProveedores.as_view(), name='proveedores'),
    path('categorias/list/<str:nombre>/', inventario.ListaProductosView.as_view(), name="listaProductos"),
    #Modificar
    path('productos/edit/<int:pk>',inventario.ProductoEdicion.as_view(),name='editarProducto'),
    path('categorias/edit/<int:pk>',inventario.CategoriaEdicion.as_view(),name='editarCategoria'),
    path('proveedor/edit/<int:pk>',inventario.ProveedorEdicion.as_view(),name='editarProveedor'),
    #Eliminar
    path('productos/eliminado/<int:pk>/',inventario.ProductoEliminar.as_view(),name='eliminarProducto'),
    path('categorias/eliminado/<int:pk>/',inventario.CategoriaEliminar.as_view(),name='eliminarCategoria'),
    path('proveedor/eliminado/<int:pk>/',inventario.ProveedorEliminar.as_view(),name='elimminarProveedor'),

    #VENTA
    path('apertura/', venta.AbrirCajaView.as_view(), name="apertura"),
    path('cierre/', venta.CerrarCajaView.as_view(), name="cierre"),
    path('panelVenta/', venta.PanelVenta.as_view(), name="panelVenta"),
    path('listaVenta/', venta.ListaVentaView.as_view(), name="listaVenta"),

    #Prueba
]  

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)