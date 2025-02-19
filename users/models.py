from django.db import models

class User(models.Model):
    uid = models.CharField(max_length=255, unique=True)  # Store Firebase UID, unique for each user
    email = models.EmailField(unique=True)  # Store the user's email, unique

    def __str__(self):
        return f"{self.uid} ({self.email})"

    # class Meta:
    #     # You can specify additional options here if needed
    #     verbose_name = "uid"
    #     verbose_name_plural = "Users"
