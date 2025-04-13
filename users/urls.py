from django.urls import path
from .views import current_user_view, delete_user_view

urlpatterns = [
    path('current/', current_user_view, name='current_user'),
    path('delete_user/', delete_user_view, name='delete_user'),  # Uncomment if needed
    # path('delete/<str:uid>/', delete_user_view, name='delete_user_by_uid')
]
