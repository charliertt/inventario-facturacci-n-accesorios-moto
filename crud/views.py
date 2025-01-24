from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from .models import UserProfile
from .models import Producto
from .models import registro_ventas
from .forms import UserProfileForm
from .forms import ProductoForm
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.db.models import Sum
from django.db.models import Q
from django.contrib.auth.models import User

# Obtén la suma de todos los valores en la columna 'valor'





def login_vista(request):
   if request.method == 'GET':
        return render(request, 'login.html', {"form": AuthenticationForm})
   else:
        user = authenticate(
            request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'HTML/auth-login.html', {"form": AuthenticationForm, "error": "Usuario o Contraseña incorrectos."})

        login(request, user)
        return redirect('index')
@login_required        
def index(request):
        usuarios = UserProfile.objects.all()
        Registro_ventas=registro_ventas.objects.all()
        
        total_tallas_cero = 0
        productos = Producto.objects.all()
        productos_agotados = []
        

        for producto in productos:
            if producto.stock_talla1 == 0:
                total_tallas_cero += 1
                productos_agotados.append({"id": producto.id, "nombre": producto.nombre, "talla": "S"}) 
                print("Producto con talla 1 en 0: ", producto.nombre)
            if producto.stock_talla2 == 0:
                total_tallas_cero += 1
                productos_agotados.append({"id": producto.id, "nombre": producto.nombre, "talla": "M"})
                
                print("Producto con talla 2 en 0: ", producto.nombre)
            if producto.stock_talla3 == 0:
                total_tallas_cero += 1
                print("Producto con talla 3 en 0: ", producto.nombre)
            if producto.stock_talla4 == 0:
                productos_agotados.append({"id": producto.id, "nombre": producto.nombre, "talla": "L"})              
                total_tallas_cero += 1
                print("Producto con talla 4 en 0: ", producto.nombre)
                productos_agotados.append({"id": producto.id, "nombre": producto.nombre, "talla": "XL"})
                
            print("agotados",productos_agotados)
                
                
    
        print("Total de tallas en 0: ", total_tallas_cero)

        

      
        suma_total = Producto.objects.aggregate(
        valor_total=Sum('valor'),
        subcompras_total=Sum('subcompras'),
        valor_compra_total=Sum('valor_compra')
        )

     

    # Ahora puedes acceder a cada suma total individualmente
        valor_total = suma_total['valor_total']
        subcompras_total = suma_total['subcompras_total']
        valor_compra_total = suma_total['valor_compra_total']
        neto=valor_compra_total-valor_total
        netoCU=neto/2

        return render(request, 'HTML/index.html', {
            "form": ProductoForm,
            "productos": productos,
            "valor_total": valor_total,
            "subcompras_total": subcompras_total,
            "valor_compra_total": valor_compra_total,
            "neto": neto, 
            "netoCU":netoCU, 
            "total_tallas_cero": total_tallas_cero,
            "usuarios": usuarios,
            "productos_agotados": productos_agotados,
             "Registro_ventas": Registro_ventas,
        })      
        
def crear_usuario(request):
    if request.method == "POST":
        try:                 
            username = request.POST['username']
            password = request.POST['password']
            nombre = request.POST['nombre']
            apellido = request.POST['apellido']
            correo = request.POST['correo']
            celular = request.POST['celular']
            rol = request.POST['rol']

            # Comprueba si el nombre de usuario ya existe
            if User.objects.filter(username=username).exists():
                messages.error(request, 'El nombre de usuario ya existe.')
                return redirect('index')
            else:
                user = User.objects.create_user(username=username, password=password)
                UserProfile.objects.create(user=user, nombre=nombre, apellido=apellido, correo=correo, celular=celular, rol=rol)
               
                messages.success(request, 'Usuario Registrado Correctamente')
                return redirect('index')
                        
        except ValueError as e:
            messages.error(request, str(e))
            return redirect('index')






def registro(request):
        if request.method == "POST":
            try: 
                form = ProductoForm(request.POST)
                print(form)
                nuevo_producto = form.save(commit=False)
                nuevo_producto.user = request.user
                nuevo_producto.subcompras = str(int(nuevo_producto.valor_compra) * (nuevo_producto.stock_talla1 + nuevo_producto.stock_talla2 + nuevo_producto.stock_talla3 + nuevo_producto.stock_talla4))
                nuevo_producto.save()
                messages.success(request, 'Producto Agregado Correctamente')
            except ValueError:
                return render(request, 'HTML/registro.html', {"form": ProductoForm, "error": "Error creating producto."})  
    # Si es una solicitud POST o GET, obtén todos los productos después de agregar o editar
        productos = Producto.objects.all()
        total_tallas_cero=0
     
        for producto in productos:
            if producto.stock_talla1 == 0:
                 total_tallas_cero += 1
            if producto.stock_talla2 == 0:
                total_tallas_cero += 1 
            if producto.stock_talla3 == 0:
                total_tallas_cero += 1
            if producto.stock_talla4 == 0:
                total_tallas_cero += 1
                
        suma_total = Producto.objects.aggregate(
        valor_total=Sum('valor'),
        subcompras_total=Sum('subcompras'),
        valor_compra_total=Sum('valor_compra')
        )

    # Ahora puedes acceder a cada suma total individualmente
        valor_total = suma_total['valor_total']
        subcompras_total = suma_total['subcompras_total']
        valor_compra_total = suma_total['valor_compra_total']
        neto=valor_compra_total-valor_total
        netoCU=neto/2
        

        return render(request, 'HTML/registro.html', {
            "form": ProductoForm,
            "productos": productos,
            "valor_total": valor_total,
            "subcompras_total": subcompras_total,
            "valor_compra_total": valor_compra_total,
            "neto": neto, 
            "netoCU":netoCU, 
            "total_tallas_cero": total_tallas_cero,
           
        })
       
        
        

def editar_datos(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)

    if request.method == 'POST':
        form = ProductoForm(request.POST, instance=producto)
        if form.is_valid():
            producto = form.save()  # Esto devuelve una instancia del modelo Producto
            producto.subcompras = str(int(producto.valor_compra) * (producto.stock_talla1 + producto.stock_talla2 + producto.stock_talla3 + producto.stock_talla4))
            producto.save()
            messages.success(request, 'Producto editado Correctamente')
            return redirect('registro')

        
def editar_usuario(request, user_id):
    usuario = get_object_or_404(UserProfile, id=user_id)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=usuario)
        
        
        if form.is_valid():
            form.save()
            messages.success(request, 'Usuario editado correctamente')
            return redirect('index')

    else:
        form = UserProfileForm(instance=usuario)

    return render(request, 'HTML/index.html', {'form': form, 'usuario': usuario})

@require_POST
def borrar_usuario(request, user_id):
    usuario = get_object_or_404(UserProfile, id=user_id)
    usuario.delete()
    messages.success(request, 'Usuario eliminado Correctamente')
    return redirect('index')



@csrf_exempt
def ventas(request):
       
        if request.method == 'POST':
                # Los datos enviados a través de FormData son accesibles a través de request.POST
                carrito = json.loads(request.POST.get('carrito'))
                subtotal_global = request.POST.get('subtotal_global')
    # Aquí puedes procesar los datos...
                for clave, producto in carrito.items():
                    id, talla = clave.split('-')
                    cantidad_comprada = producto['cantidad']

                    # Obtén el producto de la base de datos
                    producto_db = Producto.objects.get(id=id)
                    
                    
                    

                    # Resta la cantidad comprada al stock de la talla correspondiente
                    if talla == 'S':
                        producto_db.stock_talla1 -= cantidad_comprada
                    elif talla == 'M':
                        producto_db.stock_talla2 -= cantidad_comprada
                    elif talla == 'L':
                        producto_db.stock_talla3 -= cantidad_comprada
                    elif talla == 'XL':
                        producto_db.stock_talla4 -= cantidad_comprada
                        
                        
                    print(carrito)
                    

                    
                    producto_db.save()
                    registro_venta = registro_ventas(
                    nombre=producto['nombre'],
                    talla=talla,
                    valor_compra=producto['valor'],
                    total=producto['total'],
                    cantidad=cantidad_comprada,
                    user=request.user  # Asegúrate de que el usuario esté autenticado
                    )
                    registro_venta.save()
                    print(carrito)
                    print(subtotal_global)
                

                return JsonResponse({'message': 'Datos recibidos correctamente'})
            # Aquí puedes procesar los datos...
      
        else:
           
            productos = Producto.objects.all()
            total_tallas_cero=0
     
            for producto in productos:
                if producto.stock_talla1 == 0:
                    total_tallas_cero += 1
                if producto.stock_talla2 == 0:
                    total_tallas_cero += 1
                if producto.stock_talla3 == 0:
                    total_tallas_cero += 1
                if producto.stock_talla4 == 0:
                    total_tallas_cero += 1
            suma_total = Producto.objects.aggregate(
            valor_total=Sum('valor'),
            subcompras_total=Sum('subcompras'),
            valor_compra_total=Sum('valor_compra')
                    )

                # Ahora puedes acceder a cada suma total individualmente
            valor_total = suma_total['valor_total']
            subcompras_total = suma_total['subcompras_total']
            valor_compra_total = suma_total['valor_compra_total']
            neto=valor_compra_total-valor_total
            netoCU=neto/2
            return render(request, 'HTML/ventas.html', {"productos": productos,
                                                        "valor_total": valor_total,
                                                        "subcompras_total": subcompras_total,
                                                        "valor_compra_total": valor_compra_total,
                                                        "neto": neto, 
                                                        "netoCU":netoCU, 
                                                        "total_tallas_cero": total_tallas_cero,
                                                        })
        
 
        
    

@require_POST
def borrar_datos(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    producto.delete()
    messages.success(request, 'Producto eliminado Correctamente')
   
    return redirect('registro')


def cerrar_sesion(request):
       logout(request)
       return redirect('login_vista')




    
   
   
  
   
    


                
        
    


    

# Create your views here.
