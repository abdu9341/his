from django.contrib import admin
from department.models import *


class DepartmentAdmin(admin.ModelAdmin):

    list_display = ['id', 'name', 'arabic_name', 'count', 'status']


class WardAdmin(admin.ModelAdmin):

    list_display = ['id', 'name',  'arabic_name', 'count', 'status']


class TemplateAdmin(admin.ModelAdmin):

    list_display = ['id', 'name', 'arabic_name', 'url_name']


admin.site.register(Department, DepartmentAdmin)
admin.site.register(Ward, WardAdmin)
admin.site.register(Template, TemplateAdmin)


