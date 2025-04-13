from django.db import models
from user_view_history.models import ViewHistory
from coninue_watching.models import ViewHistory as ContinueWatchingViewHistory  # Adjust if the model name differs

class User(models.Model):
    uid = models.CharField(max_length=255, unique=True)  # Store Firebase UID, unique for each user
    email = models.EmailField(unique=True)  # Store the user's email, unique

    def __str__(self):
        return f"{self.uid} ({self.email})"

    def delete(self, *args, **kwargs):
        # Delete related data in user_view_history
        ViewHistory.objects.filter(user=self).delete()

        # Delete related data in coninue_watching
        ContinueWatchingViewHistory.objects.filter(user=self).delete()

        # Call the parent class's delete method
        super().delete(*args, **kwargs)