from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.utils import timezone
from .models import (
    User,
    Organizacion,
    Habilidad,
    Causa,
    Campana,
    Ubicacion,
    Actividad,
    Participacion,
)

@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    fieldsets = DjangoUserAdmin.fieldsets + (
        ("Perfil", {"fields": ("rol", "telefono", "ciudad", "habilidades")}),
    )
    list_display = ("username", "email", "rol", "ciudad", "is_active", "is_staff")
    list_filter = ("rol", "is_staff", "is_active", "habilidades")
    search_fields = ("username", "first_name", "last_name", "email")
    filter_horizontal = ("habilidades",)


class CampanaInline(admin.TabularInline):
    model = Campana
    extra = 0
    fields = ("titulo", "fecha_inicio", "fecha_termino")
    show_change_link = True


@admin.register(Organizacion)
class OrganizacionAdmin(admin.ModelAdmin):
    list_display = ("nombre", "correo", "telefono", "sitio_web")
    search_fields = ("nombre",)
    inlines = [CampanaInline]


@admin.register(Habilidad)
class HabilidadAdmin(admin.ModelAdmin):
    list_display = ("nombre", "slug")
    prepopulated_fields = {"slug": ("nombre",)}
    search_fields = ("nombre",)


@admin.register(Causa)
class CausaAdmin(admin.ModelAdmin):
    list_display = ("nombre", "slug")
    prepopulated_fields = {"slug": ("nombre",)}
    search_fields = ("nombre",)


class ParticipacionInline(admin.TabularInline):
    model = Participacion
    extra = 0
    fields = ("usuario", "estado", "postulada_en", "aprobada_en", "check_in", "check_out", "horas")
    readonly_fields = ("horas",)


@admin.register(Campana)
class CampanaAdmin(admin.ModelAdmin):
    list_display = ("titulo", "organizacion", "fecha_inicio", "fecha_termino", "esta_activa")
    list_filter = ("organizacion", "causas")
    search_fields = ("titulo", "organizacion__nombre")
    prepopulated_fields = {"slug": ("titulo",)}
    filter_horizontal = ("causas",)


@admin.register(Ubicacion)
class UbicacionAdmin(admin.ModelAdmin):
    list_display = ("nombre", "ciudad", "direccion")
    search_fields = ("nombre", "ciudad", "direccion")


@admin.action(description="Marcar como Asistió")
def marcar_asistio(modeladmin, request, queryset):
    queryset.update(estado=Participacion.Estado.ASISTIO)


@admin.action(description="Aprobar inscripción")
def aprobar_inscripcion(modeladmin, request, queryset):
    queryset.update(estado=Participacion.Estado.APROBADA, aprobada_en=timezone.now())


@admin.register(Actividad)
class ActividadAdmin(admin.ModelAdmin):
    list_display = (
        "titulo",
        "campana",
        "inicio",
        "termino",
        "estado",
        "cupos",
        "cupos_disponibles",
    )
    list_filter = ("estado", "campana", "ubicacion")
    search_fields = ("titulo", "campana__titulo")
    date_hierarchy = "inicio"
    inlines = [ParticipacionInline]


@admin.register(Participacion)
class ParticipacionAdmin(admin.ModelAdmin):
    list_display = (
        "usuario",
        "actividad",
        "estado",
        "postulada_en",
        "aprobada_en",
        "check_in",
        "check_out",
        "horas",
    )
    list_filter = ("estado", "actividad__campana", "actividad")
    search_fields = ("usuario__username", "actividad__titulo")
    readonly_fields = ("horas",)
    actions = [marcar_asistio, aprobar_inscripcion]
