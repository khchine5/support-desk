from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import SupportUser

UserAdmin.fieldsets[1][1]['fields'] += ('role',)

admin.site.register(SupportUser, UserAdmin)
