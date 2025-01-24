from django.forms import ModelForm
from .models import Producto
from .models import UserProfile

class ProductoForm(ModelForm):
    class Meta:
        model = Producto
        fields = ['id', 'fecha', 'nombre', 'stock_talla1', 'stock_talla2', 'stock_talla3', 'stock_talla4', 'valor', 'valor_compra']
        
class UserProfileForm(ModelForm):
    class Meta:
        model = UserProfile
        fields = ['nombre', 'apellido', 'correo', 'celular', 'rol']


