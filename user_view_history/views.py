import firebase_admin
from firebase_admin import auth, credentials
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import BaseAuthentication
from rest_framework import status
from api.models import Movie, Episode
from .models import ViewHistory
from .serializers import ViewHistorySerializer
from users.models import User

# Initialize Firebase Admin SDK (run this only once, e.g., in settings.py)
# if not firebase_admin._apps:
#     cred = credentials.Certificate("path/to/your-firebase-adminsdk.json")
#     firebase_admin.initialize_app(cred)

class FirebaseAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return None

        id_token = auth_header.split('Bearer ')[1]
        try:
            # Decode and verify the Firebase token
            decoded_token = auth.verify_id_token(id_token)
            uid = decoded_token['uid']

            # Get or create the user using your custom model's identifier (e.g., 'uid' or 'email')
            user, _ = User.objects.get_or_create(uid=uid)

            # Return the user object and None for the token
            return (user, None)
        except Exception as e:
            print(f"Authentication failed: {e}")
            return None

class TrackVideoView(APIView):
    authentication_classes = [FirebaseAuthentication]
    # permission_classes = [IsAuthenticated]

    def post(self, request):
        print(f"Authenticated user UID: {request.user}")

        video_url = request.data.get('video_url')
        play_time = request.data.get('play_time')
        # print(f"video_url: {video_url}")
        # print(f"play_time: {play_time}")

        if not video_url or not play_time:
            return Response({"error": "video_url and play_time are required"}, status=status.HTTP_400_BAD_REQUEST)

        # Check if video_url corresponds to a Movie or Episode
        movie = Movie.objects.filter(video_url=video_url).first()
        episode = Episode.objects.filter(video_url=video_url).first()
        # print(f"movie:{movie}")
        # print(f"episode:{episode}")

        if movie:
            # Create or update the user's view history for a movie
            view_history, created = ViewHistory.objects.update_or_create(
                user=request.user,
                movie=movie,
                defaults={'play_time': play_time},
            )
        elif episode:
            # Create or update the user's view history for an episode
            view_history, created = ViewHistory.objects.update_or_create(
                user=request.user,
                episode=episode,
                defaults={'play_time': play_time},
            )
        else:
            return Response({"error": "Invalid video_url, no Movie or Episode found"}, status=status.HTTP_404_NOT_FOUND)

        # Return the serialized response
        serializer = ViewHistorySerializer(view_history)
        return Response(serializer.data, status=status.HTTP_200_OK)
