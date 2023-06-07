from django.contrib import admin
from patient.models import BasicInfo, PatientInfo, Counter


class BasicInfoAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'phone', 'ses', 'age', 'date', 'operator']

    search_fields = ['name']


class PatientInfoAdmin(admin.ModelAdmin):
    list_display = ['id', 'basicInfo', 'patientID', 'arriveDate',
                    'condition', 'haveLaboratoryTest', 'operator']
    # search_fields = ['condition']
    search_fields = ['patientID']


class CounterAdmin(admin.ModelAdmin):
    list_display = ['id', 'day', 'count']


admin.site.register(BasicInfo, BasicInfoAdmin)
admin.site.register(PatientInfo, PatientInfoAdmin)
admin.site.register(Counter, CounterAdmin)
