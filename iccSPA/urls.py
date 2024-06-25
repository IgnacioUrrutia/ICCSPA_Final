#from django.conf.urls import url
from django.urls import path
from . import views




urlpatterns = [
    path('index', views.index, name='index'),
    path('galeria', views.galeria, name='galeria'),
    path('contacto', views.contacto, name='contacto'),
    path('login', views.login, name='login'),
    path('nosotros', views.nosotros, name='nosotros'),
    path('registrarse', views.registrarse, name='registrarse'),

    path('productos/', views.producto_list, name='producto_list'),
    path('productos/<int:pk>', views.producto_detail, name='producto_detail'),
    path('productos/nuevo/', views.producto_create, name='producto_create'),
    path('productos/<int:pk>/editar/', views.producto_update, name='producto_update'),
    path('productos/<int:pk>/borrar/', views.producto_delete, name='producto_delete'),
    
    path('iniciar-sesion/', views.iniciar_sesion, name='iniciar_sesion'),
    path('registrar-cliente/', views.registrar_usuario_cliente, name='registrar_cliente'),
    path('boleta/<int:boleta_id>/', views.detalle_boleta, name='detalle_boleta'),
    
    path('cerrar-sesion/', views.cerrar_sesion, name='cerrar_sesion'),


    path('carrito/agregar/<int:producto_id>/', views.agregar_al_carrito, name='agregar_al_carrito'),
    path('carrito/', views.ver_carrito, name='ver_carrito'),
    path('carrito/comprar/', views.realizar_compra, name='realizar_compra'),
    path('boleta/<int:boleta_id>/', views.detalle_boleta, name='detalle_boleta'),
    path('cambiar_cantidad_carrito/<int:producto_id>/', views.cambiar_cantidad_carrito, name='cambiar_cantidad_carrito'),
    path('eliminar_producto_carrito/<int:producto_id>/', views.eliminar_producto_carrito, name='eliminar_producto_carrito'),
    path('carrito/', views.carrito, name='carrito'),
]
