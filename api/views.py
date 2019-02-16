from django.contrib.auth import get_user_model
from rest_framework import viewsets
from rest_framework.authentication import SessionAuthentication
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated

from api.permissions import IsAdminUser
from .models import Resource
from .serializers import ResourceSerializer
from .serializers import UserSerializer

UserModel = get_user_model()


@authentication_classes((SessionAuthentication,))
@permission_classes((IsAdminUser,))
class UserViewSet(viewsets.ModelViewSet):
    queryset = UserModel.objects.all()
    serializer_class = UserSerializer


@authentication_classes((SessionAuthentication,))
@permission_classes((IsAuthenticated,))
class ResourceViewSet(viewsets.ModelViewSet):
    queryset = Resource.objects.all()
    serializer_class = ResourceSerializer

    def get_queryset(self):
        queryset = Resource.objects.all()
        if not self.request.user.is_admin:
            queryset = queryset.filter(user=self.request.user)
        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
