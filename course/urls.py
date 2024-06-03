from django.urls import path
from course.views.course_views import LanguageView, CoursesView, CourseView
from course.views.module_views import CoursModulesView, CoursModuleView


urlpatterns = [
    path('language/', LanguageView.as_view()),
    path('course/', CoursesView.as_view()),
    path('course/<int:pk>/', CourseView.as_view()),

    path('course/modul/', CoursModulesView.as_view()),
    path('course/modul/<int:pk>/', CoursModuleView.as_view()),

]