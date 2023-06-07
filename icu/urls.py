from django.conf.urls import url
from icu import views

urlpatterns = [

    url(r'^addVitalSigns/(\d+)/ID=(\d+)$', views.addVitalSigns, name='addVitalSigns'),  # 添加生命体征
    url(r'^viewVitalSigns(?P<pindex>\d*)/(?P<patient_id>\d+)$', views.viewVitalSigns, name='viewVitalSigns'),  # 生命体征列表
    url(r'^editVitalSigns/(\d+)/(\d+)/ID=(\d+)$', views.editVitalSigns, name='editVitalSigns'),  # 编辑
    url(r'^deleteVitalSigns/(\d+)/(\d+)$', views.deleteVitalSigns, name='deleteVitalSigns'),  # 删除
    url(r'^graphics/(\d+)/ID=(\d+)$', views.graphics, name='graphics'),  # 图形表

]
