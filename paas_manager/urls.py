from django.urls import path, include

urlpatterns = [
    path('api/v1/', include('api.urls')),
    path('api-auth/', include('rest_framework.urls'))
]
