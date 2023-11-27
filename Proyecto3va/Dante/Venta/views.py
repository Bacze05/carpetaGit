import json 
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.core.serializers import serialize
from django.contrib import messages
from django.contrib.auth import login
from django.views.generic import TemplateView,ListView,FormView
from .forms import CustomUserCreationForm
from Inventario.models import Product





class PanelVenta(TemplateView): 
    template_name = 'venta/panelVenta.html'
    
class ListaVentaView(ListView):
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
    # model = Product
    # context_object_name = 'productos'
    # template_name = 'venta/panelVenta.html'

    # def get_queryset(self):
    #     bar_code = self.request.GET.get('bar_code', '')

    #     if not bar_code.isdigit():
    #         return Product.objects.none()

    #     return Product.objects.filter(bar_code=int(bar_code))

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['bar_code'] = self.request.GET.get('bar_code', '')
    #     return context

    # def render_to_response(self, context, **response_kwargs):
    #     productos_json = [
    #         {
    #             'nombre': producto.name,
    #             'descripcion': producto.name_category.name,  # Accede al nombre de la categoría
    #             'precio': producto.price_sold,
    #             'stock': producto.stock,
    #             'cod_barra': producto.bar_code,
    #             # Agrega otros campos según sea necesario
    #         }
    #         for producto in context['productos']
    #     ]

    #     return JsonResponse(productos_json, safe=False)






class Register(FormView):
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





   