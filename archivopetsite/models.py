from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.validators import RegexValidator


alphanumeric = RegexValidator(r'^[0-9a-zA-Z]*$', 'Sólo se permiten números y letras.')


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    #bio = models.TextField(max_length=500, blank=True)
    #fecha_nacimiento = models.DateField(null=True)
    dni = models.CharField(max_length=30, verbose_name="DNI", null=True)
    es_veterinario = models.BooleanField('estado veterinario', default=False, null=True)
    tiene_lectora = models.BooleanField('tiene lectora', default=False, null=True)
    #matricula = models.CharField(max_length=30)
    MUNICIPALIDAD = "MU"
    CRIADERO = "CR"
    VETERINARIA = "VT"
    OTRO = "OT"
    ESTABLECIMIENTO_TIPO_OPCIONES = (
        (MUNICIPALIDAD, 'Municipalidad'),
        (CRIADERO, 'Criadero'),
        (VETERINARIA, 'Veterinaria'),
        (OTRO, 'Otro'),
    )
    establecimiento_tipo = models.CharField('Tipo Establecimiento',
        max_length=2,
        choices=ESTABLECIMIENTO_TIPO_OPCIONES,
    )
    calle_veterinaria = models.CharField('Calle', max_length=30, null=True)
    numero_calle_veterinaria = models.PositiveIntegerField(null=True)
    localidad_veterinaria = models.CharField(max_length=30, null=True)
    cp_veterinaria = models.PositiveIntegerField(null=True)
    provincia_veterinaria = models.CharField(max_length=30, null=True)
    nombre_veterinaria = models.CharField(max_length=30, null=True)
    telefono_veterinaria = models.CharField(max_length=15, null=True)
    telefono_celular = models.CharField(max_length=15, blank=True, null=True)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


#@receiver(post_save, sender=User)
#def update_user_profile(sender, instance, created, **kwargs):
#    if created:
#        Profile.objects.create(user=instance)
#    instance.profile.save()

class Propietario(models.Model):
    nombre = models.CharField(max_length=30)
    apellido = models.CharField(max_length=30)
    dni = models.CharField(max_length=30)
    telefono = models.CharField(max_length=15)
    email = models.EmailField(max_length=70)
    def __str__(self):
        return self.dni + " - " + self.nombre + " " + self.apellido


class Raza(models.Model):
    raza_nombre = models.CharField(max_length=35)
    def __str__(self):
        return self.raza_nombre

class Tipo_Mascota(models.Model):
    class Meta:
        verbose_name_plural = "especie de mascotas"
        verbose_name = "especie de mascota"
    tipo_mascota_nombre = models.CharField(max_length=20)
    def __str__(self):
        return self.tipo_mascota_nombre

class Mascota(models.Model):
    #identificaciones = models.ForeignKey(Identificacion, on_delete=models.CASCADE, blank=True, null=True)
    veterinario = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    propietario = models.ForeignKey(Propietario, on_delete=models.CASCADE)
    mascota_nombre = models.CharField('nombre', max_length=20, help_text="Ingrese APELLIDO y NOMBRE")
    mascota_tipo = models.ForeignKey('Tipo_Mascota', on_delete=models.CASCADE, verbose_name="Especie")
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
    fecha_ultima_vacunacion = models.DateField('fecha de ultima vacunacion')
    #observaciones = models.TextField(null=True, blank=True)
    senias = models.TextField('Señas',null=True, blank=True)
    vacunas = models.TextField(null=True, blank=True)
    tratamientos = models.TextField(null=True, blank=True)
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
    identificacion_codigo = models.CharField('codigo', max_length=16, unique=True, blank=True, null=True, validators=[alphanumeric])
    fecha_implante = models.DateField('fecha implante', auto_now_add=True)
    def __str__(self):
        return self.identificacion_codigo
