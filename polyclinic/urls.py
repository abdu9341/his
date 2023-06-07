from django.conf.urls import url
from polyclinic import views

from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [

    # record new patient  editBasicInfoPolyclinic
    url(r'^newPatientPolyclinic/$', views.newPatientPolyclinic, name='newPatientPolyclinic'),
    url(r'^basicInfoPolyclinic/(\d+)$', views.basicInfoPolyclinic, name='basicInfoPolyclinic'),
    url(r'^editBasicInfoPolyclinic/(\d+)$', views.editBasicInfoPolyclinic, name='editBasicInfoPolyclinic'),
    url(r'^deletePolyclinicPatient/(\w+)/(\d+)$', views.deletePolyclinicPatient, name='deletePolyclinicPatient'),
    url(r'^reenterPolyclinicPatient/(\d+)$', views.reenterPolyclinicPatient, name='reenterPolyclinicPatient'),

    # 门诊首页
    url(r'^indexPolyclinic/$', views.indexPolyclinic, name='indexPolyclinic'),
    url(r'^diagnosis/(\d+)$', views.diagnosis, name='diagnosis'),
    url(r'^finishTest/(\d+)$', views.finishTest, name='finishTest'),
    url(r'^absence/(\d+)$', views.absence, name='absence'),


    # 病人签到
    url(r'^arrived/(\d+)/(\w+)/(\d+)$', views.arrived, name='arrived'),
    url(r'^notArrived/(\d+)/(\w+)/(\d+)$', views.notArrived, name='notArrived'),

    # 更换顺序
    url(r'^changeNumber/(\w+)/(\d+)$', views.changeNumber, name='changeNumber'),

    # 在基本信息页面病人签到
    url(r'^arrived/(\d+)/$', views.arrivedBasicInfo, name='arrivedBasicInfo'),
    url(r'^notArrived/(\d+)/$', views.notArrivedBasicInfo, name='notArrivedBasicInfo'),

    # 呼叫病人
    url(r'^calling/$', views.calling),

    url(r'^speak/$', views.speak),
    url(r'^speakOrthopedic/$', views.speakOrthopedic),

    url(r'^getSpeak/$', views.getSpeak),
    url(r'^getSpeakOrthopedic/$', views.getSpeakOrthopedic),

    url(r'^stopSpeaking/$', views.stopSpeaking),

    # 门诊患者
    url(r'^polyclinicPatientList(?P<pindex>\d*)/$', views.polyclinicPatientList),

    # 按信息搜索门诊病人
    url(r'^searchPolyclinicPatient/$', views.searchPolyclinicPatient, name='searchPolyclinicPatient'),
    # 按日期搜索门诊病人
    url(r'^searchDatePolyclinicPatient/$', views.searchDatePolyclinicPatient, name='searchDatePolyclinicPatient'),

    # 门诊病人导出Excel
    url(r'^excelPolyclinicPatient/$', views.excelPolyclinicPatient, name='excelPolyclinicPatient'),

    # 上传预约病人信息
    url(r'^uploadPolyclinicPatient/$', views.uploadPolyclinicPatient, name='uploadPolyclinicPatient'),  # 上传门诊病人


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

