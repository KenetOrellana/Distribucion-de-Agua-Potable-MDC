import datetime
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

#--------------------------MODELO PERFIL EMPLEADOS UMAPS-----------------------------------#
class perfilEmpleadosUMAPS(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile', verbose_name='Perfil de Usuario UMAPS')
    def __str__(self):
        return f'Perfil de {self.user.username}'
    class Meta:
        verbose_name_plural = 'Perfil de Empleados UMAPS'
        ordering = ['-id']

    def perfilEmpleadosUMAPSesSuperUsuario(self):
        return self.user.is_superuser

def crearperfilEmpleadosUMAPS(sender, instance, created, **kawards):
    if created:
        perfilEmpleadosUMAPS.objects.create(user=instance)

def guardarperfilEmpleadosUMAPS(sender, instance, **kawards):
    instance.profile.save()

post_save.connect(crearperfilEmpleadosUMAPS, sender=User)
post_save.connect(guardarperfilEmpleadosUMAPS, sender=User)
#--------------------------------MODELO ZONAS UMAPS-----------------------------------------#
class zonasUMAPS(models.Model):
    nombre = models.CharField(verbose_name='Nombre de la zona', max_length=50)
    nombre_bomba = models.CharField(verbose_name='Nombre de la bomba', max_length=50)
    activo = models.BooleanField()
    class Meta:
        verbose_name_plural = 'Zonas de Distribución UMAPS'
    def __str__(self):
        return self.nombre
#-------------------------MODELO INTERVALOS DEL CALENDARIO----------------------------------#
class intervaloCalendarioUMAPS(models.Model):
    zona = models.ForeignKey(zonasUMAPS, on_delete=models.CASCADE, verbose_name='Zona', default='')
    horaInicio = models.DateTimeField(verbose_name='Hora de apertura bomba')
    horaFinal = models.DateTimeField(verbose_name='Hora de cierre bomba')
    responsable = models.ForeignKey(perfilEmpleadosUMAPS, on_delete=models.CASCADE, verbose_name='Responsable', default='')
    class Meta:
        verbose_name_plural = 'Intervalo de Calendario Zonas UMAPS'
    def __str__(self) -> str:
        return f"Intervalo de la zona {self.zona}: {self.horaInicio} - {self.horaFinal}"
#----------------------------MODELO REGISTRO DE ACTIVIDAD-----------------------------------#
class registroActividadUMAPS(models.Model):
    zona = models.ForeignKey(zonasUMAPS, on_delete=models.CASCADE)
    activacion = models.BooleanField(default=False)
    tiempo = models.DateTimeField(auto_now=True)
    responsable = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'Registro de Actividad de Bombas en Zonas UMAPS'

    def __str__(self):
        return f"[{self.tiempo}] Estado de {self.zona} cambiado a {self.activacion} por {self.responsable}."

    def save(self, *args, **kwargs):
        if not self.pk:
            self.tiempo = datetime.datetime.now()
        super().save(*args, **kwargs)