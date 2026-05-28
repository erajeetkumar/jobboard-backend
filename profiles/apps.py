from django.apps import AppConfig


class ProfilesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'profiles'
    verbose_name = 'Profiles'
    
    #signals are imported here to ensure they are registered when the app is ready
    def ready(self):
        import profiles.signals  # Import signals to ensure they are registered
        import profiles.views  # Import views to ensure they are registered
        import profiles.serializers  # Import serializers to ensure they are registered
        import profiles.urls  # Import urls to ensure they are registered