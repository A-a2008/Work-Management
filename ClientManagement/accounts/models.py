from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    phone_number = models.CharField(max_length=12)
    # add telegram_user_id is possible, then go admin page and also add that

