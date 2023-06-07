from django.conf.urls import url
from department import views


urlpatterns = [

    url(r'^ward/(\d+)$', views.ward, name='ward'),  # 病房

    url(r'^wardLaboratory/(\d+)$', views.wardLaboratory, name='wardLaboratory'),  # Laboratory查看病房

    url(r'^wardOperation/(\d+)$', views.wardOperation, name='wardOperation'),  # Operation查看病房

    url(r'^departmentPolyclinic/(\d+)$', views.departmentPolyclinic, name='departmentPolyclinic'),  # 科室

    # 手术预约
    url(r'^departmentBookingOperation/(\d+)$', views.departmentBookingOperation, name='departmentBookingOperation'),


    # 为管理员
    url(r'^allDepartments/$', views.allDepartments, name='allDepartments'),  # 所有的科室
    url(r'^activeDepartment/(\d+)$', views.activeDepartment, name='activeDepartment'),  # 激活科室
    url(r'^inactiveDepartment/(\d+)$', views.inactiveDepartment, name='inactiveDepartment'),  # 未激活科室
    url(r'^addDepartment/$', views.addDepartment, name='addDepartment'),  # 添加新科室
    url(r'^editDepartment/(\d+)$', views.editDepartment, name='editDepartment'),  # 编辑科室


    # 为管理员
    url(r'^allWards/$', views.allWards, name='allWards'),  # 所有的病房
    url(r'^activeWard/(\d+)$', views.activeWard, name='activeWard'),  # 激活病房
    url(r'^inactiveWard/(\d+)$', views.inactiveWard, name='inactiveWard'),  # 未激活病房
    url(r'^addWard/$', views.addWard, name='addWard'),  # 添加新病房
    url(r'^editWard/(\d+)$', views.editWard, name='editWard'),  # 编辑病房

]
