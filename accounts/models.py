from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    pass

    phone_number = models.CharField(max_length=13, blank=True, null=True, unique=True)

    def __str__(self):
        return self.email