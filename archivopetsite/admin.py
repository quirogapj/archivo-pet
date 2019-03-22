from django.contrib import admin

# Register your models here.

from .models import Mascota, Identificacion, Raza, Tipo_Mascota, Propietario

class IdentificacionesInline(admin.TabularInline):
    model = Identificacion

class MascotaAdmin(admin.ModelAdmin):
    inlines = [
        IdentificacionesInline,
    ]

    model = Mascota

admin.site.register(Mascota, MascotaAdmin)
admin.site.register(Identificacion)
admin.site.register(Raza)
admin.site.register(Tipo_Mascota)
admin.site.register(Propietario)
