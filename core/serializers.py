from rest_framework import serializers
from .models import Task
from django.contrib.auth.models import User


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        exclude = ("user",)

    def create(self, validated_data):
        user_id = self.context['request'].user.pk
        print(user_id)
        validated_data['user'] = User.objects.get(pk=user_id)
        return super(TaskSerializer, self).create(validated_data)
