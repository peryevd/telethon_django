from rest_framework_json_api import serializers

from .models import ChannelInfo


class ChannelInfoSerializer(serializers.ModelSerializer):

    class Meta:
        model = ChannelInfo
        fields = '__all__'

class ArticleSerializer(serializers.Serializer):
    id = serializers.CharField(max_length=120)
    about = serializers.CharField()
    participants_count = serializers.CharField()