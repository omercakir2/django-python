from email.policy import default
from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Verificate(models.Model):
    user = models.OneToOneField(User, null = True, on_delete=models.CASCADE)
    is_verificate = models.BooleanField(default=False)