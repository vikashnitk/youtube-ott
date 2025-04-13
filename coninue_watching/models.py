from django.db import models
from users.models import User  # Reference the User model
from api.models import Movie, Episode  # Import Movie and Episode models

class ContinueWatchingViewHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Reference the User model
    movie = models.ForeignKey(Movie, null=True, blank=True, on_delete=models.CASCADE)  # Optional ForeignKey to Movie
    episode = models.ForeignKey(Episode, null=True, blank=True, on_delete=models.CASCADE)  # Optional ForeignKey to Episode
    play_time = models.IntegerField()  # Store play time in seconds
    timestamp = models.DateTimeField(auto_now=True)  # Timestamp when the data was received

    def __str__(self):
        if self.movie:
            return f"User: {self.user.email}, Movie: {self.movie.title}, Time: {self.play_time}s"
        if self.episode:
            return f"User: {self.user.email}, Episode: {self.episode.title}, Time: {self.play_time}s"
        return f"User: {self.user.email}, No video, Time: {self.play_time}s"