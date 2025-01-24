from django.contrib import admin
from .models import Producto
from .models import registro_ventas
from .models import UserProfile



admin.site.register(Producto)
admin.site.register(registro_ventas)
admin.site.register(UserProfile)

# Register your models here.
