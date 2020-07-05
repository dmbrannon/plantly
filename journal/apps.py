from django.apps import AppConfig


class JournalConfig(AppConfig):
    name = 'journal'

    def ready(self):
        import journal.signals