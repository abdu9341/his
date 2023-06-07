from django.conf.urls import url
from operation import views


urlpatterns = [

    # 手术记录
    url(r'^indexOperation/$', views.indexOperation, name='indexOperation'),

    url(r'^addOperationRecord/(\d+)$', views.addOperationRecord, name='addOperationRecord'),
    url(r'^editOperationRecord/(\d+)/(\d+)$', views.editOperationRecord, name='editOperationRecord'),
    url(r'^deleteOperationRecord/(\d+)/(\d+)$', views.deleteOperationRecord, name='deleteOperationRecord'),

    url(r'^operationDetail/(\d+)$', views.operationDetail, name='operationDetail'),

    url(r'^searchOperationPatient/$', views.searchOperationPatient, name='searchOperationPatient'),
    url(r'^dateSearchOperation/$', views.dateSearchOperation, name='dateSearchOperation'),

    url(r'^allOperationPatient/$', views.allOperationPatient, name='allOperationPatient'),

    # 手术预约
    url(r'^indexBooking/$', views.indexBooking, name='indexBooking'),

    url(r'^newPatientBooking/$', views.newPatientBooking, name='newPatientBooking'),
    url(r'^bookingOperation/(\d+)$', views.bookingOperation, name='bookingOperation'),
    url(r'^editBooking/(\d+)$', views.editBooking, name='editBooking'),
    url(r'^deleteBooking/(\d+)$', views.deleteBooking, name='deleteBooking'),

    url(r'^allBookingPatients/$', views.allBookingPatients, name='allBookingPatients'),

    url(r'^bookingDetail/(\d+)$', views.bookingDetail, name='bookingDetail'),

    url(r'^searchBookingPatient/$', views.searchBookingPatient, name='searchBookingPatient'),
    url(r'^dateSearchBooking/$', views.dateSearchBooking, name='dateSearchBooking'),

    url(r'^bookingList/$', views.bookingList, name='bookingList'),

    url(r'^dateSearchBookingList/$', views.dateSearchBookingList, name='dateSearchBookingList'),

]