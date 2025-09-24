import uuid
from decimal import Decimal
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator
from django.db import models
from django.utils import timezone
from django.utils.text import slugify


class User(AbstractUser):
    class Rol(models.TextChoices):
        VOLUNTARIO = "VOL", "Voluntario"
        ORGANIZADOR = "ORG", "Organizador/Coordinador"
        STAFF = "STA", "Staff"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    rol = models.CharField(max_length=3, choices=Rol.choices, default=Rol.VOLUNTARIO)
    telefono = models.CharField(max_length=20, blank=True)
    ciudad = models.CharField(max_length=100, blank=True)
    habilidades = models.ManyToManyField("Habilidad", blank=True, related_name="usuarios")

    class Meta:
        ordering = ["username"]
        verbose_name_plural = "Usuarios"

    def __str__(self):
        return f"{self.username} ({self.get_rol_display()})"


class Organizacion(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nombre = models.CharField(max_length=200, unique=True)
    correo = models.EmailField(blank=True)
    telefono = models.CharField(max_length=20, blank=True)
    sitio_web = models.URLField(blank=True)
    descripcion = models.TextField(blank=True)

    class Meta:
        ordering = ["nombre"]
        verbose_name_plural = "Organizaciones"

    def __str__(self):
        return self.nombre


class Habilidad(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nombre = models.CharField(max_length=120, unique=True)
    slug = models.SlugField(max_length=140, unique=True, blank=True)

    class Meta:
        ordering = ["nombre"]
        verbose_name_plural = "Habilidades"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nombre)
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.nombre


class Causa(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nombre = models.CharField(max_length=150, unique=True)
    slug = models.SlugField(max_length=170, unique=True, blank=True)
    descripcion = models.TextField(blank=True)

    class Meta:
        ordering = ["nombre"]
        verbose_name_plural = "Causas"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nombre)
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.nombre


class Campana(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    organizacion = models.ForeignKey(Organizacion, on_delete=models.CASCADE, related_name="campanas")
    titulo = models.CharField(max_length=200)
    slug = models.SlugField(max_length=230, unique=True, blank=True)
    descripcion = models.TextField(blank=True)
    fecha_inicio = models.DateField()
    fecha_termino = models.DateField()
    causas = models.ManyToManyField(Causa, related_name="campanas", blank=True)
    creada_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="campanas_creadas",
    )

    class Meta:
        ordering = ["-fecha_inicio"]
        verbose_name = "Campaña"
        verbose_name_plural = "Campañas"
        constraints = [
            models.CheckConstraint(
                check=models.Q(fecha_termino__gte=models.F("fecha_inicio")),
                name="campana_fechas_validas",
            ),
        ]
        indexes = [models.Index(fields=["fecha_inicio", "fecha_termino"])]

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.titulo)
            s = base
            i = 1
            while Campana.objects.filter(slug=s).exclude(pk=self.pk).exists():
                i += 1
                s = f"{base}-{i}"
            self.slug = s
        return super().save(*args, **kwargs)

    @property
    def esta_activa(self):
        hoy = timezone.localdate()
        return self.fecha_inicio <= hoy <= self.fecha_termino

    def __str__(self):
        return f"{self.titulo} ({self.organizacion.nombre})"


class Ubicacion(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nombre = models.CharField(max_length=150)
    direccion = models.CharField(max_length=250, blank=True)
    ciudad = models.CharField(max_length=120, blank=True)
    latitud = models.FloatField(null=True, blank=True)
    longitud = models.FloatField(null=True, blank=True)

    class Meta:
        ordering = ["ciudad", "nombre"]
        verbose_name = "Ubicación"
        verbose_name_plural = "Ubicaciones"

    def __str__(self):
        return f"{self.nombre} - {self.ciudad}" if self.ciudad else self.nombre


class Actividad(models.Model):
    class Estado(models.TextChoices):
        PLANIFICADA = "PLN", "Planificada"
        ABIERTA = "OPN", "Inscripciones abiertas"
        SIN_CUPOS = "FUL", "Cupos llenos"
        FINALIZADA = "DON", "Finalizada"
        CANCELADA = "CAN", "Cancelada"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    campana = models.ForeignKey(Campana, on_delete=models.CASCADE, related_name="actividades")
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True)
    inicio = models.DateTimeField()
    termino = models.DateTimeField()
    ubicacion = models.ForeignKey(Ubicacion, on_delete=models.SET_NULL, null=True, blank=True, related_name="actividades")
    cupos = models.PositiveIntegerField(default=10, validators=[MinValueValidator(1)])
    estado = models.CharField(max_length=3, choices=Estado.choices, default=Estado.PLANIFICADA)

    class Meta:
        ordering = ["inicio"]
        verbose_name = "Actividad"
        verbose_name_plural = "Actividades"
        constraints = [
            models.CheckConstraint(
                check=models.Q(termino__gt=models.F("inicio")),
                name="actividad_tiempo_valido",
            ),
        ]
        indexes = [models.Index(fields=["inicio"]), models.Index(fields=["estado"])]

    def __str__(self):
        return f"{self.titulo} · {self.inicio:%d-%m %H:%M}"

    @property
    def cupos_disponibles(self):
        tomados = self.participaciones.filter(
            estado__in=[Participacion.Estado.APROBADA, Participacion.Estado.ASISTIO]
        ).count()
        return max(self.cupos - tomados, 0)


class Participacion(models.Model):
    class Estado(models.TextChoices):
        PENDIENTE = "PEN", "Pendiente"
        APROBADA = "APR", "Aprobada"
        RECHAZADA = "REJ", "Rechazada"
        CANCELADA = "CAN", "Cancelada"
        ASISTIO = "ATT", "Asistió"
        NO_ASISTE = "NOS", "No se presentó"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="participaciones")
    actividad = models.ForeignKey(Actividad, on_delete=models.CASCADE, related_name="participaciones")
    estado = models.CharField(max_length=3, choices=Estado.choices, default=Estado.PENDIENTE)
    postulada_en = models.DateTimeField(default=timezone.now)
    aprobada_en = models.DateTimeField(null=True, blank=True)
    check_in = models.DateTimeField(null=True, blank=True)
    check_out = models.DateTimeField(null=True, blank=True)
    horas = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal("0.00"))

    class Meta:
        ordering = ["-postulada_en"]
        verbose_name = "Participación"
        verbose_name_plural = "Participaciones"
        unique_together = ("usuario", "actividad")
        indexes = [models.Index(fields=["estado"])]

    def clean(self):
        if self.check_in and self.check_out and self.check_out <= self.check_in:
            from django.core.exceptions import ValidationError
            raise ValidationError("La salida debe ser posterior a la entrada.")

    def calcular_horas(self):
        if self.check_in and self.check_out:
            delta = self.check_out - self.check_in
            self.horas = Decimal(round(delta.total_seconds() / 3600, 2))

    def save(self, *args, **kwargs):
        self.calcular_horas()
        return super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.usuario.username} → {self.actividad.titulo} [{self.get_estado_display()}]"

