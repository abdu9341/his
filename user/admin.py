from django.contrib import admin
from user.models import *


class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'account', 'password', 'authorityDepartment', 'position', 'status']


class AccountAdmin(admin.ModelAdmin):
    list_display = ['id', 'account']


class PositionAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']


admin.site.register(User, UserAdmin)
admin.site.register(Account, AccountAdmin)
admin.site.register(Position, PositionAdmin)
