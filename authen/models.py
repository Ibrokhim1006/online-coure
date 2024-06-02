from django.db import models
from django.contrib.auth.models import AbstractUser


class GroupUser(models.Model):
    name = models.CharField(max_length=250)

    def __str__(self):
        return self.name


class CustomUser(AbstractUser):
    id_group = models.ForeignKey(GroupUser, on_delete=models.CASCADE, null=True, blank=True)