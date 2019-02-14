from django.db import models


class User(models.Model):
    user_id = models.CharField(null=False, max_length=16)
    email = models.EmailField(null=False)
    password = models.CharField(null=False, max_length=16)
    is_admin = models.BooleanField('admin status', default=False)
    resources = models.CharField(max_length=255, default=None)

    def __str__(self):
        return "User {} with email {} has {} resources left".format(self.user_id, self.email, self.resources)


class Resource(models.Model):
    uuid = models.CharField(max_length=255, null=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return "Resource id is {}".format(self.uuid)
