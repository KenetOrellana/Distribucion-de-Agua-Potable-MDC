from django.contrib.auth.models import Group, User, Permission
from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import perfilEmpleadosUMAPS, zonasUMAPS, intervaloCalendarioUMAPS, registroActividadUMAPS
from django.contrib.contenttypes.models import ContentType

#----SEÑAL QUE PERMITE LA ASIGNACIÓN AUTOMÁTICA DEL GRUPO (empleadoUMAPS) y la creación de demás grupos----#
@receiver(post_save, sender=perfilEmpleadosUMAPS)
def agregargrupoEmpleadosUMAPS(sender, instance, created, **kwargs):
    if created:
        try: 
            empleadosUMAPS = Group.objects.get(name='empleadoUMAPS')
        except Group.DoesNotExist:
            empleadosUMAPS = Group.objects.create(name='empleadoUMAPS')
#------------------------AQUÍ SE ASIGNAN LOS PERMISOS AL MODELO (zonasUMAPS)-------------------------------#
            content_type = ContentType.objects.get_for_model(zonasUMAPS)
            permisoszonasUMAPS = Permission.objects.filter(content_type=content_type, codename__in=[
                'view_zonasumaps', 'add_zonasumaps', 'change_zonasumaps'
                ])
            empleadosUMAPS.permissions.add(*permisoszonasUMAPS)

        instance.user.groups.add(empleadosUMAPS)
#-----------------------AQUÍ SE ASIGNAN LOS PERMISOS A LOS 4 MODELOS GENERALES-----------------------------#
@receiver(post_save, sender=perfilEmpleadosUMAPS)
def agregarmasgruposEmpleadosUMAPS(sender, instance, created, **kwargs):
    if created:
        gruposUMAPS = ['administradorUMAPS']
        for administradorUMAPS in gruposUMAPS:
            try: 
                administradoresUMAPS = Group.objects.get(name=administradorUMAPS)
            except Group.DoesNotExist:
                administradoresUMAPS = Group.objects.create(name=administradorUMAPS)
            
            gadministradoresUMAPS = 'administradorUMAPS'
            grupoadministradoresUMAPS, _ = Group.objects.get_or_create(name=gadministradoresUMAPS)

            # [1] Permisos del modelo zonasUMAPS
            mzonasUMAPS = ContentType.objects.get_for_model(zonasUMAPS)
            permisoszonasUMAPS = Permission.objects.filter(content_type=mzonasUMAPS)

            # [2] Permisos del modelo perfilEmpleadosUMAPS
            mperfilEmpleadosUMAPS = ContentType.objects.get_for_model(perfilEmpleadosUMAPS)
            permisosperfilEmpleadosUMAPS = Permission.objects.filter(content_type=mperfilEmpleadosUMAPS)

            # [4] Permisos del modelo intervaloCalendarioUMAPS
            mintervaloCalendarioUMAPS = ContentType.objects.get_for_model(intervaloCalendarioUMAPS)
            permisosintervaloCalendarioUMAPS = Permission.objects.filter(content_type=mintervaloCalendarioUMAPS)

            # [4] Permisos del modelo registroActividadUMAPS
            mregistroActividadUMAPS = ContentType.objects.get_for_model(registroActividadUMAPS)
            permisosregistroActividadUMAPS = Permission.objects.filter(content_type=mregistroActividadUMAPS)

            permisosUMAPS = permisoszonasUMAPS | permisosperfilEmpleadosUMAPS | permisosintervaloCalendarioUMAPS | permisosregistroActividadUMAPS
            grupoadministradoresUMAPS.permissions.add(*permisosUMAPS)
#---------------------SEÑAL QUE PERMITE LA ASIGNACIÓN AUTOMÁTICA DEL PERMISO (is_staff)---------------------#
@receiver(post_save, sender=User)
def permisoisstaffempleadosUMAPS(sender, instance, created, **kwargs):
    if created:
        instance.is_staff = True
        instance.save()