from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from .models import Movie, TVShow, Episode
from .serializers import MovieSerializer, TVShowSerializer, EpisodeSerializer

class MovieModelList(generics.ListAPIView):
    serializer_class = MovieSerializer

    def get_queryset(self):
        title = self.kwargs.get('title', '').strip()
        queryset = Movie.objects.filter(title__icontains=title)

        if not queryset.exists():
            raise NotFound(f"No movies found with title '{title}'.")

        return queryset

class TVShowModelList(generics.ListAPIView):
    serializer_class = TVShowSerializer

    def get_queryset(self):
        title = self.kwargs.get('title', '').strip()
        queryset = TVShow.objects.filter(title__icontains=title)

        if not queryset.exists():
            raise NotFound(f"No TV shows found with title '{title}'.")

        return queryset

class EpisodeModelList(generics.ListAPIView):
    serializer_class = EpisodeSerializer

    def get_queryset(self):
        try:
            show_title = self.kwargs.get('show_title', '').strip()
            season_number = int(self.kwargs.get('season_number'))

            queryset = Episode.objects.filter(
                tv_show__title__iexact=show_title, season_number=season_number
            )

            if not queryset.exists():
                raise NotFound(f"No episodes found for '{show_title}' season {season_number}.")

            return queryset

        except ValueError:
            raise NotFound("Season number must be an integer.")

    def list(self, request, *args, **kwargs):
        try:
            queryset = self.get_queryset()
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"error": f"An error occurred: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

class SearchModelList(generics.ListAPIView):
    """A view to handle searching for movies and TV shows."""
    
    def get(self, request, *args, **kwargs):
        query = request.query_params.get('q', '').strip()
        movies = Movie.objects.filter(title__icontains=query)
        tv_shows = TVShow.objects.filter(title__icontains=query)

        movies_serializer = MovieSerializer(movies, many=True)
        tv_shows_serializer = TVShowSerializer(tv_shows, many=True)

        return Response({
            'movies': movies_serializer.data,
            'tv_shows': tv_shows_serializer.data
        }, status=status.HTTP_200_OK)
