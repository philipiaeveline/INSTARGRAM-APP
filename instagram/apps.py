from django.apps import AppConfig


class InstagramConfig(AppConfig):
    name = 'instagram'

     def ready(self):
        import instagram.signals

