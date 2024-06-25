
from django.shortcuts import render, get_object_or_404, redirect
from .models import Producto, DetalleCompra, BoletaCompra
from .forms import ProductoForm, ContactoForm, RegistroClienteForm
from django.contrib import messages
from django.contrib.auth import authenticate,login as auth_login
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib.auth import logout
from django.contrib.auth.decorators import user_passes_test
# Create your views here.


def index(request):
    context={}
    return render(request, 'iccSPA/index.html', context)

def galeria(request):
    productos=Producto.objects.all()
    return render(request, 'iccSPA/galeria.html', {'productos':productos})

def contacto(request):
    context={}
    return render(request, 'iccSPA/contacto.html', context)

def login(request):
    context={}
    return render(request, 'iccSPA/login.html', context)

def nosotros(request):
    context={}
    return render(request, 'iccSPA/nosotros.html', context)

def registrarse(request):
    context={}
    return render(request, 'iccSPA/registrarse.html', context)



def es_administrador(user):
    return user.is_authenticated and (user.is_staff or user.is_superuser)

#lista de productos
@user_passes_test(es_administrador, login_url='iniciar_sesion')
def producto_list(request):
    productos = Producto.objects.all()
    return render(request, 'iccSPA/producto_list.html', {'productos': productos})

#detalle de producto
def producto_detail(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    return render(request, 'iccSPA/producto_detail.html', {'producto': producto})

#crear producto
def producto_create(request):
    if request.method=='POST':
        form= ProductoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('producto_list')
    else:
        form= ProductoForm()
    return render(request, 'iccSPA/producto_form.html', {'form': form})

#actualizar producto existente 
def producto_update(request, pk):
    producto= get_object_or_404(Producto, pk=pk)
    if request.method=='POST':
        form= ProductoForm(request.POST, request.FILES, instance=producto)
        if form.is_valid():
            form.save()
            return redirect('producto_list')
    else:
        form= ProductoForm(instance=producto)
    return render(request, 'iccSPA/producto_form.html', {'form':form})

#eliminar un producto
def producto_delete(request, pk):
    producto= get_object_or_404(Producto, pk=pk)
    if request.method=='POST':
        producto.delete()
        return redirect('producto_list')
    return render(request, 'iccSPA/producto_confirm_delete.html', {'producto':producto})

#formulario contacto
def contacto(request):
    if request.method == 'POST':
        form = ContactoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Formulario enviado correctamente.')
            return redirect('nosotros')
        else:
            messages.error(request, 'Por favor, corrige los errores en el formulario.')
    else:
        form = ContactoForm()
    return render(request, 'iccSPA/contacto.html', {'form': form})

#Usuarios,login,logout

def iniciar_sesion(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            auth_login(request, user)
            if user.is_staff or user.is_superuser:
                return redirect('producto_list')
            else:
                return redirect('galeria')
        else:
            messages.error(request, 'Nombre de usuario o contraseña incorrectos.')
    else:
        next_url = request.GET.get('next')
        if next_url and 'producto_list' in next_url:
            messages.warning(request, "Para acceder al inventario, inicie sesión con una cuenta de administrador.")
    
    return render(request, 'usuarios/iniciar_sesion.html')

def cerrar_sesion(request):
    logout(request)
    messages.success(request,("Has cerrado sesion"))
    return redirect('index')

def registrar_usuario_cliente(request):
    if request.method == 'POST':
        form = RegistroClienteForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect('iniciar_sesion')
    else:
        form = RegistroClienteForm()

    return render(request, 'usuarios/registrar_cliente.html', {'form': form})

#carrito de compras
def carrito(request):
    return render(request, 'carrito.html')
@login_required
def agregar_al_carrito(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    cantidad = int(request.POST.get('cantidad', 1))
    
    if 'carrito' not in request.session:
        request.session['carrito'] = []
    
    carrito = request.session['carrito']
    for item in carrito:
        if item['producto_id'] == producto.id:
            item['cantidad'] += cantidad
            break
    else:
        carrito.append({
            'producto_id': producto.id,
            'cantidad': cantidad,
            'precio': producto.precio
        })
    
    request.session['carrito'] = carrito
    messages.success(request, f"Se agregó {producto.nombre} al carrito.")
    return redirect('galeria')

@login_required
def ver_carrito(request):
    carrito = request.session.get('carrito', [])
    productos = []
    total = 0
    for item in carrito:
        producto = get_object_or_404(Producto, id=item['producto_id'])
        item_total = producto.precio * item['cantidad']
        productos.append({
            'producto': producto,
            'cantidad': item['cantidad'],
            'precio': item['precio'],
            'total': item_total
        })
        total += item_total
    return render(request, 'iccSPA/carrito.html', {'productos': productos, 'total': total})

@login_required
def realizar_compra(request):
    carrito = request.session.get('carrito', [])
    if not carrito:
        messages.error(request, "Tu carrito está vacío.")
        return redirect('galeria')

    boleta = BoletaCompra.objects.create(usuario=request.user)
    for item in carrito:
        producto = get_object_or_404(Producto, id=item['producto_id'])
        if producto.stock < item['cantidad']:
            messages.error(request, f"No hay suficiente stock para {producto.nombre}.")
            return redirect('ver_carrito')
        producto.stock -= item['cantidad']
        producto.save()

        detalle = DetalleCompra(
            producto=producto,
            cantidad=item['cantidad'],
            precio=producto.precio
        )
        detalle.save()  # Esto activará el método save() en DetalleCompra para calcular y guardar el campo total
        boleta.detalles.add(detalle)

    boleta.save()
    del request.session['carrito']
    messages.success(request, "Compra realizada con éxito.")
    return redirect('detalle_boleta', boleta_id=boleta.id)

@login_required
def detalle_boleta(request, boleta_id):
    boleta = get_object_or_404(BoletaCompra, id=boleta_id)
    return render(request, 'iccSPA/detalle_boleta.html', {'boleta': boleta})

@login_required
def eliminar_producto_carrito(request, producto_id):
    carrito = request.session.get('carrito', [])

    for item in carrito:
        if item['producto_id'] == producto_id:
            carrito.remove(item)
            break

    request.session['carrito'] = carrito
    messages.success(request, "Producto eliminado del carrito.")
    return redirect('ver_carrito')

@login_required
def cambiar_cantidad_carrito(request, producto_id):
    if request.method == 'POST':
        carrito = request.session.get('carrito', [])

        nueva_cantidad = int(request.POST.get('cantidad'))

        for item in carrito:
            if item['producto_id'] == producto_id:
                item['cantidad'] = nueva_cantidad
                break

        request.session['carrito'] = carrito
        messages.success(request, "Cantidad actualizada en el carrito.")
        return redirect('ver_carrito')

    else:
        return redirect('ver_carrito')

def cerrar_sesion(request):
    logout(request)
    messages.success(request,("Has cerrado sesion"))
    return redirect('index')