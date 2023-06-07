from django.conf.urls import url
from discharge import views

urlpatterns = [

    # 按日期搜索出院病人

    url(r'^dischargeForm/(\d+)/ID=(\d+)$', views.dischargeForm, name='dischargeForm'),  # 执行出院

    # 重新入院
    url(r'^reenterPatient/(?P<patient_id>\d+)/ID=(?P<patient_num>\d+)$', views.reenterPatient, name='reenterPatient'),

]
