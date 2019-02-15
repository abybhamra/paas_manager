from django.urls import path, include
from rest_framework import routers

from api.views import ResourceViewSet
from api.views import UserViewSet

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'resources', ResourceViewSet)

urlpatterns = [
    path('', include(router.urls))
]
