from django.db.models import Q
from django.shortcuts import render, redirect
from user.views import login_required
from user.models import User
from patient.models import PatientInfo, BasicInfo
from department.models import Department
from operation.models import *
from datetime import datetime, date, timedelta
from patient.function import IDCreator


@login_required
def indexOperation(request):

    user = User.objects.all().get(name=request.session['name'])

    # 更新当前模板内容
    user.currentTemplateUrl = 'indexOperation'
    user.save()

    # 病房
    wards = user.authorityWard.filter(status=True)

    return render(request, 'operation/indexOperation.html', locals())


@login_required
def indexBooking(request):

    user = User.objects.all().get(name=request.session['name'])

    # 更新当前模板内容
    user.currentTemplateUrl = 'indexBooking'
    user.save()

    # 科室
    departments = Department.objects.filter(Q(status=True, types=2) | Q(status=True, types=3))

    return render(request, 'operation/indexBooking.html', locals())


@login_required
def addOperationRecord(request, patient_id):
    """添加手术记录"""

    username = request.session['name']

    if request.method == 'POST':
        name = request.POST.get('name')
        doctor = request.POST.get('doctor')
        assistant = request.POST.get('assistant')
        surgicalNurse = request.POST.get('surgicalNurse')
        anesthetist = request.POST.get('anesthetist')
        typesNarcosis = request.POST.get('typesNarcosis')
        typesOperation = request.POST.get('typesOperation')
        roomNo = request.POST.get('roomNo')
        begin = request.POST.get('begin')
        timeOfOperation = request.POST.get('timeOfOperation')

        Operation.objects.create(patient_id=patient_id, name=name, doctor=doctor, assistant=assistant,
                                 surgicalNurse=surgicalNurse, anesthetist=anesthetist,
                                 typesNarcosis=typesNarcosis, roomNo=roomNo, typesOperation=typesOperation,
                                 begin=begin, timeOfOperation=timeOfOperation, operator=username)

        # 更新手术名称表
        if OperationDictionary.objects.filter(name=name):
            pass
        else:
            OperationDictionary.objects.create(name=name)

        return redirect('/operationDetail/' + patient_id)


@login_required
def editOperationRecord(request, patient_id, operation_id):
    """编辑手术记录"""

    username = request.session['name']

    if request.method == 'POST':
        name = request.POST.get('name')
        doctor = request.POST.get('doctor')
        assistant = request.POST.get('assistant')
        surgicalNurse = request.POST.get('surgicalNurse')
        anesthetist = request.POST.get('anesthetist')
        typesNarcosis = request.POST.get('typesNarcosis')
        typesOperation = request.POST.get('typesOperation')
        roomNo = request.POST.get('roomNo')
        begin = request.POST.get('begin')
        timeOfOperation = request.POST.get('timeOfOperation')

        operation = Operation.objects.get(id=operation_id)

        operation.name = name
        operation.doctor = doctor
        operation.assistant = assistant
        operation.surgicalNurse = surgicalNurse
        operation.anesthetist = anesthetist
        operation.typesNarcosis = typesNarcosis
        operation.typesOperation = typesOperation
        operation.roomNo = roomNo
        operation.begin = begin
        operation.timeOfOperation = timeOfOperation
        operation.operator = username
        operation.save()

        return redirect('/operationDetail/' + patient_id)


@login_required
def deleteOperationRecord(request, patient_id, operation_id):
    """删除手术记录"""

    operation = Operation.objects.get(id=operation_id)
    operation.delete()

    return redirect('/operationDetail/' + patient_id)


@login_required
def operationDetail(request, patient_id):
    """手术详情"""

    user = User.objects.get(name=request.session['name'])

    # 病房
    wards = user.authorityWard.filter(status=True)

    patient = PatientInfo.objects.get(id=patient_id)

    operations = Operation.objects.filter(patient_id=patient_id)

    doctors = User.objects.filter(position__name='Doctor')
    nurses = User.objects.filter(position__name='Nurse')

    operationNames = OperationDictionary.objects.all()

    return render(request, 'operation/operationDetail.html', locals())


@login_required
def searchOperationPatient(request):
    """搜索手术病人"""

    user = User.objects.get(name=request.session['name'])

    # 病房
    wards = user.authorityWard.filter(status=True)

    doctors = User.objects.filter(position__name='Doctor')
    nurses = User.objects.filter(position__name='Nurse')

    operationNames = OperationDictionary.objects.all()

    if request.method == 'POST':
        search = request.POST.get('search')

        patients = PatientInfo.objects.filter(Q(basicInfo__name__contains=search) | Q(patientID=search))

        if patients:

            return render(request, 'operation/searchOperationPatient.html', locals())

        else:

            message = 'Not Fond !'

            return render(request, 'operation/searchOperationPatient.html', locals())


@login_required
def operationRecode(request, patient_id, patientID):
    """手术记录"""

    user = User.objects.get(name=request.session['name'])

    # 病房
    wards = user.authorityWard.filter(status=True)

    patient = PatientInfo.objects.get(id=patient_id)

    operations = Operation.objects.filter(patient_id=patient_id)

    return render(request, 'operation/operationRecord.html', locals())


@login_required
def allOperationPatient(request):
    """所有手术病人"""

    user = User.objects.get(name=request.session['name'])

    today = date.today()
    tomorrow = date.today() + timedelta(days=1)
    dates = (today, tomorrow)

    # 病房
    wards = user.authorityWard.filter(status=True)

    doctors = User.objects.filter(position__name='Doctor')
    nurses = User.objects.filter(position__name='Nurse')

    operations = Operation.objects.filter(begin__range=dates)

    operationNames = OperationDictionary.objects.all()

    return render(request, 'operation/allOperationPatient.html', locals())


@login_required
def dateSearchOperation(request):
    """通过日期搜索手术记录"""

    user = User.objects.get(name=request.session['name'])

    # 病房
    wards = user.authorityWard.filter(status=True)

    doctors = User.objects.filter(position__name='Doctor')
    nurses = User.objects.filter(position__name='Nurse')

    operationNames = OperationDictionary.objects.all()

    if request.method == 'POST':
        start = request.POST.get('start')
        end = request.POST.get('end')

        operations = Operation.objects.filter(begin__range=(start, end))

    return render(request, 'operation/allOperationPatient.html', locals())


@login_required
def newPatientBooking(request):
    """添加病人基本信息"""

    # 获取当前需要的数据
    genders = ['', 'ذكر', 'انثى', 'طفل', 'طفلة']
    marriages = ['', 'متزوج', 'اعزب']

    user = User.objects.get(name=request.session['name'])

    # 统计科室的病人
    departments = Department.objects.filter(Q(status=True, types=2) | Q(status=True, types=3))

    message = ''

    if request.method == 'POST':
        name = request.POST.get('name').title()
        age = request.POST.get('age')
        sex = request.POST.get('sex')
        marriage = request.POST.get('marriage')
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        department_id = request.POST.get('department')

        departmentObj = Department.objects.get(id=department_id)

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
        patient_exist = PatientInfo.objects.filter(basicInfo__name=name, basicInfo__age=age).last()

        if patient_exist:

            message = 'The patient already exists '

            return render(request, 'polyclinic/newPatientPolyclinic.html', locals())

        else:
            numberID = IDCreator()

            basicInfo = BasicInfo.objects.create(name=name, birthday=birthday, sex=sex, age=tempAge,
                                                 marriage=marriage, address=address, phone=phone,
                                                 operator=user.arabic_name)

            patient = PatientInfo.objects.create(basicInfo=basicInfo, patientID=numberID,
                                                 condition=7, operator=user.name)

            # 病人所在的科室
            department_list = [Department.objects.get(id=department_id)]
            patient.department.add(*department_list)

            # 更新该科室的病人数量
            departmentObj.count += 1
            departmentObj.save()

    return render(request, 'operation/newPatientBooking.html', locals())


@login_required
def bookingOperation(request, patient_id):
    """添加手术预定"""

    username = request.session['name']

    if request.method == 'POST':
        name = request.POST.get('name')
        doctor = request.POST.get('doctor')
        begin = request.POST.get('begin')
        # timeOfOperation = request.POST.get('timeOfOperation')
        order = request.POST.get('timeOfOperation')

        # 先检查该日期没有相应的时间表
        if TimeTable.objects.filter(doctor=doctor, date=begin):

            timeTable = TimeTable.objects.filter(doctor=doctor, date=begin).last()

            BookingOperation.objects.create(patient_id=patient_id, name=name, date=begin,
                                            order=order, timeTable=timeTable, operator=username)
        else:

            timeTable = TimeTable.objects.create(doctor=doctor, date=begin)

            BookingOperation.objects.create(patient_id=patient_id, name=name, date=begin,
                                            order=order, timeTable=timeTable, operator=username)

        return redirect('/allBookingPatients/')


@login_required
def allBookingPatients(request):
    """所有手术预定"""

    user = User.objects.get(name=request.session['name'])

    departments = Department.objects.filter(Q(status=True, types=2) | Q(status=True, types=3))

    doctors = User.objects.filter(position__name='Doctor')

    operationNames = OperationDictionary.objects.all()

    today = date.today()

    bookingPatients = BookingOperation.objects.filter(date__gte=today).order_by('date')

    return render(request, 'operation/allBookingPatient.html', locals())


@login_required
def bookingDetail(request, patient_id):
    """预约详情"""

    user = User.objects.get(name=request.session['name'])

    # 科室
    departments = Department.objects.filter(Q(status=True, types=2) | Q(status=True, types=3))

    patient = PatientInfo.objects.get(id=patient_id)

    bookings = BookingOperation.objects.filter(patient_id=patient_id)

    doctors = User.objects.filter(position__name='Doctor')

    operationNames = OperationDictionary.objects.all()

    return render(request, 'operation/bookingDetail.html', locals())


@login_required
def editBooking(request, booking_id):
    """编辑预约记录"""

    username = request.session['name']

    if request.method == 'POST':
        name = request.POST.get('name')
        doctor = request.POST.get('doctor')
        begin = request.POST.get('begin')
        timeOfOperation = request.POST.get('timeOfOperation')

        booking = BookingOperation.objects.get(id=booking_id)

        # 老的时间表
        old_timeTable = booking.timeTable

        # 先检查该日期没有相应的时间表
        if TimeTable.objects.filter(doctor=doctor, date=begin):

            timeTable = TimeTable.objects.filter(doctor=doctor, date=begin).last()

            # 更新预定信息
            booking.timeTable = timeTable
            booking.name = name
            booking.date = begin
            booking.timeOfOperation = timeOfOperation
            booking.operator = username
            booking.save()

            # 如果新的时间表和老的时间表是一致的, 什么都不做
            if old_timeTable == timeTable:
                pass

            # 如果新的时间表和老的时间表是不一致的，且老的时间表没有预定信息，删除老的时间表
            else:
                if old_timeTable.bookingoperation_set.all():
                    pass
                else:
                    old_timeTable.delete()

        else:

            timeTable = TimeTable.objects.create(doctor=doctor, date=begin)

            # 更新预定信息
            booking.timeTable = timeTable
            booking.name = name
            booking.date = begin
            booking.timeOfOperation = timeOfOperation
            booking.operator = username
            booking.save()

        return redirect('/allBookingPatients/')


@login_required
def deleteBooking(request, booking_id):
    """删除预约记录"""

    booking = BookingOperation.objects.get(id=booking_id)
    timeTable = booking.timeTable
    booking.delete()

    # 检查该世界表还有没有预约，如果有预约，pass
    if BookingOperation.objects.filter(timeTable=timeTable):

        pass

    # 如果没有预约，则删除该时间表
    else:
        timeTable.delete()

    return redirect('/allBookingPatients/')


@login_required
def searchBookingPatient(request):
    """搜索手术预约病人"""

    user = User.objects.get(name=request.session['name'])

    # 科室
    departments = Department.objects.filter(Q(status=True, types=2) | Q(status=True, types=3))

    doctors = User.objects.filter(position__name='Doctor')

    operationNames = OperationDictionary.objects.all()

    if request.method == 'POST':
        search = request.POST.get('search')

        patients = PatientInfo.objects.filter(Q(basicInfo__name__contains=search) | Q(patientID=search))

        if patients:

            return render(request, 'operation/searchBooking.html', locals())

        else:

            message = 'Not Fond !'

            return render(request, 'operation/searchBooking.html', locals())


@login_required
def dateSearchBooking(request):
    """日期搜索手术预约"""

    user = User.objects.get(name=request.session['name'])

    # 科室
    departments = Department.objects.filter(Q(status=True, types=2) | Q(status=True, types=3))

    doctors = User.objects.filter(position__name='Doctor')

    operationNames = OperationDictionary.objects.all()

    if request.method == 'POST':
        start = request.POST.get('start')

        # patients = PatientInfo.objects.filter(Q(basicInfo__name__contains=search) | Q(patientID=search))
        bookingPatients = BookingOperation.objects.filter(date=start).order_by('date')
        if bookingPatients:

            return render(request, 'operation/allBookingPatient.html', locals())

        else:

            message = 'Not Fond !'

            return render(request, 'operation/allBookingPatient.html', locals())


@login_required
def bookingList(request):
    """预约清单"""

    user = User.objects.get(name=request.session['name'])

    # 病房
    wards = user.authorityWard.filter(status=True)

    dates = date.today()

    bookings = BookingOperation.objects.filter(date=dates).order_by('order')
    timeTables = TimeTable.objects.filter(date=dates)

    return render(request, 'operation/bookingList.html', locals())


@login_required
def dateSearchBookingList(request):
    """通过日期搜索手术预定"""

    user = User.objects.get(name=request.session['name'])

    # 病房
    wards = user.authorityWard.filter(status=True)

    if request.method == 'POST':

        dates = request.POST.get('start')  # 2022-12-15

        bookings = BookingOperation.objects.filter(date=dates).order_by('order')

        timeTables = TimeTable.objects.filter(date=dates)

    return render(request, 'operation/bookingList.html', locals())
