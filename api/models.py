from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_admin', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        if extra_fields.get('is_admin') is not True:
            raise ValueError('Superuser must have is_admin=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser):
    id = models.IntegerField(primary_key=True)
    email = models.CharField(unique=True, max_length=100, null=False)
    is_admin = models.BooleanField(default=False)
    quota = models.IntegerField(default=None, null=True)

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['is_admin']

    objects = UserManager()


class Resource(models.Model):
    uuid = models.UUIDField(primary_key=True, max_length=50, null=False)
    user = models.ForeignKey(User, related_name='resources', on_delete=models.CASCADE)

    def __str__(self):
        return "Resource id {}".format(self.uuid)
