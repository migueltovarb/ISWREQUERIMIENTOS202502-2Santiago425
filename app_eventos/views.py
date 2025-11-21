from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from .models import (
    Auditoria, Notificacion, Evento, Participante,
    Registro, Pago, Recordatorio, ReporteAsistencia
)

# =====================================================
# HELPERS (Auditoría + Notificaciones)
# =====================================================

def registrar_accion(usuario, accion):
    if usuario and usuario.is_authenticated:
        Auditoria.objects.create(usuario=usuario, accion=accion)


def crear_notificacion(usuario, mensaje):
    if usuario and usuario.is_authenticated:
        Notificacion.objects.create(usuario=usuario, mensaje=mensaje)


# =====================================================
# AUTENTICACIÓN
# =====================================================

def inicio(request):
    return render(request, 'inicio.html')


def login_usuario(request):
    if request.method == 'POST':
        usuario = request.POST['usuario']
        contraseña = request.POST['contraseña']
        user = authenticate(request, username=usuario, password=contraseña)

        if user:
            login(request, user)
            registrar_accion(user, "Inició sesión en la plataforma")
            crear_notificacion(user, "Has iniciado sesión correctamente.")
            return redirect('dashboard')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos')
            return redirect('login')

    return render(request, 'login.html')


def logout_usuario(request):
    if request.user.is_authenticated:
        registrar_accion(request.user, "Cerró sesión en la plataforma")
    logout(request)
    return redirect('login')


# =====================================================
# DASHBOARD
# =====================================================

@login_required
def dashboard(request):
    total_eventos = Evento.objects.count()
    total_participantes = Participante.objects.count()
    total_registros = Registro.objects.count()
    ultimas_acciones = Auditoria.objects.order_by('-fecha')[:5]

    return render(request, 'dashboard.html', {
        'total_eventos': total_eventos,
        'total_participantes': total_participantes,
        'total_registros': total_registros,
        'ultimas_acciones': ultimas_acciones,
    })


# =====================================================
# CRUD EVENTOS
# =====================================================

@login_required
def eventos_listar(request):
    eventos = Evento.objects.all()
    return render(request, 'eventos_listar.html', {'eventos': eventos})


@login_required
def eventos_crear(request):
    if request.method == 'POST':
        titulo = request.POST['titulo']
        descripcion = request.POST['descripcion']
        fecha = request.POST['fecha']
        hora = request.POST['hora']
        lugar = request.POST['lugar']
        capacidad = request.POST['capacidad']
        precio_inscripcion = request.POST['precio_inscripcion']

        evento = Evento.objects.create(
            titulo=titulo,
            descripcion=descripcion,
            fecha=fecha,
            hora=hora,
            lugar=lugar,
            capacidad=capacidad,
            precio_inscripcion=precio_inscripcion,
            creado_por=request.user
        )

        registrar_accion(request.user, f"Creó el evento: {evento.titulo}")
        crear_notificacion(request.user, f"Evento '{evento.titulo}' creado exitosamente.")

        return redirect('eventos_listar')

    return render(request, 'eventos_crear.html')


@login_required
def eventos_editar(request, id):
    evento = Evento.objects.get(id=id)

    if request.method == 'POST':
        evento.titulo = request.POST['titulo']
        evento.descripcion = request.POST['descripcion']
        evento.fecha = request.POST['fecha']
        evento.hora = request.POST['hora']
        evento.lugar = request.POST['lugar']
        evento.capacidad = request.POST['capacidad']
        evento.precio_inscripcion = request.POST['precio_inscripcion']
        evento.save()

        registrar_accion(request.user, f"Editó el evento: {evento.titulo}")
        crear_notificacion(request.user, f"Evento '{evento.titulo}' fue actualizado.")

        return redirect('eventos_listar')

    return render(request, 'eventos_editar.html', {'evento': evento})


@login_required
def eventos_eliminar(request, id):
    evento = Evento.objects.get(id=id)
    titulo = evento.titulo
    evento.delete()

    registrar_accion(request.user, f"Eliminó el evento: {titulo}")
    crear_notificacion(request.user, f"Evento '{titulo}' fue eliminado.")

    return redirect('eventos_listar')


# =====================================================
# CRUD PARTICIPANTES
# =====================================================

@login_required
def participantes_listar(request):
    participantes = Participante.objects.all()
    return render(request, 'participantes_listar.html', {'participantes': participantes})


@login_required
def participantes_crear(request):
    if request.method == 'POST':
        nombre = request.POST['nombre']
        email = request.POST['email']
        telefono = request.POST['telefono']

        participante = Participante.objects.create(
            nombre=nombre,
            email=email,
            telefono=telefono,
            creado_por=request.user
        )

        registrar_accion(request.user, f"Registró al participante: {participante.nombre}")
        crear_notificacion(request.user, f"Participante '{participante.nombre}' agregado.")

        return redirect('participantes_listar')

    return render(request, 'participantes_crear.html')


@login_required
def participantes_editar(request, id):
    participante = Participante.objects.get(id=id)

    if request.method == 'POST':
        participante.nombre = request.POST['nombre']
        participante.email = request.POST['email']
        participante.telefono = request.POST['telefono']
        participante.save()

        registrar_accion(request.user, f"Editó participante: {participante.nombre}")

        return redirect('participantes_listar')

    return render(request, 'participantes_editar.html', {'participante': participante})


@login_required
def participantes_eliminar(request, id):
    participante = Participante.objects.get(id=id)
    nombre = participante.nombre
    participante.delete()

    registrar_accion(request.user, f"Eliminó participante: {nombre}")

    return redirect('participantes_listar')


# =====================================================
# REGISTROS
# =====================================================

@login_required
def registros_listar(request):
    registros = Registro.objects.all()
    return render(request, 'registros_listar.html', {'registros': registros})


@login_required
def registros_crear(request):
    if request.method == 'POST':
        evento = Evento.objects.get(id=request.POST['evento'])
        participante = Participante.objects.get(id=request.POST['participante'])

        Registro.objects.create(evento=evento, participante=participante)

        registrar_accion(request.user, f"Registró asistencia: {participante.nombre}")
        crear_notificacion(request.user, f"Asistencia registrada para '{participante.nombre}'.")

        return redirect('registros_listar')

    return render(request, 'registros_crear.html', {
        'eventos': Evento.objects.all(),
        'participantes': Participante.objects.all()
    })


@login_required
def registros_eliminar(request, id):
    registro = Registro.objects.get(id=id)
    registro.delete()

    registrar_accion(request.user, "Eliminó un registro de asistencia")
    return redirect('registros_listar')


# =====================================================
# NOTIFICACIONES
# =====================================================

@login_required
def notificaciones_listar(request):
    notificaciones = Notificacion.objects.filter(usuario=request.user).order_by('-fecha')
    return render(request, 'notificaciones_listar.html', {'notificaciones': notificaciones})


# =====================================================
# USUARIOS (LISTAR / CREAR / ELIMINAR)
# =====================================================

@login_required
def usuarios_listar(request):
    usuarios = User.objects.all()
    return render(request, 'usuarios_listar.html', {'usuarios': usuarios})


@login_required
def usuarios_crear(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        if User.objects.filter(username=username).exists():
            messages.error(request, "Ese usuario ya existe.")
            return redirect('usuarios_crear')

        User.objects.create_user(username=username, password=password)

        registrar_accion(request.user, f"Creó el usuario: {username}")
        crear_notificacion(request.user, f"Usuario '{username}' creado correctamente.")

        return redirect('usuarios_listar')

    return render(request, 'usuarios_crear.html')


@login_required
def usuarios_eliminar(request, id):
    usuario = User.objects.get(id=id)
    nombre = usuario.username
    usuario.delete()

    registrar_accion(request.user, f"Eliminó el usuario: {nombre}")
    return redirect('usuarios_listar')



