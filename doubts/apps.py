from django.apps import AppConfig


class DoubtsConfig(AppConfig):
    name = 'doubts'
    def ready(self):
        import doubts.signals
