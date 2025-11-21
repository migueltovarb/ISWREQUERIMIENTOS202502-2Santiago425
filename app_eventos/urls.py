from django.urls import path
from . import views

urlpatterns = [
    # LOGIN / DASHBOARD
    path('', views.inicio, name='inicio'),
    path('login/', views.login_usuario, name='login'),
    path('logout/', views.logout_usuario, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),

    # EVENTOS
    path('eventos/', views.eventos_listar, name='eventos_listar'),
    path('eventos/crear/', views.eventos_crear, name='eventos_crear'),
    path('eventos/editar/<int:id>/', views.eventos_editar, name='eventos_editar'),
    path('eventos/eliminar/<int:id>/', views.eventos_eliminar, name='eventos_eliminar'),

    # PARTICIPANTES
    path('participantes/', views.participantes_listar, name='participantes_listar'),
    path('participantes/crear/', views.participantes_crear, name='participantes_crear'),
    path('participantes/editar/<int:id>/', views.participantes_editar, name='participantes_editar'),
    path('participantes/eliminar/<int:id>/', views.participantes_eliminar, name='participantes_eliminar'),

    # REGISTROS
    path('registros/', views.registros_listar, name='registros_listar'),
    path('registros/crear/', views.registros_crear, name='registros_crear'),
    path('registros/eliminar/<int:id>/', views.registros_eliminar, name='registros_eliminar'),

    # NOTIFICACIONES
    path('notificaciones/', views.notificaciones_listar, name='notificaciones_listar'),

    # USUARIOS  🔥🔥🔥 (CORREGIDO)
    path('usuarios/', views.usuarios_listar, name='usuarios_listar'),
    path('usuarios/crear/', views.usuarios_crear, name='usuarios_crear'),
    path('usuarios/eliminar/<int:id>/', views.usuarios_eliminar, name='usuarios_eliminar'),
]
