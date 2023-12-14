import json
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from django.db import IntegrityError
from django.urls import reverse
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.core.serializers import serialize
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, ListView, FormView, View
from .forms import CustomUserCreationForm, DetalleVentaForm
from Inventario.models import Product
from .models import *




from django.views.decorators.http import require_POST

# class PanelVenta(View):
#     template_name = 'venta/panelVenta.html'

#     def get(self, request):
#         return render(request, self.template_name)
#     @staticmethod
#     def post(request):
#         if request.method == 'POST':
#             formulario = DetalleVentaForm(request.POST)
#             if formulario.is_valid():
#                 detalle_venta = formulario.save()
#                 detalle_venta.save()
#                 return JsonResponse({'mensaje': 'Detalle de venta creado con éxito'})
#             else:
#                 errores = formulario.errors
#                 return JsonResponse({'errores': errores}, status=400)
#         else:
#             # La solicitud no es POST, puedes manejarla según tus necesidades
#             return HttpResponse('Esta vista solo acepta solicitudes POST.', status=405)
from django.views import View
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from .forms import DetalleVentaForm

class PanelVenta(View):
    template_name = 'venta/panelVenta.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        if request.method == 'POST':
            formulario = DetalleVentaForm(request.POST)
            if formulario.is_valid():
                detalle_venta = formulario.save(commit=False)
                
                # Restar 1 al stock del producto
                detalle_venta.producto.stock -= 1
                detalle_venta.producto.save()

                detalle_venta.save()
                return JsonResponse({'mensaje': 'Detalle de venta creado con éxito'})
            else:
                errores = formulario.errors
                return JsonResponse({'errores': errores}, status=400)
        else:
            # La solicitud no es POST, puedes manejarla según tus necesidades
            return HttpResponse('Esta vista solo acepta solicitudes POST.', status=405)

        





class ListaVentaView(LoginRequiredMixin, ListView):
    model = Product
    context_object_name = 'productos'
    template_name = 'venta/panelVenta.html'

    def get_queryset(self):
        bar_code = self.request.GET.get('bar_code', '')

        # Verifica si bar_code es un número antes de realizar la consulta
        if bar_code.isdigit():
            return Product.objects.filter(bar_code=int(bar_code))
        else:
            # No devuelvas datos si bar_code no es un número
            return Product.objects.none()

    def render_to_response(self, context, **response_kwargs):
        productos_json = serialize('json', context['productos'], fields=(
            'id', 'name', 'price_sold', 'stock', 'bar_code', 'name_category'))
        productos_data = [item['fields']
                          for item in json.loads(productos_json)]

        # Agrega el ID del producto a cada elemento en la lista
        for i, producto in enumerate(productos_data):
            producto['id'] = context['productos'][i].id

        return JsonResponse(productos_data, safe=False)
    
   


    

        





class AbrirCajaView(LoginRequiredMixin, View):
    template_name = 'venta/apertura.html'

    def get(self, request, *args, **kwargs):
        usuario_actual = self.get_usuario_actual()

        # Verifica si ya hay una caja abierta
        caja_abierta = Cajas.objects.filter(
            vendedor=usuario_actual, cerrada=False).exists()

        return render(request, self.template_name, {'turno_abierto': caja_abierta})

    def post(self, request, *args, **kwargs):
        usuario_actual = self.get_usuario_actual()

        # Verifica si ya hay una caja abierta
        caja_abierta = Cajas.objects.filter(
            vendedor=usuario_actual, cerrada=False).exists()

        if not caja_abierta:
            # Si no hay una caja abierta, crea una nueva
            nueva_caja = Cajas(vendedor=usuario_actual, cerrada=False)
            nueva_caja.save()
            messages.success(self.request, 'Caja abierta', 'success')
        else:
            # Si ya hay una caja abierta, muestra un mensaje o realiza la acción adecuada
            messages.error(self.request, 'La caja ya está abierta', 'error')

        return redirect('panelVenta')

    def get_usuario_actual(self):
        if hasattr(self.request.user, 'profile'):
            return self.request.user.profile.user
        else:
            return self.request.user


class CerrarCajaView(LoginRequiredMixin, View):
    template_name = 'venta/cierre.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, context={})

    def post(self, request, *args, **kwargs):
        caja_usuario = self.get_caja_abierta()

        if caja_usuario:
            caja_usuario.cerrar_caja()
            messages.success(self.request, 'Caja cerrada', 'success')
        else:
            messages.success(self.request, 'No hay caja abierta', 'error')

        return redirect('panelVenta')

    def get_usuario_actual(self):
        if hasattr(self.request.user, 'profile'):
            return self.request.user.profile.user
        else:
            return self.request.user

    def get_caja_abierta(self):
        usuario_actual = self.get_usuario_actual()
        caja_abierta = Cajas.objects.filter(
            vendedor=usuario_actual, cerrada=False).first()
        return caja_abierta


# En la vista de escaneo
class EscanearProductoView(View):
    template_name = 'venta/escanear_producto.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        if request.method == 'POST':
            codigo_barras = request.POST.get('codigo_barras')
            producto = get_object_or_404(Product, bar_code=codigo_barras)

            # Recupera la venta actual del usuario desde la sesión
            venta_actual_id = request.session.get('venta_actual')

            # Si no hay venta actual, crea una nueva
            if not venta_actual_id:
                venta_actual = Venta.objects.create()
                request.session['venta_actual'] = venta_actual.id
            else:
                venta_actual = Venta.objects.get(pk=venta_actual_id)

            detalle_venta = DetalleVenta(
                producto=producto,
                cantidad=1,
                precio=producto.price_sold,
                venta=venta_actual
            )

            if producto.stock > 0:
                detalle_venta.save()
                venta_actual.detalles.add(detalle_venta)
                venta_actual.save()
                producto.stock -= 1
                producto.save()

                # Convierte los detalles a un formato serializable
                detalles_serializable = list(venta_actual.detalles.values())

                return JsonResponse({
                    'status': 'OK',
                    'message': 'Producto escaneado correctamente.',
                    'producto_nombre': producto.name,
                    'subtotal': detalle_venta.calcular_subtotal(),
                    'detalles': detalles_serializable
                })

            else:
                return JsonResponse({'status': 'Error', 'message': 'Producto sin stock'}, status=400)

        return JsonResponse({'status': 'Error', 'message': 'Método no permitido'}, status=400)
