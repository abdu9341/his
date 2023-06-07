from django.conf.urls import url
from laboratory import views

urlpatterns = [

    # laboratory首页
    url(r'^indexLaboratory/$', views.indexLaboratory, name='indexLaboratory'),

    # 录入页面
    url(r'^laboratory/(\d+)/ID=(\d+)$', views.laboratory, name='laboratory'),

    # 录入数据
    url(r'^write_cbc/(\d+)/ID=(\d+)$', views.write_cbc, name='write_cbc'),
    url(r'^write_coagulation/(\d+)/ID=(\d+)$', views.write_coagulation, name='write_coagulation'),
    url(r'^write_biochemistry/(\d+)/ID=(\d+)$', views.write_biochemistry, name='write_biochemistry'),
    url(r'^write_electrolytes/(\d+)/ID=(\d+)$', views.write_electrolytes, name='write_electrolytes'),
    url(r'^write_abg/(\d+)/ID=(\d+)$', views.write_abg, name='write_abg'),
    url(r'^write_serology/(\d+)/ID=(\d+)$', views.write_serology, name='write_serology'),
    url(r'^write_urineAnalysis/(\d+)/ID=(\d+)$', views.write_urineAnalysis, name='write_urineAnalysis'),
    url(r'^write_csf/(\d+)/ID=(\d+)$', views.write_csf, name='write_csf'),
    url(r'^write_antibiotics/(\d+)/ID=(\d+)$', views.write_antibiotics, name='write_antibiotics'),
    url(r'^write_hormones/(\d+)/ID=(\d+)$', views.write_hormones, name='write_hormones'),

    # 编辑数据
    url(r'^edit_cbc/(\d+)/(\d+)/ID=(\d+)$', views.edit_cbc, name='edit_cbc'),
    url(r'^edit_coagulation/(\d+)/(\d+)/ID=(\d+)$', views.edit_coagulation, name='edit_coagulation'),
    url(r'^edit_biochemistry/(\d+)/(\d+)/ID=(\d+)$', views.edit_biochemistry, name='edit_biochemistry'),
    url(r'^edit_electrolytes/(\d+)/(\d+)/ID=(\d+)$', views.edit_electrolytes, name='edit_electrolytes'),
    url(r'^edit_abg/(\d+)/(\d+)/ID=(\d+)$', views.edit_abg, name='edit_abg'),
    url(r'^edit_serology/(\d+)/(\d+)/ID=(\d+)$', views.edit_serology, name='edit_serology'),
    url(r'^edit_urineAnalysis/(\d+)/(\d+)/ID=(\d+)$', views.edit_urineAnalysis, name='edit_urineAnalysis'),
    url(r'^edit_csf/(\d+)/(\d+)/ID=(\d+)$', views.edit_csf, name='edit_csf'),
    url(r'^edit_antibiotics/(\d+)/(\d+)/ID=(\d+)$', views.edit_antibiotics, name='edit_antibiotics'),
    url(r'^edit_hormones/(\d+)/(\d+)/ID=(\d+)$', views.edit_hormones, name='edit_hormones'),

    url(r'^results/(\d+)/ID=(\d+)$', views.results, name='results'),


    url(r'^cancelLaboratory/(\d+)/(\d+)/types=(\w+)$', views.cancelLaboratory, name='cancelLaboratory'),

    url(r'^confirmLaboratory/(\d+)/(\d+)/types=(\w+)$', views.confirmLaboratory, name='confirmLaboratory'),

    url(r'^allLaboratoryResults/(\d+)/ID=(\d+)$', views.allLaboratoryResults, name='allLaboratoryResults'),  # 查看laboratory报告


    url(r'^todayPatients/$', views.todayPatients, name='todayPatients'),  # 今天入院的病人


    # 图形表
    url(r'^graphicLaboratory/(\d+)/(\w+)/(\w+)$', views.graphicLaboratory, name='graphicLaboratory'),

    # 搜索
    url(r'^searchLaboratoryPatient/$', views.searchLaboratoryPatient, name='searchLaboratoryPatient'),


    # 付费检验
    url(r'^moneyLaboratory/$', views.moneyLaboratory, name='moneyLaboratory'),
    url(r'^addMoneyLaboratoryPatient/$', views.addMoneyLaboratoryPatient, name='addMoneyLaboratoryPatient'),
    url(r'^dateSearchMoneyLaboratory/$', views.dateSearchMoneyLaboratory, name='dateSearchMoneyLaboratory'),
    url(r'^displayMoneyLaboratoryPrint/(\d+)/ID=(\d+)$', views.displayMoneyLaboratoryPrint, name='displayMoneyLaboratoryPrint'),

]
