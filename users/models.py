from django.db import models
from django.apps import apps  # Import apps to dynamically reference models

class User(models.Model):
    uid = models.CharField(max_length=255, unique=True)  # Store Firebase UID, unique for each user
    email = models.EmailField(unique=True)  # Store the user's email, unique

    def __str__(self):
        return f"{self.uid} ({self.email})"

    def delete(self, *args, **kwargs):
        # Dynamically get the ViewHistory models to avoid circular imports
        ViewHistory = apps.get_model('user_view_history', 'ViewHistory')
        ContinueWatchingViewHistory = apps.get_model('continue_watching', 'ViewHistory')  # Fixed typo

        # Delete related data in user_view_history
        ViewHistory.objects.filter(user=self).delete()

        # Delete related data in continue_watching
        ContinueWatchingViewHistory.objects.filter(user=self).delete()

        # Call the parent class's delete method
        super().delete(*args, **kwargs)