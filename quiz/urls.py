from django.urls import path
from quiz.views.answer_views import QuizAnswersView, QuizAnswerView, AnsewerCouseView
from quiz.views.group_views import QuizGroupsView, QuizGroupView, GroupCourseView
from quiz.views.quiz_views import QuizsView, QuizView, GroupQuestionView

urlpatterns = [
    path('quiz/course/<uuid:pk>/answer/', AnsewerCouseView.as_view()),
    path('quiz/answer/', QuizAnswersView.as_view()),
    path('quiz/answer/<uuid:pk>/', QuizAnswerView.as_view()),
    
    path('quiz/course/<uuid:pk>/group/', GroupCourseView.as_view()),
    path('quiz/group/', QuizGroupsView.as_view()),
    path('quiz/group/<uuid:pk>/', QuizGroupView.as_view()),

    path('quiz/<uuid:course_pk>/group/<uuid:pk>/question/', GroupQuestionView.as_view()),
    path('quiz/', QuizsView.as_view()),
    path('quiz/<uuid:pk>/', QuizView.as_view()),

]