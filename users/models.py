from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    verified_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.username
