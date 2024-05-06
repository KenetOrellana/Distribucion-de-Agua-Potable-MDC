from django import forms
from .models import zonasUMAPS, intervaloCalendarioUMAPS, perfilEmpleadosUMAPS
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

#------------------------FORM REGISTRO (apunta a la views.py: signup)--------------------------------#
class signupEmpleadosUMAPS(UserCreationForm):

	username = forms.CharField(label='Usuario',  widget=forms.TextInput(
		attrs={
			'placeholder': 'Ingrese un nombre de usuario'}
			),
			error_messages={'required': ''}
		)
	first_name = forms.CharField(label='Primer Nombre', widget=forms.TextInput(
		attrs={
			'placeholder': 'Ingrese su primer nombre'}
			),
			error_messages={'required': ''}
		)
	last_name = forms.CharField(label='Primer Apellido', widget=forms.TextInput(
		attrs={
			'placeholder': 'Ingrese su primer apellido'}
			),
			error_messages={'required': ''}
		)
	email = forms.EmailField(label='Correo Electrónico', widget=forms.TextInput(
		attrs={
			'placeholder': 'Ingrese su correo electrónico'}
			),
			error_messages={'required': ''}
		)
	password1 = forms.CharField(label='Contraseña', widget=forms.PasswordInput(
		attrs={
			'placeholder': 'Ingrese su contraseña'}
			),
			error_messages={'required': ''}
		)
	password2 = forms.CharField(label='Confirme la Contraseña', widget=forms.PasswordInput(
		attrs={
			'placeholder': 'Confirme su contraseña'}
			),
			error_messages={'required': ''}
		)
	class Meta:
		model = User
		fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']
#-----------FORM CALENDARIO (apunta a las views.py: agregarIntervalo y mostrarCalendario)-------------#
class intervaloCalendarioUMAPSForm(forms.ModelForm):	
	class Meta:
		model = intervaloCalendarioUMAPS
		fields= ['zona', 'horaInicio', 'horaFinal', 'responsable']

	def clean(self):
		cleaned_data = super().clean()
		hora_inicio = cleaned_data.get("horaInicio")
		hora_final = cleaned_data.get("horaFinal")
		if hora_inicio and hora_final and hora_final < hora_inicio:
			raise forms.ValidationError("La hora final no puede ser antes que la hora de inicio.")
		return cleaned_data
	
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['zona'].queryset = zonasUMAPS.objects.all()
		self.fields['horaInicio'].widget = forms.DateTimeInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M')    
		self.fields['horaFinal'].widget = forms.DateTimeInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M')
		self.fields['responsable'].queryset = perfilEmpleadosUMAPS.objects.all()

	def save(self, commit=True):
		instance = super().save(commit=False)
		perfil_empleado = self.cleaned_data.get('responsable')
		instance.responsable = perfil_empleado
		if commit:
			instance.save()
		return instance
#-------FORM INTERVALO CALENDARIO (apunta a las views.py: agregarIntervalo y mostrarCalendario)--------#
class intervaloCalendarioUMAPSZonaForm(forms.ModelForm):
	class Meta:
		model = intervaloCalendarioUMAPS
		fields = ['horaInicio', 'horaFinal']
	
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['horaInicio'].widget = forms.DateTimeInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M')
		self.fields['horaFinal'].widget = forms.DateTimeInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M')

	def clean(self):
		cleaned_data = super().clean()
		hora_inicio = cleaned_data.get('horaInicio')
		hora_final = cleaned_data.get('horaFinal')
		if hora_inicio and hora_final and hora_inicio >= hora_final:
			raise forms.ValidationError("La hora de inicio debe ser anterior a la hora final")
		return cleaned_data
#------------------FORM REGISTRO ZONAS (apunta a la views.py: paneldecontrol)--------------------------#
class registrozonasUMAPSForm(forms.ModelForm):
	class Meta:
		model = zonasUMAPS
		fields = ['nombre','nombre_bomba', 'activo']
		labels = {
            'nombre': 'Nombre de la zona',
            'nombre_bomba': 'Nombre de la bomba',
            'activo': 'Activo',
        }