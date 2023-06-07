from django.core.paginator import Paginator
from django.db.models import Q, Sum
from django.shortcuts import render, redirect, HttpResponse
from django.urls import reverse
from patient.models import *
from user.models import User
from department.models import Department, Ward
from user.views import login_required
from patient.function import *
from gtts import gTTS
import os


@login_required
def newPatient(request):
    """添加病人基本信息"""

    # 获取当前需要的数据
    genders = ['', 'ذكر', 'انثى', 'طفل', 'طفلة']
    marriages = ['', 'متزوج', 'اعزب']
    bloodGroups = ['Null', 'A: Neg-', 'A: Pos+', 'B: Neg-', 'B: Pos+',
                   'AB:Neg-', 'AB:Pos+', 'O: Neg-', 'O: Pos+']

    user = User.objects.get(name=request.session['name'])
    departments = Department.objects.filter(Q(status=True, types=1) | Q(status=True, types=3))

    # 统计病房病人
    wards = user.authorityWard.filter(status=True)
    countOfTotal = wards.aggregate(Sum('count'))['count__sum']

    message = ''

    if request.method == 'POST':
        name = request.POST.get('name').title()
        age = request.POST.get('age')
        sex = request.POST.get('sex')
        marriage = request.POST.get('marriage')
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        sickroom_id = request.POST.get('sickroom')
        bloodGroup = request.POST.get('bloodGroup')

        # 通过年龄计算出生年月日
        tempAge = age
        age = float(age)
        if age <= 1:
            birthday = datetime(datetime.now().year, datetime.now().month, datetime.now().day)

        else:
            age = int(age)
            birthdayYear = datetime.now().year - age
            birthdayMonth = datetime.now().month
            birthdayDay = datetime.now().day
            birthday = datetime(birthdayYear, birthdayMonth, birthdayDay)

        # 判断该病人是否已在数据库
        patient_exist = PatientInfo.objects.filter(basicInfo__name=name, basicInfo__age=age).order_by('enterDate').last()

        if patient_exist:
            message = 'المريض موجود '
            return render(request, 'patient/newPatient.html', locals())
        else:
            numberID = IDCreator()

            basicInfo = BasicInfo.objects.create(name=name, birthday=birthday, sex=sex, age=tempAge,
                                                 marriage=marriage, address=address, phone=phone,
                                                 bloodGroup=bloodGroup, operator=user.name)

            patient = PatientInfo.objects.create(basicInfo=basicInfo, patientID=numberID, condition=1,
                                                 sickroom_id=sickroom_id, operator=user.arabic_name)

            # 增加病房病人数量
            ward = Ward.objects.get(id=sickroom_id)
            ward.count += 1
            ward.save()

            # 病人所在的科室
            department_ids = request.POST.getlist('department')
            department_list = []
            for department_id in department_ids:
                department_list.append(Department.objects.get(id=department_id))
            patient.department.add(*department_list)

            url = reverse('viewBasicInfo', args=(patient.id, patient.patientID))
            return redirect(url)

    return render(request, 'patient/newPatient.html', locals())


@login_required
def patientList(request, pindex):
    """病人基本信息"""

    username = request.session['name']
    user = User.objects.all().get(name=username)

    patients = PatientInfo.objects.filter(condition__range=(1, 2)).order_by('sickroom__name')

    # 统计病房病人
    wards = user.authorityWard.filter(status=True)
    countOfTotal = wards.aggregate(Sum('count'))['count__sum']

    # 分页显示
    paginator = Paginator(patients, 20)
    if pindex == '':
        pindex = 1
    else:
        pindex = int(pindex)
    page = paginator.page(pindex)

    return render(request, 'patient/patientList.html', locals())


@login_required
def searchHospitalizedPatient(request):

    user = User.objects.all().get(name=request.session['name'])

    # 统计病房病人
    wards = user.authorityWard.filter(status=True)
    countOfTotal = wards.aggregate(Sum('count'))['count__sum']

    message = ''

    if request.method == 'POST':

        search = request.POST.get('search')

        # page = PatientInfo.objects.filter(Q(basicInfo__name__contains=search, condition__range=(0, 1))
        #                                   | Q(patientID=search, condition__range=(0, 1)))

        page = PatientInfo.objects.filter(Q(basicInfo__name__contains=search) | Q(patientID=search))

        if page:
            pass

        else:
            message = 'Not Found !'

    return render(request, 'patient/patientList.html', locals())


@login_required
def viewBasicInfo(request, patient_id, patient_num):
    """查看病人基本信息"""

    username = request.session['name']
    user = User.objects.all().get(name=username)

    rights = False
    if user.position.name == 'Receptionist' or user.position.name == 'Manager':
        rights = True

    patient = PatientInfo.objects.get(id=patient_id)

    # 该用户能访问的病人
    patientsDoctor = PatientInfo.objects.filter(condition=1, department=user.authorityDepartment)
    patientsNurse = PatientInfo.objects.filter(condition=1, sickroom__in=user.authorityWard.all())

    # 统计病房病人
    wards = user.authorityWard.filter(status=True)
    countOfTotal = wards.aggregate(Sum('count'))['count__sum']

    # 病人所属科室
    # departments = DepartmentPatient.objects.filter(patient_id=patient_id)

    # # 病人所在的科室
    # department_list = []
    # for department in departments:
    #     department_list.append(department.department)
    #
    # patient.department.add(*department_list)

    # 计算年龄
    if patient.basicInfo.age < 1 and datetime.now().year == patient.basicInfo.birthday.year:
        pass

    else:
        # 出生年月日
        birthYear = patient.basicInfo.birthday.year
        birthMonth = patient.basicInfo.birthday.month
        birthDay = patient.basicInfo.birthday.day

        # 当前年月日
        year = datetime.now().year
        month = datetime.now().month
        day = datetime.now().day

        # 计算年龄
        age = 0
        if year > birthYear:
            age = year - birthYear - 1
            if month - birthMonth:
                age = age + 1
            elif month == birthMonth and day >= birthDay:
                age = age + 1

        patient.basicInfo.age = age
        patient.basicInfo.save()

    return render(request, 'patient/viewBasicInfo.html', locals())


@login_required
def editBasicInfo(request, patient_id, patient_num):
    """编辑基本信息"""

    # 获取当前需要编辑数据
    genders = ['', 'ذكر', 'انثى', 'طفل', 'طفلة']
    marriages = ['', 'متزوج', 'اعزب']
    bloodGroups = ['Null', 'A: Neg-', 'A: Pos+', 'B: Neg-', 'B: Pos+',
                   'AB:Neg-', 'AB:Pos+', 'O: Neg-', 'O: Pos+']

    patient = PatientInfo.objects.get(id=patient_id)

    user = User.objects.get(name=request.session['name'])

    departments = Department.objects.filter(Q(status=True, types=1) | Q(status=True, types=3))

    # patientDepartments = DepartmentPatient.objects.filter(patient_id=patient_id)

    # 统计病房病人
    wards = user.authorityWard.filter(status=True)
    countOfTotal = wards.aggregate(Sum('count'))['count__sum']

    message = ''

    if request.method == 'POST':

        # 获取前台传递过来的数据
        name = request.POST.get('name').title()
        age = request.POST.get('age')
        sex = request.POST.get('sex')
        marriage = request.POST.get('marriage')
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        ward_id = request.POST.get('ward')
        bloodGroup = request.POST.get('bloodGroup')
        # department_ids = request.POST.getlist('department')

        # 增加病房病人数量
        ward_new = Ward.objects.get(id=ward_id)
        ward_old = patient.sickroom

        # 通过年龄计算出生年月日
        tempAge = age
        age = float(age)
        if age <= 1:
            birthday = datetime(datetime.now().year, datetime.now().month, datetime.now().day)

        else:
            age = int(age)
            birthdayYear = datetime.now().year - age
            birthdayMonth = datetime.now().month
            birthdayDay = datetime.now().day
            birthday = datetime(birthdayYear, birthdayMonth, birthdayDay)

        # 判断该病人是否已在数据库
        patient_exist = BasicInfo.objects.filter(name=name, birthday=birthday)
        if patient_exist and patient.basicInfo.name != name:
            message = 'The patient already exists '
            return render(request, 'patient/editBasicInfo.html', locals())

        else:
            # 对表中已存在数据进行修改
            patient.basicInfo.name = name
            patient.basicInfo.age = tempAge
            patient.basicInfo.birthday = birthday
            patient.basicInfo.sex = sex
            patient.basicInfo.marriage = marriage
            patient.basicInfo.address = address
            patient.sickroom = ward_new
            patient.basicInfo.phone = phone
            patient.basicInfo.bloodGroup = bloodGroup
            patient.condition = 1
            patient.operator = user.arabic_name
            patient.save()
            patient.basicInfo.save()

            # 病人所在的科室
            department_ids = request.POST.getlist('department')
            department_list = []
            for department_id in department_ids:
                department_list.append(Department.objects.get(id=department_id))

            if department_ids:
                patient.department.clear()
            patient.department.add(*department_list)

            # 更新病房的人数
            if ward_old is None:
                ward_new.count += 1
                ward_new.save()

            elif ward_new == ward_old:
                pass

            else:
                ward_old.count -= 1
                ward_old.save()

                ward_new.count += 1
                ward_new.save()

            # departmentPatients = DepartmentPatient.objects.filter(patient_id=patient_id, patient__condition=1)
            # department_ids = request.POST.getlist('department')
            #
            # if department_ids:
            #     for department in departmentPatients:
            #         department.delete()
            #
            #     for department_id in department_ids:
            #         DepartmentPatient.objects.create(department_id=department_id, patient_id=patient_id)

            url = reverse('viewBasicInfo', args=(patient.id, patient.patientID))
            return redirect(url)

    if patient.condition:

        return render(request, 'patient/editBasicInfo.html', locals())

    else:
        return HttpResponse('This Patient already discharged, you can\'t edit !')


@login_required
def transfer(request, patient_id, patient_num):
    """转科"""

    patient = PatientInfo.objects.get(id=patient_id)
    user = User.objects.all().get(name=request.session['name'])

    # 统计病房病人
    wards = user.authorityWard.filter(status=True)
    countOfTotal = wards.aggregate(Sum('count'))['count__sum']

    wardObjs = Ward.objects.filter(status=True)

    # 该用户能访问的病人
    patientsDoctor = PatientInfo.objects.filter(condition=1, department=user.authorityDepartment)
    patientsNurse = PatientInfo.objects.filter(condition=1, sickroom__in=user.authorityWard.all())

    message = ''

    if request.method == 'POST':
        transferSickroom_id = request.POST.get('sickroom')
        # date = request.POST.get('date')
        date = datetime.now()

        # 增加病房病人数量
        ward_new = Ward.objects.get(id=transferSickroom_id)
        ward_old = patient.sickroom

        patient.sickroom_id = transferSickroom_id
        patient.transferDate = date
        patient.save()

        # 更新病房的人数
        if ward_new == ward_old:
            pass

        else:
            ward_new.count += 1
            ward_new.save()

            ward_old.count -= 1
            ward_old.save()

        message = 'Successful transfer !'

        url = reverse('viewBasicInfo', args=(patient_id, patient_num))

        return redirect(url)

    if patient.condition:

        return render(request, 'patient/transfer.html', locals())

    else:
        return HttpResponse('This Patient already discharged, you can\'t transfer !')
