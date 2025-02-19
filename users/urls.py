from django.urls import path
from .views import current_user_view

urlpatterns = [
    path('current/', current_user_view, name='current_user'),
]
