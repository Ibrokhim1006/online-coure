from django.db import models
from authen.models import CustomUser


class Languages(models.Model):
    name = models.CharField(max_length=250)

    def __str__(self):
        return self.name


class Course(models.Model):
    name = models.CharField(max_length=250)
    content = models.TextField()
    language = models.ForeignKey(Languages, on_delete=models.CASCADE, related_name="lang")
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name


class CourseModul(models.Model):
    name = models.CharField(max_length=250)
    content = models.TextField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="cours")
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)


class Lesson(models.Model):
    name = models.CharField(max_length=250)
    files = models.FileField(upload_to='files', null=True, blank=True)
    videos = models.FileField(upload_to='video', null=True, blank=True)
    model = models.ForeignKey(CourseModul, on_delete=models.CASCADE, related_name="lessons")
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)



class Quiz(models.Model):
    name = models.CharField(max_length=250)
    module = models.ForeignKey(CourseModul, on_delete=models.CASCADE)
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name


class QuizChoice(models.Model):
    question = models.ForeignKey(Quiz, on_delete=models.CASCADE, null=True, blank=True, related_name="choice")
    text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.text
    

class CourseStudent(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True, blank=True)
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)


class UserTest(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    selected_options = models.ManyToManyField(QuizChoice)
    