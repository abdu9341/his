from django.conf.urls import url
from user import views


urlpatterns = [
    url(r'^login/$', views.login),
    url(r'^loginCheck$', views.loginCheck, name='loginCheck'),
    url(r'^logout$', views.logout, name='logout'),
    url(r'^changePwdAction$', views.changePwdAction, name='changePwdAction'),
    url(r'^userProfile/$', views.userProfile, name='userProfile'),


    # 管理员首页
    url(r'^indexAdmin/$', views.indexAdmin, name='indexAdmin'),

    # 管理账户
    url(r'^allUsers/$', views.allUsers, name='allUsers'),
    url(r'^addUser/$', views.addUser, name='addUser'),
    url(r'^editUser/(\d+)$', views.editUser, name='editUser'),

    url(r'^activeUser/(\d+)$', views.activeUser, name='activeUser'),
    url(r'^inactiveUser/(\d+)$', views.inactiveUser, name='inactiveUser'),

    # 切换语言
    url(r'^arabic/$', views.arabic, name='arabic'),
    url(r'^english/$', views.english, name='english'),

]
