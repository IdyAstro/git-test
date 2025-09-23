from django.apps import AppConfig


class StockAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'stock_app'


def ready(self):
    import stock_app.signals