from django.apps import AppConfig

class AppCommonConfig(AppConfig):
    name = 'app_common'

    def ready(self):
        import app_common.signals  
