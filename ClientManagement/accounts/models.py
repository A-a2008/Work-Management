from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    telegram_name = models.CharField(max_length=1000, default="")
    telegram_user_id = models.CharField(max_length=50, null=True)

