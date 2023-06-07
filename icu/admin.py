from django.contrib import admin
from icu.models import VitalSigns, DatesInICU


class VitalSignsAdmin(admin.ModelAdmin):

    list_display = ['id', 'pulse', 'bloodPressureMax', 'spo2', 'temperature', 'breathingRate',
                    'urineOutput', 'oxygen', 'glucose', 'recorder', 'date', 'patient']


class DatesAdmin(admin.ModelAdmin):

    list_display = ['id', 'date', 'icuPatient']


admin.site.register(VitalSigns, VitalSignsAdmin)
admin.site.register(DatesInICU, DatesAdmin)
