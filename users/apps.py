from django.apps import AppConfig


class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'

    def ready(self):
        from firebase_config.firestore import listen_for_user_deletions
        listen_for_user_deletions()
