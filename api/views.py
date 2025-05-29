from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework.views import APIView
from .models import Movie, TVShow, Episode
from .serializers import MovieSerializer, TVShowSerializer, EpisodeSerializer
from firebase_config.auth import FirebaseAuthentication

class MovieModelList(APIView):
    serializer_class = MovieSerializer
    authentication_classes = [FirebaseAuthentication]
    def get(self, request, *args, **kwargs):
        title = self.kwargs.get('title', '').strip()
        user = request.user
        user_age = user.age if hasattr(user, 'age') else '13'
        queryset = Movie.objects.filter(
            title__icontains=title,
            age_rating__lte=user_age
        )

        if not queryset.exists():
            raise NotFound(f"No movies found with title '{title}'.")

        serializer = MovieSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class TVShowModelList(generics.ListAPIView):
    serializer_class = TVShowSerializer
    authentication_classes = [FirebaseAuthentication]

    def get(self, request, *args, **kwargs):
        title = self.kwargs.get('title', '').strip()
        user = request.user
        user_age = user.age if hasattr(user, 'age') else '13'
        queryset = TVShow.objects.filter(
            title__icontains=title,
            age_rating__lte=user_age
        )

        if not queryset.exists():
            raise NotFound(f"No TV shows found with title '{title}'.")

        serializer = TVShowSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class EpisodeModelList(generics.ListAPIView):
    serializer_class = EpisodeSerializer
    authentication_classes = [FirebaseAuthentication]

    def get(self, request, *args, **kwargs):
        try:
            show_title = self.kwargs.get('show_title', '').strip()
            season_number = int(self.kwargs.get('season_number'))
            user = request.user
            user_age = user.age if hasattr(user, 'age') else '13'
            print(f"User age: {user_age}")  # Debugging line to check user age
            queryset = Episode.objects.filter(
                tv_show__title__iexact=show_title, 
                season_number=season_number, 
                tv_show__age_rating__lte=user_age
            )
            print(f"Queryset: {queryset}")  # Debugging line to check the queryset

            if not queryset.exists():
                raise NotFound(f"No episodes found for '{show_title}' season {season_number}.")

            serializer = EpisodeSerializer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

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
    authentication_classes = [FirebaseAuthentication]
    
    def get(self, request, *args, **kwargs):
        query = request.query_params.get('q', '').strip()
        user = request.user
        user_age = user.age if hasattr(user, 'age') else '13'
        movies = Movie.objects.filter(
            title__icontains=query,
            age_rating__lte=user_age
        )
        tv_shows = TVShow.objects.filter(
            title__icontains=query,
            age_rating__lte=user_age
        )

        movies_serializer = MovieSerializer(movies, many=True)
        tv_shows_serializer = TVShowSerializer(tv_shows, many=True)

        return Response({
            'movies': movies_serializer.data,
            'tv_shows': tv_shows_serializer.data
        }, status=status.HTTP_200_OK)
