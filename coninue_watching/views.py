from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import APIException
from rest_framework.authentication import BaseAuthentication
from firebase_admin import auth
from rest_framework.views import APIView
from user_view_history.models import ViewHistory
from api.models import Movie, Episode
from django.db.models import Max
from users.models import User
from django.conf import settings

class FirebaseAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return None

        id_token = auth_header.split('Bearer ')[1]
        try:
            decoded_token = auth.verify_id_token(id_token)
            uid = decoded_token['uid']
            user, _ = User.objects.get_or_create(uid=uid)
            return (user, None)
        except Exception as e:
            print(f"Authentication failed: {e}")
            return None

class UserFilteredDataView(APIView):
    authentication_classes = [FirebaseAuthentication]

    def get(self, request):
        user = request.user
        if not user:
            return Response(
                {"detail": "Authentication credentials were not provided."},
                status=401
            )

        history = ViewHistory.objects.filter(user=user)
        video_data = []
        latest_episodes = {}

        for entry in history:
            if entry.movie:
                movie_data = Movie.objects.filter(title=entry.movie).first()                
                if movie_data:
                    total_duration = movie_data.duration
                    cutoff_duration = movie_data.cutoff_duration
                    play_time = entry.play_time
                    if play_time<=(total_duration-cutoff_duration): 
                        # print(f"entry.id:{entry.id}")                   
                        video_data.append({
                            "id": entry.id,
                            "type": "movie",
                            "video_url": movie_data.video_url,
                            "play_time": play_time,
                            # 'total_duration': movie_data.duration,
                            'cutoff_duration': cutoff_duration,
                            "thumbnail": f"{movie_data.thumbnail_movie}",
                            "name": entry.movie.title
                        })

            if entry.episode:
                episode_data = Episode.objects.filter(title=entry.episode.title).first()
                if episode_data:
                    tvshow_data = episode_data.tv_show
                    if tvshow_data.title not in latest_episodes:
                        latest_episode = ViewHistory.objects.filter(
                            user=user, episode__tv_show=tvshow_data
                        ).order_by('-timestamp').first()

                        if latest_episode:
                            latest_episodes[tvshow_data.title] = latest_episode
                            latest_episode_data = latest_episode.episode

                            total_duration = latest_episode_data.duration
                            cutoff_duration = latest_episode_data.cutoff_duration
                            play_time = latest_episode.play_time
                            if play_time<=(total_duration-cutoff_duration): 
                                video_data.append({
                                    "id": latest_episode.id,
                                    "type": "tvshow",
                                    "video_url": latest_episode_data.video_url,
                                    "play_time": play_time,
                                    "thumbnail": f"{tvshow_data.thumbnail_tvshow}",
                                    "name": tvshow_data.title,
                                    "episode_title": latest_episode_data.title,
                                    "cutoff_duration": cutoff_duration
                                    # sample comment
                                })

        return Response(video_data, status=200)

    def delete(self, request, pk=None):
        user = request.user
        if not user:
            return Response(
                {"detail": "Authentication credentials were not provided."},
                status=401
            )

        try:
            # Find the item in the user's view history by ID
            entry = ViewHistory.objects.filter(user=user, id=pk).first()
            # print(f"entry: {entry}")

            if entry:
                if entry.episode:
                    # If the entry is associated with an episode, delete all entries for the same TV show
                    tv_show = entry.episode.tv_show
                    if tv_show:
                        ViewHistory.objects.filter(user=user, episode__tv_show=tv_show).delete()
                        return Response(
                            {"detail": f"All episodes for TV show '{tv_show.title}' deleted successfully."},
                            status=204
                        )
                elif entry.movie:
                    # If the entry is a movie, delete only the movie entry
                    entry.delete()
                    return Response({"detail": "Movie entry deleted successfully."}, status=204)
            else:
                return Response({"detail": "Item not found."}, status=404)

        except Exception as e:
            print(f"Error deleting item: {e}")
            return Response({"detail": "An error occurred while deleting the item."}, status=500)
