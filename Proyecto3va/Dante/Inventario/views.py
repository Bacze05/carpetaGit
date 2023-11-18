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