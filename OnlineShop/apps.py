from django.apps import AppConfig


class OnlineShopConfig(AppConfig):
    name = 'OnlineShop'

     def ready(self):
        import OnlineShop.signals

