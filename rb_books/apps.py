from django.apps import AppConfig


class RbBooksConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'rb_books'

    def ready(self):
        import rb_books.signals
