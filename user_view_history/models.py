from django.db import models
from users.models import User  # Assuming you are using Django's built-in User model
from api.models import Movie, Episode  # Import Movie and Episode models to link them

class ViewHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Correct the user field to reference User model
    movie = models.ForeignKey(Movie, null=True, blank=True, on_delete=models.CASCADE)  # Optional ForeignKey to Movie
    episode = models.ForeignKey(Episode, null=True, blank=True, on_delete=models.CASCADE)  # Optional ForeignKey to Episode
    play_time = models.IntegerField()  # Store play time in seconds
    timestamp = models.DateTimeField(auto_now=True)  # Timestamp when the data was received

    @property
    def video_url(self):
        """Return video_url depending on whether it is from a Movie or Episode."""
        if self.movie:
            return self.movie.video_url
        if self.episode:
            return self.episode.video_url
        return None  # In case neither is set (this shouldn't happen if the model is used correctly)

    def __str__(self):
        if self.movie:
            return f"User: {self.user.email}, Movie: {self.movie.title}, Time: {self.play_time}s"
        if self.episode:
            return f"User: {self.user.email}, Episode: {self.episode.title}, Time: {self.play_time}s"
        return f"User: {self.user.email}, No video, Time: {self.play_time}s"
