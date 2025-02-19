from rest_framework import serializers
from .models import ViewHistory

class ViewHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ViewHistory
        fields = ['video_url', 'play_time']
