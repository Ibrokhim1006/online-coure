from django.urls import path
from authen.views import (
    # UserSignUp,
    # UserSignIn,
    # UserProfile,
    # change_password,
    # RequestPasswordRestEmail,
    # SetNewPasswordView,
    # UserGroupsView,
    # StudentGroupView,
    user_login,
    register,
    user_logout, user_profile
)

urlpatterns = [
    # path('register/', UserSignUp.as_view()),
    # path('login/', UserSignIn.as_view()),
    # path('profile/', UserProfile.as_view()),
    # path('password/change/', change_password),
    # path('password/rest/', RequestPasswordRestEmail.as_view()),
    # path('password/new/', SetNewPasswordView.as_view()),
    # path('user/roll', UserGroupsView.as_view()),
    # path('user/class_name/', StudentGroupView.as_view()),

    path('', user_login, name='login'),
    path('registers/', register, name='register'),
    path('user_logout/', user_logout, name='user_logout'),
    path('user_profile/', user_profile, name='user_profile'),

]