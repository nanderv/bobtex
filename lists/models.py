from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.db.models import CASCADE


class List(models.Model):
    name = models.CharField(max_length=255)


class UserToList(models.Model):
    user = models.ForeignKey(User, on_delete=CASCADE)
    list = models.ForeignKey(List, on_delete=CASCADE)
    can_edit = models.BooleanField()
    is_owner = models.BooleanField()
