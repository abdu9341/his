from django.conf.urls import url
from patient import views

urlpatterns = [

    url(r'^newPatient$', views.newPatient, name='newPatient'),  # 添加病人基本信息
    url(r'^patientList(?P<pindex>\d*)/$', views.patientList, name='patientList'),  # 病人基本信息

    # 搜索住院病人
    url(r'^searchHospitalizedPatient/$', views.searchHospitalizedPatient, name='searchHospitalizedPatient'),

    url(r'^viewBasicInfo/(\d+)/ID=(\d+)$', views.viewBasicInfo, name='viewBasicInfo'),  # 查看病人基本信息
    url(r'^editBasicInfo/(\d+)/ID=(\d+)$', views.editBasicInfo, name='editBasicInfo'),  # 编辑病人基本信息

    url(r'^transfer/(\d+)/ID=(\d+)$', views.transfer, name='transfer'),  # 转科病人


]
