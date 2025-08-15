from rest_framework import serializers
from .models import Movie, TVShow, Episode, Genre

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['id', 'name']  # Serialize only the essential fields


class MovieSerializer(serializers.ModelSerializer):
    genres = GenreSerializer(many=True)  # Nested genre serializer
    # thumbnail_movie = serializers.SerializerMethodField()

    class Meta:
        model = Movie
        fields = [
            'id', 'title', 'description', 'genres', 'release_year', 
            'video_url','duration','cutoff_duration', 'age_rating'
        ]

    # def get_thumbnail_movie(self, obj):
    #     return obj.thumbnail_movie.name if obj.thumbnail_movie else None


class TVShowSerializer(serializers.ModelSerializer):
    genres = GenreSerializer(many=True)  # Nested genre serializer
    # thumbnail_tvshow = serializers.SerializerMethodField()

    class Meta:
        model = TVShow
        fields = [
            'id', 'title', 'description', 'genres', 'release_year', 
            'number_of_seasons','age_rating','trailer'
        ]

    # def get_thumbnail_tvshow(self, obj):
    #     return obj.thumbnail_tvshow.name if obj.thumbnail_tvshow else None

class EpisodeSerializer(serializers.ModelSerializer):
    tv_show = serializers.StringRelatedField()  # Display TV show title instead of ID
    tv_show_details = TVShowSerializer(source='tv_show', read_only=True)  # Nested TV show details
    total_seasons = serializers.SerializerMethodField()
    next_episode = serializers.SerializerMethodField()  # New field for next episode details

    class Meta:
        model = Episode
        fields = [
            'id', 'tv_show', 'season_number', 'episode_number', 'title',
            'video_url', 'tv_show_details',
            'total_seasons', 'next_episode','duration','cutoff_duration','age_rating','trailer'
        ]

    def get_total_seasons(self, obj):
        """Calculate the total number of distinct seasons for the TV show."""
        return (
            Episode.objects.filter(tv_show=obj.tv_show)
            .values('season_number')
            .distinct()
            .count()
        )

    def get_next_episode(self, obj):
        """Retrieve the next episode within the same season."""
        next_episode = (
            Episode.objects.filter(tv_show=obj.tv_show, season_number=obj.season_number)
            .filter(episode_number__gt=obj.episode_number)
            .order_by('episode_number')
            .first()
        )

        if next_episode:
            return {
                'episode_number': next_episode.episode_number,
                'video_url': next_episode.video_url
            }
        else:
            return {'episode_number': None, 'video_url': None}  # No next episode

