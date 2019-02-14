from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from api.views import UserViewSet

user_list = UserViewSet.as_view({'get': 'list'})
user_detail = UserViewSet.as_view({'get': 'retrieve',
                                   'put': 'update',
                                   'patch': 'partial_update',
                                   'delete': 'destroy'})

urlpatterns = format_suffix_patterns([
    path('users/', user_list, name='users-list'),
    path('users/<str:pk>/', user_detail, name='user-details')
])
