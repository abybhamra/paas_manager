from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from rest_framework import serializers

from .models import Resource, User


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    password = serializers.CharField()
    quota = serializers.IntegerField()

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data.get('password'))
        return super(UserSerializer, self).create(validated_data)

    class Meta:
        model = get_user_model()
        fields = ('id', 'email', 'password', 'quota')


class ResourceSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.email')

    class Meta:
        model = Resource
        fields = ('user', 'uuid')


class ResourceAdminSerializer(serializers.ModelSerializer):
    user = serializers.ChoiceField(choices=[u.email for u in User.objects.all()])

    class Meta:
        model = Resource
        fields = ('user', 'uuid')
