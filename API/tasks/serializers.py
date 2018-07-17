from datetime import datetime
from rest_framework import serializers

from .models import Task


class TaskSerializer(serializers.ModelSerializer):

    owner = serializers.StringRelatedField()

    class Meta:
        model = Task
        fields = ('name', 'content', 'finished', 'start', 'owner', )
        read_only_fields = ('owner', )


class TaskCreateSerializer(serializers.ModelSerializer):
    owner = serializers.StringRelatedField()

    class Meta:
        model = Task
        fields = ('name', 'content', 'start', 'owner', 'finished')
        read_only_fields = ('owner', 'finished',)

    def validate(self, attrs):
        if attrs['start'].replace(tzinfo=None) < datetime.now():
            raise serializers.ValidationError('Bad date of start task', 400)
        else:
            return attrs
