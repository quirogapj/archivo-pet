from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User


# Register your models here.


from .models import Mascota, Identificacion, Raza, Tipo_Mascota, Propietario, Profile

class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'
    fk_name = 'user'

class CustomUserAdmin(UserAdmin):
    inlines = (ProfileInline, )

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(CustomUserAdmin, self).get_inline_instances(request, obj)


class IdentificacionesInline(admin.TabularInline):
    model = Identificacion

class MascotaAdmin(admin.ModelAdmin):
    inlines = [
        IdentificacionesInline,
    ]

    model = Mascota

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
admin.site.register(Mascota, MascotaAdmin)
admin.site.register(Identificacion)
admin.site.register(Raza)
admin.site.register(Tipo_Mascota)
admin.site.register(Propietario)
