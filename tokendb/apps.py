from django.apps import AppConfig


class TokendbConfig(AppConfig):
    name = 'tokendb'

    def ready(self):
        import tokendb.signals  # noqa
