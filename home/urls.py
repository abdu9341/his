from django.conf.urls import url
from home import views


urlpatterns = [

    # 住院首页
    url(r'^index/$', views.index, name='index'),

    # 统计
    url(r'^statistics/$', views.statistics, name='statistics'),

    # 病人信息导出Excel
    url(r'^excelPatientInfo/$', views.excelPatientInfo, name='excelPatientInfo'),
]
