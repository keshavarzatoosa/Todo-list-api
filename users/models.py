from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    # username = None
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['password', 'username']

    def __str__(self):
        return self.email