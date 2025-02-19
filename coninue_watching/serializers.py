# serealizers.py
from rest_framework import serializers
from api.models import Movie, Episode, TVShow
from user_view_history.models import ViewHistory


class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ['id', 'title', 'video_url', 'description', 'thumbnail_movie']


class TVShowSerializer(serializers.ModelSerializer):
    class Meta:
        model = TVShow
        fields = ['id', 'title']


class EpisodeSerializer(serializers.ModelSerializer):
    tvshow = TVShowSerializer(read_only=True)  # Assuming Episode has a ForeignKey to TVShow

    class Meta:
        model = Episode
        fields = ['id', 'title', 'video_url', 'description', 'tvshow']


class ViewHistorySerializer(serializers.ModelSerializer):
    movie = MovieSerializer(read_only=True)
    episode = EpisodeSerializer(read_only=True)

    class Meta:
        model = ViewHistory
        fields = ['id', 'user_id', 'movie', 'episode', 'play_time']
