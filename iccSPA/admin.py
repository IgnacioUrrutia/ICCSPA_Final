from django.contrib import admin
from .models import Producto,Categoria, Contacto
from .models import User


admin.site.register(Producto)
admin.site.register(Categoria)
admin.site.register(Contacto)
admin.site.register(User)
