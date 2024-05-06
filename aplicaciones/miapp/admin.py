from django.contrib import admin
from .models import perfilEmpleadosUMAPS, zonasUMAPS, registroActividadUMAPS, intervaloCalendarioUMAPS

#--------------------------------------------------------------------------------#
@admin.register(perfilEmpleadosUMAPS)
class mostrardetallezonasUMAPS(admin.ModelAdmin):
    list_display = ('id', 'user_id', 'user')
#--------------------------------------------------------------------------------#
@admin.register(zonasUMAPS)
class mostrardetallezonasUMAPS(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'nombre_bomba', 'activo')
#--------------------------------------------------------------------------------#
@admin.register(registroActividadUMAPS)
class mostrardetallezonasUMAPS(admin.ModelAdmin):
    list_display = ('id', 'zona', 'activacion', 'tiempo', 'responsable')
#--------------------------------------------------------------------------------#
@admin.register(intervaloCalendarioUMAPS)
class mostrardetalleintervaloCalendarioUMAPS(admin.ModelAdmin):
    list_display = ('id','horaInicio', 'horaFinal', 'responsable_id', 'zona_id', 'zona', 'responsable')
#--------------------------------------------------------------------------------#
admin.site.site_header = 'UMAPS'