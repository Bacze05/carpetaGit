import json 
from django.http import  JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.core.serializers import serialize
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView,ListView,FormView, View
from Inventario.models import Product
from .forms import CustomUserCreationForm
from .models import  *




from django.views import View
from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Venta, DetalleVenta

from django.http import JsonResponse

from django.http import JsonResponse
from django.views import View
from .models import DetalleVenta
from django.db import IntegrityError

class PanelVenta(View):
    template_name = 'venta/panelVenta.html'

    def post(self, request):
        try:
            producto_id = request.POST.get('producto_id')
            venta_id = request.POST.get('venta_id')
            precio = request.POST.get('precio')
            cantidad = request.POST.get('cantidad')
            print(f"producto_id: {producto_id}, venta_id: {venta_id}, precio: {precio}, cantidad: {cantidad}")

             # Creamos una instancia de DetalleVenta y la guárdamos en la base de datos
            detalle_venta = DetalleVenta.objects.create(
            producto_id = producto_id,
            venta_id=venta_id,
            precio=precio,
            cantidad=cantidad,
            )
        except IntegrityError as e:
             print(f"Error al crear DetalleVenta: {e}")

        return redirect('home')
    
    def get(self, request):
        return render(request, self.template_name)

    



    
class ListaVentaView(LoginRequiredMixin,ListView):
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
        productos_json = serialize('json', context['productos'], fields=('name', 'price_sold', 'stock', 'bar_code', 'name_category'))
        productos_data = [item['fields'] for item in json.loads(productos_json)]
        return JsonResponse(productos_data, safe=False)
    
    






class Register(LoginRequiredMixin,FormView):
    template_name = 'registration/register.html'
    form_class = CustomUserCreationForm

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context



class AbrirCajaView(LoginRequiredMixin,View):
    template_name = 'venta/apertura.html'

    def get(self, request, *args, **kwargs):
        usuario_actual = self.get_usuario_actual()

        # Verifica si ya hay una caja abierta
        caja_abierta = Cajas.objects.filter(vendedor=usuario_actual, cerrada=False).exists()

        return render(request, self.template_name, {'turno_abierto': caja_abierta})

    def post(self, request, *args, **kwargs):
        usuario_actual = self.get_usuario_actual()

        # Verifica si ya hay una caja abierta
        caja_abierta = Cajas.objects.filter(vendedor=usuario_actual, cerrada=False).exists()

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



    
class CerrarCajaView(LoginRequiredMixin,View):
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
        caja_abierta = Cajas.objects.filter(vendedor=usuario_actual, cerrada=False).first()
        return caja_abierta


#Codigo de prueba 
from django.contrib.auth import get_user_model
from django.utils import timezone
from .forms import CantidadForm

# class ConfirmarVentaView(View):
#     template_name = 'venta/confirmar_venta.html'
#     form_class = CantidadForm

#     def get(self, request, producto_id=None):
#         producto = None
#         if producto_id:
#             producto = get_object_or_404(Product, pk=producto_id)
#         return render(request, self.template_name, {'producto': producto, 'form': self.form_class(), 'producto_id': producto_id})

#     def post(self, request, producto_id=None):
#         form = self.form_class(request.POST)
#         if form.is_valid():
#             cantidad = form.cleaned_data['cantidad']

#             if producto_id:
#                 producto = get_object_or_404(Product, pk=producto_id)
#                 subtotal = producto.price_sold * cantidad

#                 venta = request.session.get('venta', Venta())
#                 detalle_venta = DetalleVenta(producto=producto, cantidad=cantidad, precio=producto.price_sold, subtotal=subtotal)
#                 venta.detalles.add(detalle_venta)
#                 venta.total_venta += subtotal

#                 request.session['venta'] = venta

#             # Redirige a la misma vista para permitir escanear más productos
#             return redirect('confirmar_venta', producto_id=None)

#         return render(request, self.template_name, {'producto_id': producto_id, 'form': form})

from django.shortcuts import render
from django.http import JsonResponse, HttpResponseRedirect,HttpResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views import View
from .models import Product, Venta, DetalleVenta

    
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


# En la vista de confirmación
class ConfirmarVentaView(View):
    template_name = 'venta/confirmar_venta.html'

    def get(self, request):
        venta_actual_id = request.session.get('venta_actual')
        
        # Verifica si la venta_actual_id es un entero antes de intentar obtener el objeto Venta
        if isinstance(venta_actual_id, int):
            venta_actual = Venta.objects.get(pk=venta_actual_id)
            return render(request, self.template_name, {'venta': venta_actual})
        else:
            # Manejar el caso donde venta_actual_id no es un entero (puede ser None u otro tipo)
            return HttpResponse("Error: No se pudo encontrar la venta actual.")

    def post(self, request):
        venta_actual_id = request.session.get('venta_actual')

        # Verifica si la venta_actual_id es un entero antes de intentar obtener el objeto Venta
        if isinstance(venta_actual_id, int):
            venta_actual = Venta.objects.get(pk=venta_actual_id)

            # Guarda los detalles de la venta en la base de datos
            detalles_venta = request.session.get('detalle_venta', [])

            for detalle_data in detalles_venta:
                producto_id = detalle_data.get('producto_id')
                cantidad = detalle_data.get('cantidad')
                precio = detalle_data.get('precio')

                producto = Product.objects.get(pk=producto_id)

                detalle_venta = DetalleVenta.objects.create(
                    producto=producto,
                    cantidad=cantidad,
                    precio=precio,
                    venta=venta_actual
                )

                venta_actual.detalles.add(detalle_venta)

            venta_actual.calcular_total_venta()
            venta_actual.save()

            # Limpia la sesión
            request.session.pop('venta_actual', None)
            request.session.pop('detalle_venta', None)

            # Redirige a donde sea necesario después de confirmar la venta
            return HttpResponseRedirect(reverse('home'))
        else:
            # Manejar el caso donde venta_actual_id no es un entero (puede ser None u otro tipo)
            return HttpResponse("Error: No se pudo confirmar la venta.")






# class EscanearProductoView(View):
#     template_name = 'venta/escanear_producto.html'

#     def get(self, request):
#         return render(request, self.template_name)

#     def post(self, request):
#         if request.method == 'POST':
#             codigo_barras = request.POST.get('codigo_barras')
#             producto = get_object_or_404(Product, bar_code=codigo_barras)

#             venta = Venta.objects.create()  # Crea una nueva venta

#             detalle_venta = DetalleVenta.objects.create(
#                 producto=producto,
#                 cantidad=1,
#                 precio=producto.price_sold,
#                 venta=venta
#             )

#             if producto.stock > 0:
#                 venta.detalles.add(detalle_venta)
#                 venta.save()
#                 producto.stock -= 1
#                 producto.save()

#                 return JsonResponse({'status': 'OK', 'producto_nombre': producto.name, 'subtotal': detalle_venta.calcular_subtotal()})
#             else:
#                 return JsonResponse({'status': 'Error', 'message': 'Producto sin stock'}, status=400)

#         return JsonResponse({'status': 'Error'}, status=400)