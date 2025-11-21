from django.db import models
from django.contrib.auth.models import User


# =====================================================
# ROLES DE USUARIO
# =====================================================
class Rol(models.Model):
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre


# =====================================================
# PERFIL DEL USUARIO
# =====================================================
class Perfil(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rol = models.ForeignKey(Rol, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} - {self.rol.nombre}"


# =====================================================
# EVENTOS
# =====================================================
class Evento(models.Model):
    titulo = models.CharField(max_length=100)
    descripcion = models.TextField()
    fecha = models.DateField()
    hora = models.TimeField()
    lugar = models.CharField(max_length=150)
    creado_por = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    creado_en = models.DateTimeField(auto_now_add=True)

    # NUEVO: Requerido por tu profesor
    capacidad = models.IntegerField(default=50)
    precio_inscripcion = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return self.titulo


# =====================================================
# PARTICIPANTES
# =====================================================
class Participante(models.Model):
    nombre = models.CharField(max_length=100)
    email = models.EmailField()
    telefono = models.CharField(max_length=20, null=True, blank=True)
    creado_por = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    creado_en = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre


# =====================================================
# REGISTROS (INSCRIPCIÓN + ASISTENCIA)
# =====================================================
class Registro(models.Model):
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE)
    participante = models.ForeignKey(Participante, on_delete=models.CASCADE)
    fecha_registro = models.DateTimeField(auto_now_add=True)

    # NUEVOS CAMPOS PEDIDOS POR TU PROFESOR
    asistencia_confirmada = models.BooleanField(default=False)
    certificado_generado = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.participante.nombre} en {self.evento.titulo}"


# =====================================================
# PAGOS (INSCRIPCIÓN)
# =====================================================
class Pago(models.Model):
    registro = models.OneToOneField(Registro, on_delete=models.CASCADE)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    pagado = models.BooleanField(default=False)
    fecha_pago = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Pago de {self.registro.participante.nombre}"


# =====================================================
# RECORDATORIOS AUTOMÁTICOS
# =====================================================
class Recordatorio(models.Model):
    registro = models.ForeignKey(Registro, on_delete=models.CASCADE)
    mensaje = models.CharField(max_length=200)
    enviado = models.BooleanField(default=False)
    fecha_envio = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Recordatorio a {self.registro.participante.nombre}"


# =====================================================
# REPORTES DE ASISTENCIA
# =====================================================
class ReporteAsistencia(models.Model):
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE)
    total_inscritos = models.IntegerField()
    total_asistentes = models.IntegerField()
    generado_en = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Reporte de {self.evento.titulo}"


# =====================================================
# NOTIFICACIONES
# =====================================================
class Notificacion(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    mensaje = models.TextField()
    leida = models.BooleanField(default=False)
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notif. para {self.usuario.username}"


# =====================================================
# AUDITORÍA
# =====================================================
class Auditoria(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    accion = models.CharField(max_length=200)
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.usuario.username} - {self.accion}"
