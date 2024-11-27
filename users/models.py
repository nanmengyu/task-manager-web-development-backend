from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class CustomUser(AbstractUser):
    registration_date = models.DateTimeField(auto_now_add=True,verbose_name="注册时间")
