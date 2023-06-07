from django.conf.urls import url
from emergency import views


urlpatterns = [

    # 急诊首页
    url(r'^indexEmergency/$', views.indexEmergency, name='indexEmergency'),

    # 所有的急诊病人
    url(r'^emergencyPatientList(?P<pindex>\d*)$', views.emergencyPatientList, name='emergencyPatientList'),

    # 搜索急诊病人
    url(r'^searchEmergencyPatient/$', views.searchEmergencyPatient, name='searchEmergencyPatient'),

    # 新急诊病人
    url(r'^newEmergencyPatient/$', views.newEmergencyPatient, name='newEmergencyPatient'),

    url(r'^emergencyPatientInfo/(\d+)/ID=(\d+)$', views.emergencyPatientInfo, name='emergencyPatientInfo'),

    url(r'^editEmergencyPatientInfo/(\d+)/ID=(\d+)$', views.editEmergencyPatientInfo, name='editEmergencyPatientInfo'),

    # 重新入院急诊病人
    url(r'^reenterEmergencyPatient/(?P<patient_id>\d+)/ID=(?P<patient_num>\d+)$', views.reenterEmergencyPatient, name='reenterEmergencyPatient'),

    # 门诊病人Laboratory信息
    url(r'^emergencyPatientLaboratory/(\d+)/ID=(\d+)$', views.emergencyPatientLaboratory, name='emergencyPatientLaboratory'),

    url(r'^emergencyPatientTransfer/(\d+)/ID=(\d+)$', views.emergencyPatientTransfer, name='emergencyPatientTransfer'),

    # 急诊病人出院
    url(r'^emergencyPatientDischarge/(\d+)/ID=(\d+)$', views.emergencyPatientDischarge, name='emergencyPatientDischarge'),
]
