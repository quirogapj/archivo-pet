from django.core.mail import send_mail, BadHeaderError
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from .models import Mascota, Identificacion, Propietario
from .forms import MascotaForm, PropietarioForm, ContactForm, UserForm, ProfileForm
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.forms.models import inlineformset_factory
from django.http import HttpResponse
from django.db import transaction
from django.contrib import messages
from django.conf import settings
from django.contrib import admin


from .forms import SignUpForm


def index(request):
    """
    Función vista para la página inicio del sitio.
    """
    # Genera contadores de algunos de los objetos principales
    #num_books=Book.objects.all().count()
    #num_instances=BookInstance.objects.all().count()
    # Libros disponibles (status = 'a')
    #num_instances_available=BookInstance.objects.filter(status__exact='a').count()
    #num_authors=Author.objects.count()  # El 'all()' esta implícito por defecto.

    # Renderiza la plantilla HTML index.html con los datos en la variable contexto
    return render(
        request,
        'index.html'#,
        #context={'num_books':num_books,'num_instances':num_instances,'num_instances_available':num_instances_available,'num_authors':num_authors},
    )

@login_required
def home(request):
    return render(request, 'home.html')

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()  # load the profile instance created by the signal
            #user.profile.birth_date = form.cleaned_data.get('fecha_nacimiento')
            user.is_staff = False
            user.is_superuser = False
            user.profile.es_veterinario = True
            user.profile.tiene_lectora = form.cleaned_data.get('tiene_lectora')
            user.profile.dni = form.cleaned_data.get('dni')
            user.profile.calle_veterinaria = form.cleaned_data.get('calle_veterinaria')
            user.profile.numero_calle_veterinaria = form.cleaned_data.get('numero_calle_veterinaria')
            user.profile.localidad_veterinaria = form.cleaned_data.get('localidad_veterinaria')
            user.profile.provincia_veterinaria = form.cleaned_data.get('provincia_veterinaria')
            user.profile.nombre_veterinaria = form.cleaned_data.get('nombre_veterinaria')
            user.profile.telefono_veterinaria = form.cleaned_data.get('telefono_veterinaria')
            user.profile.telefono_celular = form.cleaned_data.get('telefono_celular')
            user.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            return redirect('index')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})

@login_required
def mascota_list(request):
    mascotas = Mascota.objects.filter(veterinario=request.user).order_by('fecha_nacimiento_mascota')
    return render(request, 'archivopetsite/mascota_list.html', {'mascotas': mascotas})

@login_required
def mascota_detail(request, pk):
    mascota = get_object_or_404(Mascota, pk=pk)
    return render(request, 'archivopetsite/mascota_detail.html', {'mascota': mascota})

@login_required
def mascota_new(request):

    #IdentificacionesFormSet = inlineformset_factory(Mascota, Identificacion, fields=['identificacion_codigo'], widgets={
    #'identificacion_codigo': Textarea(attrs={'cols': 80, 'rows': 20})}, form=MascotaForm, extra=1, can_delete=False)
    IdentificacionesFormSet = inlineformset_factory(Mascota, Identificacion, fields=('identificacion_codigo','identificacion_tipo', 'identificacion_ubicacion',), form=MascotaForm, extra=2, max_num=2, can_delete=False)
    #PropietarioFormSet = inlineformset_factory(Propietario, Mascota, form=MascotaForm, extra=0, max_num=1, can_delete=False)
    mascota = Mascota()
    propietario = Propietario()

    if request.method == "POST":
        form = MascotaForm(request.POST, instance=mascota)
        formpropietario = PropietarioForm(request.POST, instance=propietario)
        identificacionesformset = IdentificacionesFormSet(request.POST, instance=mascota)
        #propietarioformset = PropietarioFormSet(request.POST, instance=mascota)
        if form.is_valid() and identificacionesformset.is_valid() and formpropietario.is_valid():
            mascota = form.save(commit=False)
            propietario = formpropietario.save()

            mascota.veterinario = request.user
            mascota.propietario = propietario

            mascota.save()
            #nuevas_identificaciones = identificacionesformset.save(commit=False)
            #for identificacion in nuevas_identificaciones:
            #    new_id = Identificacion.objects.get_or_create( identificacion_codigo='identificacion')
            #    identificacion.mascota = mascota
            #    identificacion.save()
            identificacionesformset.save()
            #propietarioformset.save()
            return redirect('mascota_detail', pk=mascota.pk)
    else:
        form = MascotaForm(instance=mascota)
        formpropietario = PropietarioForm(instance=propietario)
        identificacionesformset = IdentificacionesFormSet(instance=mascota)
        #propietarioformset = PropietarioFormSet(instance=mascota)
    return render(request, 'archivopetsite/mascota_edit.html', {
        'form': form,
        'formpropietario': formpropietario,
        'identificacionesformset': identificacionesformset,
    })

@login_required
def mascota_edit(request, pk):
    mascota = get_object_or_404(Mascota, pk=pk)
    IdentificacionesFormSet = inlineformset_factory(Mascota, Identificacion, fields=('identificacion_codigo','identificacion_tipo', 'identificacion_ubicacion',), form=MascotaForm, extra=1, max_num=2, can_delete=False)
    propietario = get_object_or_404(Propietario, pk=mascota.propietario.id)
    if request.method == "POST":
        form = MascotaForm(request.POST, instance=mascota)
        identificacionesformset = IdentificacionesFormSet(request.POST, instance=mascota)
        formpropietario = PropietarioForm(request.POST, instance=propietario)
        if form.is_valid() and identificacionesformset.is_valid() and formpropietario.is_valid():
            mascota = form.save(commit=False)
            mascota.save()
            identificacionesformset.save()
            return redirect('mascota_detail', pk=mascota.pk)
    else:
        form = MascotaForm(instance=mascota)
        identificacionesformset = IdentificacionesFormSet(instance=mascota)
        formpropietario = PropietarioForm(instance=propietario)
    return render(request, 'archivopetsite/mascota_edit.html', {
        'form': form,
        'identificacionesformset': identificacionesformset,
        'formpropietario': formpropietario,
    })

def search_form(request):
    return render(request, 'archivopetsite/buscar_mascota.html')

def preguntasFrecuentesView(request):
    return render(request, 'archivopetsite/preguntas_frecuentes.html')

def search(request):
    error = False
    if 'q' in request.GET and request.GET['q']:
        q = request.GET['q']
        identificacion = Identificacion.objects.filter(identificacion_codigo__icontains=q)
        if identificacion:
            id = Identificacion.objects.get(identificacion_codigo__icontains=q)
            name = request.GET['nombre']
            subject = "Archivo PET - Reporte de mascota ENCONTRADA"
            tel = request.GET['telefono']
            from_email = request.GET['email']
            to_email = id.mascota.propietario.email
            message = "\nNombre: " + name +"\nTelefono: " + tel + "\nEmail: " + from_email + "\nMensaje: " + request.GET['mensaje']
            try:
                send_mail(subject, message, from_email, [to_email])
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
        return render(request, 'archivopetsite/busqueda_resultados.html',
                      {'identificacion': identificacion, 'query': q})
    else:
        error = True
        return render(request, 'archivopetsite/buscar_mascota.html', {'error': error})

def emailView(request):
    if request.method == 'GET':
        form = ContactForm()
    else:
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            from_email = form.cleaned_data['from_email']
            message = form.cleaned_data['message']
            try:
                send_mail(subject, message, from_email, ['archivopet@gmail.com'])
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            return redirect('success')
    return render(request, "archivopetsite/email.html", {'form': form})

def successView(request):
    #return HttpResponse('Success! Thank you for your message.')
    return render(request, 'archivopetsite/success.html')

@login_required
@transaction.atomic
def update_profile(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            request.user.is_staff = False
            request.user.is_superuser = False
            user_form.save()
            profile_form.save()
            messages.success(request, ('Your profile was successfully updated!'))
            return redirect('/modificarperfil')
        else:
            messages.error(request, ('Please correct the error below.'))
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
    return render(request, 'profiles/profile.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })
