from django.shortcuts import render
from Venta.models import *
import json 
from django.http import JsonResponse
from inventarioApi.serializer import *
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
# Create your views here.
def UsuarioApi(request):
    usuarios= User.objects.all()
    data = {
        'usuarios':list(
            usuarios.values('pk','username','first_name','last_name','email',)
        )
    }
    return JsonResponse(data)
@api_view(['GET','POST'])
def usuario_listado(request):
    if request.method=='GET':
        usuarios = User.objects.all()
        serializer = UsuariosSerializados(usuarios,many=True)
        return Response(serializer.data)
    
    if request.method == 'POST':
        serializer = UsuariosSerializados(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status= status.HTTP_201_CREATED)
        return Response(serializer.errors,status = status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET','PUT','DELETE'])   
def usuario_detalle(request,pk):
    try:
        usuarios=User.objects.get(id=pk)
    except User.DoesNotExist:
        return Response(status = status.HTTP_404_NOT_FOUND)
    
    if request.method=='GET':
        serializer = UsuariosSerializados(usuarios)
        return Response(serializer.data)
    
    if request.method == 'PUT':
        serializer = UsuariosSerializados(usuarios,data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,status = status.HTTP_404_NOT_FOUND)
    if request.method=='DELETE':
        usuarios.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
@api_view(['GET','POST'])
def productos_listado(request):
    if request.method=='GET':
        productos = Product.objects.all()
        serializer = productosSerializados(productos,many=True)
        return Response(serializer.data)
    
    if request.method == 'POST':
        serializer = productosSerializados(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status= status.HTTP_201_CREATED)
        return Response(serializer.errors,status = status.HTTP_400_BAD_REQUEST)