from django.apps import AppConfig

class MiappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'aplicaciones.miapp'
    verbose_name = 'perfiles'

    def ready(self):
        import aplicaciones.miapp.signals
