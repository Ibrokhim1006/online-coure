from django.db import models
from authen.models import CustomUser


class Languages(models.Model):
    name = models.CharField(max_length=250)

    def __str__(self):
        return self.name


class Course(models.Model):
    name = models.CharField(max_length=250)
    content = models.TextField()
    language = models.ForeignKey(Languages, on_delete=models.CASCADE)
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name


class CourseModul(models.Model):
    name = models.CharField(max_length=250)
    content = models.TextField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)