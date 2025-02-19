from django.contrib import admin
from .models import Movie, TVShow, Episode, Genre
from django.utils.html import format_html

@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'release_year', 'genre_list', 'thumbnail_preview')
    search_fields = ('title', 'genres__name')
    list_filter = ('release_year', 'genres')
    readonly_fields = ('thumbnail_preview',)

    fieldsets = (
        (None, {
            'fields': (
                'title', 'description', 'genres', 'release_year',
                'video_url', 'thumbnail_movie', 'thumbnail_preview'
            ),
        }),
    )

    def genre_list(self, obj):
        return ", ".join([genre.name for genre in obj.genres.all()])
    genre_list.short_description = 'Genres'

    def thumbnail_preview(self, obj):
        if obj.thumbnail_movie:
            return format_html(f'<img src="{obj.thumbnail_movie.url}" height="50" />')
        return "No Thumbnail"
    thumbnail_preview.short_description = 'Thumbnail'


@admin.register(TVShow)
class TVShowAdmin(admin.ModelAdmin):
    list_display = ('title', 'release_year', 'number_of_seasons', 'genre_list', 'thumbnail_preview')
    search_fields = ('title', 'genres__name')
    list_filter = ('release_year', 'genres')
    readonly_fields = ('thumbnail_preview',)

    fieldsets = (
        (None, {
            'fields': (
                'title', 'description', 'genres', 'release_year',
                'number_of_seasons', 'thumbnail_tvshow', 'thumbnail_preview'
            ),
        }),
    )

    def genre_list(self, obj):
        return ", ".join([genre.name for genre in obj.genres.all()])
    genre_list.short_description = 'Genres'

    def thumbnail_preview(self, obj):
        if obj.thumbnail_tvshow:
            return format_html(f'<img src="{obj.thumbnail_tvshow.url}" height="50" />')
        return "No Thumbnail"
    thumbnail_preview.short_description = 'Thumbnail'


@admin.register(Episode)
class EpisodeAdmin(admin.ModelAdmin):
    list_display = (
        'tv_show', 'season_number', 'episode_number', 'title',
        'video_url', 'thumbnail_preview'
    )
    search_fields = ('tv_show__title', 'title')
    list_filter = ('season_number', 'tv_show')
    readonly_fields = ('thumbnail_preview',)

    fieldsets = (
        (None, {
            'fields': (
                'tv_show', 'season_number', 'episode_number', 'title',
                'video_url', 'thumbnail_episode', 'thumbnail_preview'
            ),
        }),
    )

    def thumbnail_preview(self, obj):
        if obj.thumbnail_episode:
            return format_html(f'<img src="{obj.thumbnail_episode.url}" height="50" />')
        return "No Thumbnail"
    thumbnail_preview.short_description = 'Thumbnail'
