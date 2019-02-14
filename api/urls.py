from .views import ListUserView
from django.urls import path

urlpatterns = [
    path('users/', ListUserView.as_view(), name='users-all')
    ]