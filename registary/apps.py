from django.apps import AppConfig


class RegistaryConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'registary'

    def ready(self):
        import registary.signals
