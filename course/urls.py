from django.urls import path
from course.views.course_views import LanguageView, CoursesView, CourseView
from course.views.module_views import CoursModulesView, CoursModuleView

from course.view import *


urlpatterns = [
    path('language/', LanguageView.as_view()),
    path('course/', CoursesView.as_view()),
    path('course/<int:pk>/', CourseView.as_view()),

    path('course/modul/', CoursModulesView.as_view()),
    path('course/modul/<int:pk>/', CoursModuleView.as_view()),

    path('home/', home, name='home'),
    path('teacher_course/', teacher_course, name='teacher_course'),
    path('add_course/', add_course, name='add_course'),
    path('module_teacher/', modul_teacher, name='module_teacher'),
    path('add_module/', add_module, name='add_module'),
    path('lesson_teacher/', lesson_teacher, name='lesson_teacher'),
    path('add_lesson/', add_lesson, name='add_lesson')

]