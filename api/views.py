from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from .models import Movie, TVShow, Episode
from .serializers import MovieSerializer, TVShowSerializer, EpisodeSerializer
from firebase_admin import auth
from rest_framework.authentication import BaseAuthentication
from firebase_config.auth import FirebaseAuthentication
from users.models import User

# class FirebaseAuthentication(BaseAuthentication):
#     def authenticate(self, request):
#         auth_header = request.headers.get('Authorization')
#         if not auth_header or not auth_header.startswith('Bearer '):
#             return None

#         id_token = auth_header.split('Bearer ')[1]
#         try:
#             # Decode and verify the Firebase token
#             decoded_token = auth.verify_id_token(id_token)
#             uid = decoded_token['uid']

#             # Get or create the user using your custom model's identifier (e.g., 'uid' or 'email')
#             user, _ = User.objects.get_or_create(uid=uid)

#             # Return the user object and None for the token
#             return (user, None)
#         except Exception as e:
#             print(f"Authentication failed: {e}")
#             return None

class MovieModelList(generics.ListAPIView):
    serializer_class = MovieSerializer
    authentication_classes = [FirebaseAuthentication]

    def get_queryset(self):
        title = self.kwargs.get('title', '').strip()
        user = self.request.user
        user = User.objects.filter(user=user).first()
        user_age = user.age if user else 13
        print(f"User age: {user_age}")

        queryset = Movie.objects.filter(
            title__icontains=title,
            age_rating__lte=user_age
        )
        # print(f"Queryset for movie '{title}': {queryset}")
        if not queryset.exists():
            raise NotFound(f"No movies found with title '{title}'.")

        return queryset

class TVShowModelList(generics.ListAPIView):
    serializer_class = TVShowSerializer
    authentication_classes = [FirebaseAuthentication]

    def get_queryset(self):
        title = self.kwargs.get('title', '').strip()
        user = self.request.user
        user = User.objects.filter(user=user).first()
        user_age = user.age if user else 13
        print(f"User age: {user_age}")

        queryset = TVShow.objects.filter(
            title__icontains=title,
            age_rating__lte=user_age
        )
        # print(f"Queryset for tvshow '{title}': {queryset}")
        if not queryset.exists():
            raise NotFound(f"No TV shows found with title '{title}'.")

        return queryset

class EpisodeModelList(generics.ListAPIView):
    serializer_class = EpisodeSerializer
    authentication_classes = [FirebaseAuthentication]

    def get_queryset(self):
        try:
            show_title = self.kwargs.get('show_title', '').strip()
            user = self.request.user
            user = User.objects.filter(user=user).first()
            user_age = user.age if user else 13
            season_number = int(self.kwargs.get('season_number'))

            queryset = Episode.objects.filter(
                tv_show__title__iexact=show_title, 
                season_number=season_number, 
                tv_show__age_rating__lte=user_age
            )
            # print(f"Queryset for tvshow '{show_title}': {queryset}")
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
    authentication_classes = [FirebaseAuthentication]
    
    def get(self, request, *args, **kwargs):
        query = request.query_params.get('q', '').strip()

        user = self.request.user
        user = User.objects.filter(user=user).first()
        user_age = user.age if user else 13

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
