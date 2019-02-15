from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from api.views import ResourceViewSet

resources_list = ResourceViewSet.as_view({'get': 'list'})
resource_details = ResourceViewSet.as_view({'get': 'retrieve',
                                            'put': 'update',
                                            'patch': 'partial_update',
                                            'delete': 'destroy'})
urlpatterns = format_suffix_patterns([
    path('resources/', resources_list, name='resources-list'),
    path('resources/<str:pk>/', resource_details, name='resource-details')
])
