from django.contrib import admin
from authen.models import CustomUser, GroupUser

admin.site.register(CustomUser)
admin.site.register(GroupUser)