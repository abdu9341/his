from django.contrib import admin
from discharge.models import Discharge


class DischargeAdmin(admin.ModelAdmin):
    list_display = ['id', 'leaveDate', 'dischargeStatus', 'leavingDepartment', 'patient']


admin.site.register(Discharge, DischargeAdmin)


