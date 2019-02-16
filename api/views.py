from django.contrib.auth import get_user_model
from rest_framework import viewsets
from rest_framework.authentication import SessionAuthentication
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated

from api.permissions import IsAdminUser
from api.serializers import ResourceAdminSerializer
from .models import Resource
from .serializers import ResourceSerializer
from .serializers import UserSerializer

UserModel = get_user_model()


@authentication_classes((SessionAuthentication,))
@permission_classes((IsAuthenticated, IsAdminUser))
class UserViewSet(viewsets.ModelViewSet):
    queryset = UserModel.objects.all()
    serializer_class = UserSerializer

    def get_queryset(self):
        queryset = UserModel.objects.all()
        if not self.request.user.is_admin:
            queryset = queryset.filter(id=self.request.user.id)
        return queryset


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

    def get_serializer_class(self):
        if self.request.user.is_admin:
            return ResourceAdminSerializer
        return ResourceSerializer

    def perform_create(self, serializer):
        owner = self._get_owner()
        serializer.save(user=owner)

    def _get_owner(self):
        owner = self.request.user
        post_param_owner_email = self.request.POST.get("user")
        if owner.is_admin and owner.email != post_param_owner_email:
            owner = UserModel.objects.get(email=post_param_owner_email)
        return owner
