# models.py
from django.db import models

class Genre(models.Model):
    name = models.CharField(max_length=50, unique=True, default="General")

    def __str__(self):
        return self.name

class Movie(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    genres = models.ManyToManyField(Genre, related_name='movies')  # Many-to-many relationship
    release_year = models.IntegerField()
    thumbnail_movie = models.ImageField(upload_to='thumbnails/movies/', null=True, blank=True)
    video_url = models.URLField()
    duration = models.IntegerField()
    cutoff_duration = models.IntegerField()
    age_rating = models.IntegerField()
    trailer = models.URLField(null=True, blank=True)

    def __str__(self):
        return self.title

class TVShow(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(default="No description available")
    genres = models.ManyToManyField(Genre, related_name='tvshows')  # Many-to-many relationship
    release_year = models.IntegerField()
    thumbnail_tvshow = models.ImageField(upload_to='thumbnails/tvshows/', null=True, blank=True)
    number_of_seasons = models.IntegerField(default=1)
    age_rating = models.IntegerField()
    trailer = models.URLField(null=True, blank=True)

    def __str__(self):
        return self.title

class Episode(models.Model):
    tv_show = models.ForeignKey(TVShow, on_delete=models.CASCADE)
    season_number = models.IntegerField()
    episode_number = models.IntegerField()
    title = models.CharField(max_length=255)
    thumbnail_episode = models.ImageField(upload_to='thumbnails/episodes/', null=True, blank=True)
    video_url = models.URLField()
    duration = models.IntegerField()
    cutoff_duration = models.IntegerField()

    @property
    def age_rating(self):
        return self.tv_show.age_rating

    def __str__(self):
        return f'{self.tv_show.title} - S{self.season_number}E{self.episode_number}: {self.title}'
