from django.contrib import admin
from course.models import Languages, Course, CourseModul, Lesson, Quiz, QuizChoice, CourseStudent, UserTest


admin.site.register(Languages)
admin.site.register(Course)
admin.site.register(CourseModul)
admin.site.register(Lesson)
admin.site.register(Quiz)
admin.site.register(QuizChoice)
admin.site.register(CourseStudent)
admin.site.register(UserTest)