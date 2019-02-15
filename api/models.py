from django.contrib.auth.models import User
from django.db import models


class Resource(models.Model):
    uuid = models.CharField(max_length=255, null=False)
    user = models.ForeignKey(User, related_name='resources', on_delete=models.CASCADE)

    def __str__(self):
        return "Resource id is {}".format(self.uuid)
