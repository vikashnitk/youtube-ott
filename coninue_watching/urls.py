from django.urls import path
from .views import UserFilteredDataView

urlpatterns = [
    path('user_filter_video/', UserFilteredDataView.as_view(), name='user_filter_video'),
    path('delete/<int:pk>/', UserFilteredDataView.as_view(), name='delete_user_video'),
]
