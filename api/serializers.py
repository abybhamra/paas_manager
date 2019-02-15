from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from rest_framework import serializers

from .models import Resource


class UserSerializer(serializers.ModelSerializer):
    resources = serializers.PrimaryKeyRelatedField(many=True, queryset=Resource.objects.all())

    class Meta:
        model = get_user_model()
        fields = ('id', 'username', 'email', 'resources')


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')


class ResourceSerializer(serializers.ModelSerializer):
    email = serializers.ReadOnlyField(source='user.email')

    class Meta:
        model = Resource
        fields = ('email', 'uuid')
