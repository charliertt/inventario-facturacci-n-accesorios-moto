from django.db import models
from django.contrib.auth.models import User
from datetime import datetime, timezone as tz


class MyModel(models.Model):
    created_at = models.DateTimeField(default=datetime.now(tz.utc))

# Create your models here.




class Producto(models.Model):
    id = models.AutoField(primary_key=True)
    valor = models.CharField(max_length=200)
    nombre = models.TextField(max_length=1000)
    stock_talla1 = models.IntegerField(default=0)
    stock_talla2 = models.IntegerField(default=0)
    stock_talla3 = models.IntegerField(default=0)
    stock_talla4 = models.IntegerField(default=0)
    fecha = models.DateTimeField(auto_now_add=False)
    valor_compra = models.CharField(max_length=200)
    subcompras = models.CharField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
          return f"{self.nombre} - {self.stock_talla1} -  {self.stock_talla2} - {self.stock_talla3}  - {self.stock_talla4}- {self.fecha.strftime('%Y-%m-%d %H:%M:%S')}"
      
class registro_ventas(models.Model):
    id = models.AutoField(primary_key=True) 
    nombre= models.TextField(max_length=1000)
    talla= models.TextField(max_length=1000)
    fecha = models.DateTimeField(auto_now_add=True)
    valor_compra = models.CharField(max_length=200)
    cantidad = models.CharField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total = models.CharField(max_length=200)
    
    
    def __str__(self):
          return f"{self.nombre} - {self.talla} -  {self.cantidad} - {self.fecha.strftime('%Y-%m-%d %H:%M:%S')}"
      
class UserProfile(models.Model):
    id = models.AutoField(primary_key=True) 
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    correo = models.EmailField()
    celular = models.CharField(max_length=20)
    fecha = models.DateTimeField(auto_now_add=True)
    
    ROLES = (
        ('U', 'Usuario'),
        ('A', 'Administrador'),
    )
    rol = models.CharField(max_length=1, choices=ROLES, default='U')
    
    
    def __str__(self):
          return f"{self.nombre} - {self.correo}"