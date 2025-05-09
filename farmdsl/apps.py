from django.apps import AppConfig


class FarmdslConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "farmdsl"

    def ready(self):
        from django.db.models.signals import post_migrate
        from farmdsl.signals import create_elasticsearch_index
        post_migrate.connect(create_elasticsearch_index, sender=self)
