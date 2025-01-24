"""inventario_cascos URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from crud import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name="index"),
    path('crear_usuario/', views.crear_usuario, name="crear_usuario"),
    path('editar_usuario/<int:user_id>/', views.editar_usuario, name='editar_usuario'),
    path('borrar_usuario/<int:user_id>/', views.borrar_usuario, name='borrar_usuario'),
    path('login_vista/', views.login_vista, name="login_vista"),
    path('cerrar_sesion/', views.cerrar_sesion, name="cerrar_sesion"),
    path('registro/', views.registro, name="registro"),
    path('registro/editar_datos/<int:producto_id>/', views.editar_datos, name="editar_datos"),
    path('registro/borrar_datos/<int:producto_id>/', views.borrar_datos, name="borrar_datos"),
    path('ventas/', views.ventas, name="ventas")
      
      
    
 
   
]
