from django.shortcuts import redirect
from django.contrib.auth import login
from django.views.generic import TemplateView,ListView,FormView
from .forms import CustomUserCreationForm


class Venta(TemplateView):
    template_name='venta/panelVenta.html'





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





   