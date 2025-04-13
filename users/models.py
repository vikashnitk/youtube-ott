from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from user_view_history.models import ViewHistory
from coninue_watching.models import ViewHistory as ContinueWatchingViewHistory  # Adjust if the model name differs

class User(models.Model):
    uid = models.CharField(max_length=255, unique=True)  # Store Firebase UID, unique for each user
    email = models.EmailField(unique=True)  # Store the user's email, unique

    def __str__(self):
        return f"{self.uid} ({self.email})"

@receiver(pre_delete, sender=User)
def delete_user_related_data(sender, instance, **kwargs):
    # Delete related data in user_view_history
    ViewHistory.objects.filter(user=instance).delete()

    # Delete related data in coninue_watching
    ContinueWatchingViewHistory.objects.filter(user=instance).delete()