from django.db.models import Sum
from django.shortcuts import render, redirect, HttpResponse
from django.urls import reverse
from patient.models import PatientInfo
from user.models import User
from user.views import login_required
from department.models import Department, Ward
from laboratory.models import *
from discharge.models import Discharge
from datetime import datetime
from gtts import gTTS


@login_required
def dischargeForm(request, patient_id, patient_num):
    """执行出院"""

    # 用户信息
    user = User.objects.all().get(name=request.session['name'])

    # 病人基本信息
    patient = PatientInfo.objects.all().get(id=patient_id)

    # 统计病房病人
    wards = user.authorityWard.filter(status=True)
    countOfTotal = wards.aggregate(Sum('count'))['count__sum']

    # 该用户能访问的病人
    patientsDoctor = PatientInfo.objects.filter(condition=1, department=user.authorityDepartment)
    patientsNurse = PatientInfo.objects.filter(condition=1, sickroom__in=user.authorityWard.all())

    # 获取前端数据
    if request.method == 'POST':
        leaveDate = datetime.now()
        dischargeStatus = request.POST.get('discharge')

        Discharge.objects.create(dischargeStatus=dischargeStatus, leaveDate=leaveDate,
                                 patient_id=patient_id, operator=user.name,
                                 leavingDepartment=user.authorityDepartment.arabic_name)
        #  更新在院状态
        patient.condition = 0
        patient.save()

        # 减少病房病人数量
        ward = patient.sickroom
        ward.count -= 1
        ward.save()

        return redirect('/index/')

    if patient.condition:

        return render(request, 'discharge/dischargeForm.html', locals())

    else:
        return HttpResponse('This patient already discharged !')


@login_required
def reenterPatient(request, patient_id, patient_num):
    """返回病人"""

    user = User.objects.all().get(name=request.session['name'])
    patient = PatientInfo.objects.get(id=patient_id)
    message = ''
    patientInfos = PatientInfo.objects.filter(basicInfo=patient.basicInfo)

    for patientInfo in patientInfos:
        if patientInfo.condition == 0 or patientInfo.condition == 8:
            pass

        else:
            message = 'The patient already in the hospital !'

            return HttpResponse(message)

    # 统计病房病人
    wards = user.authorityWard.filter(status=True)
    countOfTotal = wards.aggregate(Sum('count'))['count__sum']

    departments = Department.objects.filter(status=True).order_by('name')

    if request.method == 'POST':

        # 要住院的病人更新的信息
        sickroom_id = request.POST.get('sickroom')
        department_ids = request.POST.getlist('department')

        newPatientInfo = PatientInfo.objects.create(basicInfo=patient.basicInfo,
                                                    sickroom_id=sickroom_id, condition=1,
                                                    patientID=patient.patientID, operator=user.arabic_name)
        # 增加病房病人数量
        ward = Ward.objects.get(id=sickroom_id)
        ward.count += 1
        ward.save()

        # 记录这次的住院科室
        department_list = []
        for department_id in department_ids:
            department_list.append(Department.objects.get(id=department_id))
        newPatientInfo.department.add(*department_list)

        url = reverse('viewBasicInfo', args=(newPatientInfo.id, patient.patientID))
        return redirect(url)

    return render(request, 'discharge/reenterPatient.html', locals())
