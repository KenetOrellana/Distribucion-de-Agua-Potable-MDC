from django.urls import path
from . import views

urlpatterns = [
    path('', views.bienvenida, name='bienvenida'), #Redirecciona a la página de bienvenida (welcome)
    path("index/", views.index, name="index"), #Redirecciona a la página principal del usuario logueado dentro del sistema (index)
    #path("verform/", views.verform, name="verform"), #Redirecciona a la página del registro de usuarios (modelform)
    path("signup/", views.signup, name="signup"), #Redirecciona a la página del registro de empleados (modelform)
    path("login/", views.login, name="login"), #Redirecciona a la página de inicio de sesión (login)
    path("logout/", views.logout, name="logout"), #Redirecciona a la página de cierre de sesión (logout)
    path("paneldecontrol/<int:zona_id>/", views.paneldecontrol, name="paneldecontrol"), #Redirecciona a la página de inicio de sesión (login)
    path("agregarintervalo/", views.agregarIntervalo, name="agregarintervalo"),
    path("mostrarcalendario/", views.mostrarCalendario, name="mostrarcalendario"),
    path("accesodenegado/", views.accesodenegado, name="accesodenegado")
]