from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.conf import settings
# Create your models here.
class Categoria(models.Model):
    nombre=models.CharField(max_length=50)

    def __str__(self):
        return self.nombre

class Producto(models.Model):
    codigo = models.CharField(max_length=10, unique=True)
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    imagen = models.ImageField(upload_to='productos/')
    precio = models.PositiveBigIntegerField()
    stock = models.PositiveBigIntegerField()
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre
    
class Contacto(models.Model):
    nombre = models.CharField(max_length=50)
    apellidoPaterno = models.CharField(max_length=50)
    apellidoMaterno = models.CharField(max_length=50)
    fechaNacimiento = models.DateField()
    celular = models.CharField(
        max_length=15)
    email = models.EmailField()
    motivacion = models.TextField()

    def __str__(self):
        return f"{self.nombre} {self.apellidoPaterno}"
    
#usuarios
class User(AbstractUser):
    es_administrador = models.BooleanField(default=False)

    groups = models.ManyToManyField(
        Group,
        related_name='custom_user_groups',  
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='custom_user_permissions',  
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )

User = get_user_model()

#carrito
class DetalleCompra(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    precio = models.PositiveBigIntegerField()
    total = models.PositiveBigIntegerField(blank=True, null=True)

    def save(self, *args, **kwargs):
        self.total = self.precio * self.cantidad
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.cantidad} x {self.producto.nombre} - ${self.total}"

class BoletaCompra(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    fecha = models.DateTimeField(default=timezone.now)
    estado = models.CharField(max_length=20, default="recibido")
    detalles = models.ManyToManyField('DetalleCompra', related_name='boletas')

    def __str__(self):
        return f"Boleta {self.id} - {self.usuario.username} - {self.fecha}"

    def calcular_total(self):
        total = 0
        for detalle in self.detalles.all():
            total += detalle.total
        return total