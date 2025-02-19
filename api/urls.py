from django.urls import path
from .views import MovieModelList, EpisodeModelList, SearchModelList

urlpatterns = [
    # path('movies/', MovieModelList.as_view(), name='movie-list'),  # Endpoint for movies
    path('movies/<str:title>/', MovieModelList.as_view(), name='movie-search'),  # Search movies by title
    path('episodes/<str:show_title>/<int:season_number>/', EpisodeModelList.as_view(), name='episode-list'),  # Endpoint for episodes
    path('search/', SearchModelList.as_view(), name='search'),  # Search for movies and TV shows
]
