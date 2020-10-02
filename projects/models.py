from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
from django.db.models import CASCADE, SET_NULL




class Project(models.Model):
    name = models.CharField(max_length=255)


    def count(self):
        from library.models import Item
        return len(Item.objects.filter(project=self))


class User(AbstractUser):
    default_project = models.ForeignKey(Project, null=True, blank=True, on_delete=SET_NULL)


class UserToProject(models.Model):
    user = models.ForeignKey(User, on_delete=CASCADE)
    project = models.ForeignKey(Project, on_delete=CASCADE)
    can_edit = models.BooleanField()
    is_owner = models.BooleanField()



