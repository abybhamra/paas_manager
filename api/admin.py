from django.contrib import admin

from .models import Resource, User

admin.site.register(User)
admin.site.register(Resource)
