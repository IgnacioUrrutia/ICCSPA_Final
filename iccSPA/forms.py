from django import forms
from .models import Producto
from .models import Contacto
from .models import User
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['codigo', 'nombre', 'descripcion', 'imagen', 'precio', 'stock', 'categoria']

class ContactoForm(forms.ModelForm):
    fechaNacimiento = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        input_formats=['%Y-%m-%d']
    )

    class Meta:
        model = Contacto
        fields = ['nombre', 'apellidoPaterno', 'apellidoMaterno', 'fechaNacimiento', 'celular', 'email', 'motivacion']

    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre')
        if not nombre.isalpha():
            raise ValidationError("El nombre debe contener solo letras.")
        return nombre

    def clean_apellidoPaterno(self):
        apellido = self.cleaned_data.get('apellidoPaterno')
        if not apellido.isalpha():
            raise ValidationError("El apellido paterno debe contener solo letras.")
        return apellido

    def clean_apellidoMaterno(self):
        apellido = self.cleaned_data.get('apellidoMaterno')
        if not apellido.isalpha():
            raise ValidationError("El apellido materno debe contener solo letras.")
        return apellido

    def clean_celular(self):
        celular = self.cleaned_data.get('celular')
        if not celular.isdigit():
            raise ValidationError("El número de celular debe contener solo dígitos.")
        return celular
    
class RegistroClienteForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Este correo electrónico ya está en uso.")
        return email

