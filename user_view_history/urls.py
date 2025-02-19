from django.urls import path
from .views import TrackVideoView  # Make sure you're importing the class, not a function

urlpatterns = [
    path('track_video/', TrackVideoView.as_view(), name='track_video'),  # Correct usage of .as_view() for a CBV
]
