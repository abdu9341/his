from django.contrib import admin
from operation.models import *


class OperationAdmin(admin.ModelAdmin):

    list_display = ['id', 'patient', 'name', 'begin']


class OperationDictionaryAdmin(admin.ModelAdmin):

    list_display = ['id', 'name']


class TimeTableAdmin(admin.ModelAdmin):

    list_display = ['id', 'doctor', 'date']


class BookingOperationAdmin(admin.ModelAdmin):

    list_display = ['id', 'name', 'patient', 'order']


admin.site.register(Operation, OperationAdmin)
admin.site.register(OperationDictionary, OperationDictionaryAdmin)
admin.site.register(TimeTable, TimeTableAdmin)
admin.site.register(BookingOperation, BookingOperationAdmin)
