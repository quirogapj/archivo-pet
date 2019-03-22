from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    fecha_nacimiento = models.DateField(null=True)
    dni = models.CharField(max_length=30, verbose_name="DNI")
    es_veterinario = models.BooleanField('estado veterinario', default=False, null=True)
    matricula = models.CharField(max_length=30)
    direccion_veterinaria = models.CharField(max_length=30)
    nombre_veterinaria = models.CharField(max_length=30)
    telefono_veterinaria = models.CharField(max_length=15)
    telefono_celular = models.CharField(max_length=15, blank=True)

@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()

class Propietario(models.Model):
    nombre = models.CharField(max_length=30)
    apellido = models.CharField(max_length=30)
    dni = models.CharField(max_length=30)
    def __str__(self):
        return self.dni + " - " + self.nombre + " " + self.apellido


class Raza(models.Model):
    raza_nombre = models.CharField(max_length=20)
    def __str__(self):
        return self.raza_nombre

class Tipo_Mascota(models.Model):
    class Meta:
        verbose_name_plural = "tipo de mascotas"
        verbose_name = "tipo de mascota"
    tipo_mascota_nombre = models.CharField(max_length=20)
    def __str__(self):
        return self.tipo_mascota_nombre

class Mascota(models.Model):
    #identificaciones = models.ForeignKey(Identificacion, on_delete=models.CASCADE, blank=True, null=True)
    veterinario = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    propietario = models.ForeignKey(Propietario, on_delete=models.CASCADE)
    mascota_nombre = models.CharField('nombre', max_length=20)
    mascota_tipo = models.ForeignKey('Tipo_Mascota', on_delete=models.CASCADE, verbose_name="Tipo")
    mascota_raza = models.ForeignKey('Raza', on_delete=models.CASCADE, verbose_name="Raza")
    MACHO = "M"
    HEMBRA = "H"
    MASCOTA_SEXO_OPCIONES = (
        (MACHO, 'Macho'),
        (HEMBRA, 'Hembra'),
    )
    mascota_sexo = models.CharField("Sexo",
        max_length=2,
        choices=MASCOTA_SEXO_OPCIONES,
    )
    fecha_nacimiento_mascota = models.DateField('fecha de nacimiento')
    mascota_color = models.CharField("Color", max_length=20)
    def __str__(self):
        return self.mascota_nombre


class Identificacion(models.Model):
    class Meta:
        verbose_name_plural = "identificaciones"
    mascota = models.ForeignKey(Mascota, on_delete=models.CASCADE, blank=True, null=True)
    IMPLANTE = "IM"
    PLACA = "PL"
    IDENTIFICACION_TIPO_OPCIONES = (
        (IMPLANTE, 'Implante'),
        (PLACA, 'Placa'),
    )
    identificacion_tipo = models.CharField('tipo',
        max_length=2,
        choices=IDENTIFICACION_TIPO_OPCIONES,
        default=PLACA,
        blank=True,
        null=True
    )
    identificacion_ubicacion = models.CharField('ubicacion', max_length=20, blank=True, null=True)
    identificacion_codigo = models.CharField('codigo', max_length=10, unique=True, blank=True, null=True)
    fecha_implante = models.DateField('fecha implante', auto_now_add=True)
    def __str__(self):
        return self.identificacion_codigo
