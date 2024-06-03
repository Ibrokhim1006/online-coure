from django.contrib import admin
from quiz.models import QuizAnswers, QuizGroup, Quiz, QuizChoice


@admin.register(QuizAnswers)
class QuizAnswersAdmin(admin.ModelAdmin):
    list_display = ('id', 'answer', 'course')


@admin.register(QuizGroup)
class QuizGroupAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'course')


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ('id', 'question', 'course', 'group')


@admin.register(QuizChoice)
class QuizChoiceAdmin(admin.ModelAdmin):
    list_display = ('id', 'question', 'text', 'is_correct')






