from django.apps import AppConfig


class KeepmainConfig(AppConfig):
    name = 'keepmain'

    def ready(self):
        import keepmain.signals