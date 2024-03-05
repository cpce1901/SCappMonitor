from django.apps import AppConfig


class LecturesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.lectures'

    def ready(self):
        from. import signals
       