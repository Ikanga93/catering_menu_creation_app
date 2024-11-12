from django.apps import AppConfig


class MenuManagementConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'menu_management'

    def ready(self):
        import menu_management.signals