from django.shortcuts import render,redirect
from .forms import CustomUserCreationForm
from django.contrib.auth import authenticate,login

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import CustomUserCreationForm

def register(request):
    data = {'form': CustomUserCreationForm()}

    if request.method == 'POST':
        user_creation_form = CustomUserCreationForm(data=request.POST)

        if user_creation_form.is_valid():
            user = user_creation_form.save()  # El usuario ya está disponible después de guardar el formulario
            login(request, user)
            return redirect('home')
        else:
            # Si hay errores en el formulario, puedes manejarlos aquí y pasarlos al contexto de la plantilla
            data['form'] = user_creation_form

    return render(request, 'registration/register.html', data)

