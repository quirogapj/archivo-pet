from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from .models import Mascota, Identificacion, Propietario, Profile

#class DateInput(forms.DateInput):
#    input_type = 'date'

class MascotaForm(forms.ModelForm):

    class Meta:
        model = Mascota
        exclude = ['veterinario', 'propietario']
        fecha_nacimiento_mascota = forms.DateField(input_formats=['%d/%m/%Y'])
        fecha_ultima_vacunacion = forms.DateField(input_formats=['%d/%m/%Y'])
        #senias = forms.Textarea(attrs={'rows':2})
        #vacunas = forms.Textarea(attrs={'rows':2})
        #tratamientos = forms.Textarea(attrs={'rows':2})
        widgets = {
            'senias': forms.Textarea(attrs={'rows': 3}),
            'vacunas': forms.Textarea(attrs={'rows': 3}),
            'tratamientos': forms.Textarea(attrs={'rows': 3}),
   }
        #fecha_nacimiento_mascota = forms.DateField(
        #    widget=forms.widgets.DateInput(format='%d/%m/%Y')
        #)
        #widgets =  {'fecha_nacimiento_mascota' : DateInput()}

class PropietarioForm(forms.ModelForm):

    class Meta:
        model = Propietario
        fields = ('nombre', 'apellido', 'dni', 'email', 'telefono')


    #def clean_identificacion_codigo(self):
    #    identificacion_codigo = self.cleaned_data['identificacion_codigo']
    #    if identificacion_codigo not in Identificacion.objects.filter(mascota__isnull=True).values_list('identificacion_codigo', flat=True):
    #        raise ValidationError("Identificacion inválida o en uso.")
    #    return identificacion_codigo

    #def save(self, commit=True):
    #    identificacion_codigo = self.cleaned_data['identificacion_codigo']
    #    identificacion, _ = Identificacion.objects.get_or_create(identificacion_codigo=identificacion_codigo)
    #    instance = self.save(commit=False)
    #    instance.identificacion_codigo = identificacion_codigo
        #if commit = True:
        #    instance.save()
    #    return instance


    #class Meta:
    #    model = Mascota
    #    fields = ('mascota_nombre', 'mascota_sexo', 'mascota_tipo', 'mascota_raza', 'mascota_color', 'fecha_nacimiento')


class SignUpForm(UserCreationForm):
    dni = forms.CharField(max_length=30, help_text='Requerido.', label='DNI')
    #es_veterinario = models.BooleanField('estado veterinario', default=False, null=True)
    tiene_lectora = forms.BooleanField(label='Tilde si dispone de lectora de microchip', required=False   )
    calle_veterinaria = forms.CharField(max_length=30, help_text='Requerido.')
    numero_calle_veterinaria = forms.IntegerField(help_text='Requerido.')
    localidad_veterinaria = forms.CharField(max_length=30, help_text='Requerido.')
    cp_veterinaria = forms.IntegerField(label='Código Postal:',help_text='Requerido.')
    provincia_veterinaria = forms.CharField(max_length=30, help_text='Requerido.')
    nombre_veterinaria = forms.CharField(max_length=30, help_text='Requerido.')
    telefono_veterinaria = forms.CharField(max_length=30, help_text='Requerido.')
    telefono_celular = forms.CharField(max_length=30, required=False, help_text='Opcional.')
    email = forms.EmailField(max_length=254, help_text='Requerido. Ingrese una dirección válida.', label='Email veterinaria')
    first_name = forms.CharField(max_length=30, label='Nombre:', help_text='Requerido.')
    last_name = forms.CharField(max_length=30, label='Apellidos:', help_text='Requerido.')

    class Meta:
        model = User
        fields = ('username',
        'password1',
        'password2',
        'email',
        'first_name',
        'last_name',
        'dni',
        'tiene_lectora',
        'calle_veterinaria',
        'numero_calle_veterinaria',
        'localidad_veterinaria',
        'cp_veterinaria',
        'provincia_veterinaria',
        'nombre_veterinaria',
        'telefono_veterinaria',
        'telefono_celular')

class ContactForm(forms.Form):
    from_email = forms.EmailField(label='Email', required=True)
    subject = forms.CharField(label='Título', required=True)
    message = forms.CharField(label='Mensaje', widget=forms.Textarea, required=True)


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('dni',
        'tiene_lectora',
        'calle_veterinaria',
        'numero_calle_veterinaria',
        'localidad_veterinaria',
        'cp_veterinaria',
        'provincia_veterinaria',
        'nombre_veterinaria',
        'telefono_veterinaria',
        'telefono_celular')
