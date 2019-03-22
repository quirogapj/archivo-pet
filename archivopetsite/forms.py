from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from .models import Mascota, Identificacion, Propietario

#class DateInput(forms.DateInput):
#    input_type = 'date'

class MascotaForm(forms.ModelForm):

    class Meta:
        model = Mascota
        exclude = ['veterinario', 'propietario']
        fecha_nacimiento_mascota = forms.DateField(input_formats=['%d/%m/%Y'])
        #fecha_nacimiento_mascota = forms.DateField(
        #    widget=forms.widgets.DateInput(format='%d/%m/%Y')
        #)
        #widgets =  {'fecha_nacimiento_mascota' : DateInput()}

class PropietarioForm(forms.ModelForm):

    class Meta:
        model = Propietario
        fields = ('nombre', 'apellido', 'dni')


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

    class Meta:
        model = User
        fields = ('username','email', 'password1', 'password2',  )
