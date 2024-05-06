from django.shortcuts import redirect, render, get_object_or_404
from .forms import signupEmpleadosUMAPS, intervaloCalendarioUMAPSForm, perfilEmpleadosUMAPS, intervaloCalendarioUMAPSZonaForm, registrozonasUMAPSForm
from django.contrib import messages 
from django.contrib.auth.decorators import login_required
from .models import perfilEmpleadosUMAPS, zonasUMAPS, intervaloCalendarioUMAPS, registroActividadUMAPS #Importación de models.py (Tablas de la Base de Datos)
from django.contrib.auth import authenticate
from django.utils import timezone
from django.urls import reverse
from datetime import timedelta
from django.db.models import Q

#------------------------------------------VISTA BIENVENIDA-------------------------------------------------#
def bienvenida(request):
	return render(request, "bienvenida.html")
#------------------------------------------VISTA ZONAS UMAPS------------------------------------------------#
@login_required
def index(request):
	zonas = zonasUMAPS.objects.all()
	context = []
	for zona in zonas:
		data = get_horario_activo_para_zona(zona.id)
		context.append({'zona': zona, 'intervalo': data['intervalo'], 'enhoras': data['enhoras']})
	return render(request, "index.html", {'data':context})
#--------------------------------VISTA REGISTRO DE EMPLEADOS UMAPS------------------------------------------#
def signup(request):
	form = signupEmpleadosUMAPS(request.POST)
	if request.method == "POST":
		if form.is_valid():
			form.save()
			username = form.cleaned_data['username']
			form = signupEmpleadosUMAPS()
			messages.success(request,f"¡USUARIO {username} CREADO EXITOSAMENTE!")
			return redirect('/accounts/login')
		else:
			form = signupEmpleadosUMAPS()
	context = { 'form' : form }
	return render(request, "formularioRegistroEmpleadosUMAPS.html", context)
#-------------------------------------VISTA LOGIN EMPLEADOS UMAPS--------------------------------------------#
def login(request):
	if request.method == "POST":
		form = perfilEmpleadosUMAPS(request.POST)
		if form.is_valid():
			cd = form.cleaned_data
			user = authenticate(request, username = cd['usernamne'], password = cd['password1'])
			if user is not None:
				if user.is_active:
					login(request, user)
		else:
			messages.error(request, "Usuario o contraseña incorrectos")
			form = perfilEmpleadosUMAPS()
			context = { "form" : form }	
			return render(request, "login.html", context)
#------------------------------------VISTA LOGOUT EMPLEADOS UMAPS--------------------------------------------#
def logout(request):
	return render(request, "logout.html")
#----------------------------------------VISTA PANEL DE CONTROL----------------------------------------------#
@login_required
def paneldecontrol(request, zona_id=None):

	empleadoUMAPSautorizado = request.user.groups.filter(name='empleadoUMAPS').exists()
	administradorUMAPSautorizado = request.user.groups.filter(name='administradorUMAPS').exists()

	if zona_id is None:
		return redirect('accesodenegado')
	
	zona = get_object_or_404(zonasUMAPS, pk=zona_id)
	datainter = get_horario_activo_para_zona(zona_id)
	intervalo = datainter['intervalo']
	enhoras = datainter['enhoras']
	todosIntervalos = intervaloCalendarioUMAPS.objects.filter(zona_id=zona_id)
	registros = registroActividadUMAPS.objects.filter(zona=zona)

	if request.method == 'POST':

		if 'toggle_activo' in request.POST:
			zona.activo = not zona.activo
			zona.save()
            
			registro_actividad = registroActividadUMAPS.objects.create(
				zona=zona,
				activacion=zona.activo,
				tiempo=timezone.now(),
				responsable=request.user
			)
			registro_actividad.save()            
			return redirect('paneldecontrol', zona_id=zona_id)
		elif 'intervalo_form_submit' in request.POST:
			intervalo_form = intervaloCalendarioUMAPSZonaForm(request.POST)
			if intervalo_form.is_valid():
				intervalo = intervalo_form.save(commit=False)
				intervalo.zona = zona
				print(request.user)
				print(perfilEmpleadosUMAPS.objects.get(user=request.user))
				intervalo.responsable = perfilEmpleadosUMAPS.objects.get(user=request.user)
				intervalo.save()
				return redirect('paneldecontrol', zona_id=zona_id)
	else:
		intervalo_form = intervaloCalendarioUMAPSZonaForm()
	
	if not (empleadoUMAPSautorizado or administradorUMAPSautorizado):
		return redirect('accesodenegado')
		
	return render(request, "paneldecontrol.html", {'zona':zona, 
												'intervalo':intervalo, 
												'enhoras':enhoras, 
												'todosIntervalos':todosIntervalos, 
												'intervaloForm':intervalo_form, 
												'registros':registros,
												'empleadoUMAPSautorizado':request.user.groups.filter(name='empleadoUMAPS').exists(),
												'administradorUMAPSautorizado':request.user.groups.filter(name='administradorUMAPS').exists()})
#--------------------------------------VISTA INTERVALO DE TIEMPO---------------------------------------------#
@login_required
def agregarIntervalo(request):

	empleadoUMAPSautorizado = request.user.groups.filter(name='empleadoUMAPS').exists()
	administradorUMAPSautorizado = request.user.groups.filter(name='administradorUMAPS').exists()

	if not (empleadoUMAPSautorizado or administradorUMAPSautorizado):
		return redirect('accesodenegado')

	intervalo_form = intervaloCalendarioUMAPSForm()
	zona_form = registrozonasUMAPSForm()

	if request.method == 'POST':
		if 'intervalo_form_submit' in request.POST:
			intervalo_form = intervaloCalendarioUMAPSForm(request.POST)
			if intervalo_form.is_valid():
				intervalo_form.save()
				zona = intervalo_form.cleaned_data['zona']
				messages.success(request, f"¡ZONA {zona} ACTIVADA EXITOSAMENTE!")                
		elif 'zona_form_submit' in request.POST:
			zona_form = registrozonasUMAPSForm(request.POST)
			if zona_form.is_valid():
				zona_form.save()
				return redirect(reverse('index'))
			        
	return render(request, 'agregarintervalo.html', {'intervalo_form': intervalo_form, 'zona_form': zona_form})
#--------------------------------------VISTA MOSTRAR CALENDARIO----------------------------------------------#
@login_required
def mostrarCalendario(request):

	empleadoUMAPSautorizado = request.user.groups.filter(name='empleadoUMAPS').exists()
	administradorUMAPSautorizado = request.user.groups.filter(name='administradorUMAPS').exists()

	if not (empleadoUMAPSautorizado or administradorUMAPSautorizado):
		return redirect('accesodenegado')

	hoy = timezone.now().date()
	ayer = hoy - timedelta(days=1)
	ultimo_dia = ayer + timedelta(days=5)
	rango_dias = [ayer + timedelta(days=i) for i in range(5)]
	intervalos = intervaloCalendarioUMAPS.objects.select_related('zona', 'responsable__user')
	zonas = zonasUMAPS.objects.all()

	local_timezone = timezone.get_current_timezone()
	for interval in intervalos:
		interval.horaInicio = interval.horaInicio.astimezone(local_timezone)
		interval.horaFinal = interval.horaFinal.astimezone(local_timezone)

	zona_intervalos = {}
	for zona in zonas:
		zona_intervalos[zona.nombre] = {0: [], 1: [], 2:[], 3:[], 4:[]}

	for interval in intervalos:		
		day = interval.horaInicio.date()
		if day in rango_dias:
			zona_intervalos[interval.zona.nombre][rango_dias.index(day)].append("<span class="'resaltado-verde'"><i class='fa-solid fa-toggle-on'></i>&nbsp;<span style="'color:#000;'">Encendido a las:&nbsp;" + str(interval.horaInicio.time())+"&nbsp;horas </span>")
		day = interval.horaFinal.date()
		if day in rango_dias:
			zona_intervalos[interval.zona.nombre][rango_dias.index(day)].append("<span class="'resaltado-rojo'"><i class='fa-solid fa-toggle-off'></i>&nbsp;<span style="'color:#fff;'">Apagado a las:&nbsp;" + str(interval.horaFinal.time())+"&nbsp;horas</span>")
	
	for element in zona_intervalos:
		for arr in zona_intervalos[element]:
			if len(zona_intervalos[element][arr]) == 0:
				zona_intervalos[element][arr].append("No hay actividad planeada")
		
	context = {
		'rango_dias': rango_dias,
		'zona_intervalos': zona_intervalos
	}
	return render(request, 'mostrarcalendario.html', context)

#--------------------------------------VISTA MOSTRAR CALENDARIO----------------------------------------------#
def get_horario_activo_para_zona(zona):
	tiempo_actual = timezone.now()
	intervalo_actual = intervaloCalendarioUMAPS.objects.filter(zona=zona, horaInicio__lte=tiempo_actual, horaFinal__gte=tiempo_actual)
	enhoras : bool = False
	if intervalo_actual.exists():
		return {'intervalo':intervalo_actual.first(), 'enhoras':True}
	intervalo_actual = intervaloCalendarioUMAPS.objects.filter(zona=zona, horaInicio__gte=tiempo_actual).order_by('horaInicio')
	if intervalo_actual.exists():
		return {'intervalo':intervalo_actual.first(), 'enhoras':False}
	else:
		return {'intervalo':None, 'enhoras':False}
#----------------------------------------VISTA ACCESO DENEGADO-----------------------------------------------#
def accesodenegado(request):
	return render(request, "plantillaAccesoDenegado.html")
