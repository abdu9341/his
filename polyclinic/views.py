from django.core.paginator import Paginator
from django.http import HttpResponse, StreamingHttpResponse
from django.db.models import Q
from django.shortcuts import render, redirect
from django.http import JsonResponse
from user.views import login_required
from department.models import Department
from patient.models import *
from user.models import User
from datetime import datetime
from django.utils import timezone
from io import BytesIO
from his import settings
from gtts import gTTS
from patient.function import IDCreator
from polyclinic.text_to_speech import speech
from django.db.models import Sum
import os
import xlwt
import xlrd


@login_required
def newPatientPolyclinic(request):
    """添加病人基本信息"""

    # 获取当前需要的数据
    genders = ['', 'ذكر', 'انثى', 'طفل', 'طفلة']
    marriages = ['', 'متزوج', 'اعزب']
    bloodGroups = ['Null', 'A: Neg-', 'A: Pos+', 'B: Neg-', 'B: Pos+',
                   'AB:Neg-', 'AB:Pos+', 'O: Neg-', 'O: Pos+']

    user = User.objects.get(name=request.session['name'])

    # 统计科室的病人
    departments = Department.objects.filter(Q(status=True, types=2) | Q(status=True, types=3))
    countOfTotal = departments.aggregate(Sum('count'))['count__sum']

    message = ''

    if request.method == 'POST':
        name = request.POST.get('name').title()
        age = request.POST.get('age')
        sex = request.POST.get('sex')
        marriage = request.POST.get('marriage')
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        bloodGroup = request.POST.get('bloodGroup')
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
        patient_exist = PatientInfo.objects.filter(basicInfo__name=name, basicInfo__age=age,
                                                   department=departmentObj).last()

        if patient_exist:
            if 5 <= patient_exist.condition <= 7:
                message = 'المريض موجود '
                return render(request, 'polyclinic/newPatientPolyclinic.html', locals())

            else:
                patient_exist.basicInfo.marriage = marriage
                patient_exist.basicInfo.address = address
                patient_exist.basicInfo.phone = phone
                patient_exist.basicInfo.save()

                patient = PatientInfo.objects.create(basicInfo=patient_exist.basicInfo,
                                                     patientID=patient_exist.patientID,
                                                     condition=5, operator=user.arabic_name)

                # 病人所在的科室
                department_list = [Department.objects.get(id=department_id)]
                patient.department.add(*department_list)

                # 更新该科室的病人数量
                departmentObj.count += 1
                departmentObj.save()

                try:

                    # 生成音频文件
                    # speech(name, departmentObj.arabic_name, patient.patientID)
                    text1 = 'إلى العِيَادَة'
                    textToAudio = name + ',' + text1 + ',' + departmentObj.arabic_name

                    language = 'ar'
                    myCall = gTTS(text=textToAudio, lang=language, slow=False)

                    myCall.save("C:/his/media/calling/"f'{patient.patientID}.mp3')

                    return redirect('/basicInfoPolyclinic/' + str(patient.id))

                except:

                    return redirect('/basicInfoPolyclinic/' + str(patient.id))

        else:
            numberID = IDCreator()

            basicInfo = BasicInfo.objects.create(name=name, birthday=birthday, sex=sex, age=tempAge,
                                                 marriage=marriage, address=address, phone=phone,
                                                 operator=user.arabic_name)

            patient = PatientInfo.objects.create(basicInfo=basicInfo, patientID=numberID,
                                                 condition=5, operator=user.arabic_name)

            # 病人所在的科室
            department_list = [Department.objects.get(id=department_id)]
            patient.department.add(*department_list)

            # 更新该科室的病人数量
            departmentObj.count += 1
            departmentObj.save()

            try:

                # 生成音频文件
                # speech(name, departmentObj.arabic_name, patient.patientID)
                text1 = 'إلى العِيَادَة'
                textToAudio = name + ',' + text1 + ',' + departmentObj.arabic_name

                language = 'ar'
                myCall = gTTS(text=textToAudio, lang=language, slow=False)

                myCall.save("C:/his/media/calling/"f'{patient.patientID}.mp3')

                return redirect('/basicInfoPolyclinic/' + str(patient.id))

            except:

                return redirect('/basicInfoPolyclinic/' + str(patient.id))

    return render(request, 'polyclinic/newPatientPolyclinic.html', locals())


@login_required
def editBasicInfoPolyclinic(request, patient_id):
    """编辑基本信息"""

    # 获取当前需要编辑数据
    genders = ['', 'ذكر', 'انثى', 'طفل', 'طفلة']
    marriages = ['', 'متزوج', 'اعزب']
    bloodGroups = ['Null', 'A: Neg-', 'A: Pos+', 'B: Neg-', 'B: Pos+',
                   'AB:Neg-', 'AB:Pos+', 'O: Neg-', 'O: Pos+']

    patient = PatientInfo.objects.get(id=patient_id)
    user = User.objects.get(name=request.session['name'])

    # 统计科室的病人
    departments = Department.objects.filter(Q(status=True, types=2) | Q(status=True, types=3))
    countOfTotal = departments.aggregate(Sum('count'))['count__sum']

    message = ''

    if request.method == 'POST':

        # 获取前台传递过来的数据
        name = request.POST.get('name').title()
        age = request.POST.get('age')
        sex = request.POST.get('sex')
        marriage = request.POST.get('marriage')
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        bloodGroup = request.POST.get('bloodGroup')
        department_id = request.POST.get('department')

        # 科室对象
        department_new = Department.objects.get(id=department_id)
        # department_old = Department.objects.get(name=patient.polyclinicDepartment)

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
        patient_exist = PatientInfo.objects.filter(basicInfo__name=name, basicInfo__age=age,
                                                   department=department_new).last()

        if patient_exist and patient != patient_exist:
            if 5 <= patient_exist.condition <= 7:
                message = 'المريض موجود '
                return redirect('/basicInfoPolyclinic/' + str(patient_exist.id))

            elif patient_exist.condition != 1:

                patient.basicInfo.name = name
                patient.basicInfo.age = tempAge
                patient.basicInfo.birthday = birthday
                patient.basicInfo.sex = sex
                patient.basicInfo.marriage = marriage
                patient.basicInfo.address = address
                patient.basicInfo.phone = phone
                patient.condition = 5
                patient.enterDate = datetime.now()
                patient.operator = user.arabic_name
                patient.basicInfo.save()
                patient.save()

                # 病人所在的科室
                department_list = [Department.objects.get(id=department_id)]
                patient.department.clear()
                patient.department.add(*department_list)

                # 更新该科室的病人数量
                for department in departments:
                    patientObjs = PatientInfo.objects.filter(department=department, condition__range=(5, 7))
                    department.count = patientObjs.count()
                    department.save()

                try:
                    # 生成音频文件
                    # speech(name, department_new.arabic_name, patient.patientID)
                    text1 = 'إلى العِيَادَة'
                    textToAudio = name + ',' + text1 + ',' + department_new.arabic_name

                    language = 'ar'
                    myCall = gTTS(text=textToAudio, lang=language, slow=False)

                    myCall.save("C:/his/media/calling/"f'{patient.patientID}.mp3')

                    return redirect('/basicInfoPolyclinic/' + patient_id)

                except:

                    return redirect('/basicInfoPolyclinic/' + patient_id)

            else:
                message = 'The patient already in the hospital '
                return render(request, 'polyclinic/editBasicInfoPolyclinic.html', locals())

        else:
            # 对表中已存在数据进行修改
            patient.basicInfo.name = name
            patient.basicInfo.age = tempAge
            patient.basicInfo.birthday = birthday
            patient.basicInfo.sex = sex
            patient.basicInfo.marriage = marriage
            patient.basicInfo.address = address
            patient.basicInfo.phone = phone
            patient.condition = 5
            patient.enterDate = datetime.now()
            patient.operator = user.arabic_name
            patient.save()
            patient.basicInfo.save()

            # 病人所在的科室
            department_list = [Department.objects.get(id=department_id)]
            patient.department.clear()
            patient.department.add(*department_list)

            # 更新该科室的病人数量
            for department in departments:
                patientObjs = PatientInfo.objects.filter(department=department, condition__range=(5, 7))
                department.count = patientObjs.count()
                department.save()

            try:
                # 生成音频文件
                # speech(name, department_new.arabic_name, patient.patientID)
                text1 = 'إلى عِيَادَةِ'
                textToAudio = name + ',' + text1 + ',' + department_new.arabic_name

                language = 'ar'
                myCall = gTTS(text=textToAudio, lang=language, slow=False)

                myCall.save("C:/his/media/calling/"f'{patient.patientID}.mp3')

                return redirect('/basicInfoPolyclinic/' + patient_id)

            except:

                return redirect('/basicInfoPolyclinic/' + patient_id)

    if patient.condition:

        return render(request, 'polyclinic/editBasicInfoPolyclinic.html', locals())

    else:
        return HttpResponse('This Patient already discharged, you can\'t edit !')


@login_required
def basicInfoPolyclinic(request, patient_id):
    user = User.objects.all().get(name=request.session['name'])

    # 统计科室的病人
    departments = Department.objects.filter(Q(status=True, types=2) | Q(status=True, types=3))
    countOfTotal = departments.aggregate(Sum('count'))['count__sum']

    # 门诊病人详情
    patient = PatientInfo.objects.get(id=patient_id)

    # 待就诊病人
    waitPatients = PatientInfo.objects.filter(department=user.authorityDepartment,
                                              condition=5, arrive=True, ).order_by('arriveDate')
    # 已就诊病人
    finishPatients = PatientInfo.objects.filter(department=user.authorityDepartment,
                                                condition=6, arrive=True)
    # 缺席的病人
    absencePatients = PatientInfo.objects.filter(department=user.authorityDepartment,
                                                 condition=7, arrive=True)

    # 统计等待，结束，缺席病人
    countOfWait = waitPatients.count()
    countOfFinish = finishPatients.count()
    countOfAbsence = absencePatients.count()

    return render(request, 'polyclinic/basicInfoPolyclinic.html', locals())


@login_required
def deletePolyclinicPatient(request, url_str, url_num):

    if request.method == 'POST':

        patient_ids = request.POST.getlist('patient_id')

        for patient_id in patient_ids:

            patient = PatientInfo.objects.get(id=patient_id)

            # 更新该科室的病人数量
            departments = patient.department.all()
            for department in departments:
                department.count -= 1
                department.save()

            patient.delete()

        url = "/" + url_str + "/" + url_num

        return redirect(url)


@login_required
def reenterPolyclinicPatient(request, patient_id):

    user = User.objects.get(name=request.session['name'])

    departments = Department.objects.filter(Q(status=True, types=2) | Q(status=True, types=3))

    patient = PatientInfo.objects.get(id=patient_id)

    if request.method == 'POST':

        address = request.POST.get('address')
        phone = request.POST.get('phone')
        department_id = request.POST.get('department')

        departmentObj = Department.objects.get(id=department_id)

        # update basicInfo
        patient.basicInfo.address = address
        patient.basicInfo.phone = phone
        patient.basicInfo.save()

        newPatientInfo = PatientInfo.objects.create(basicInfo=patient.basicInfo, condition=5,
                                                    patientID=patient.patientID, operator=user.arabic_name)
        # 病人所在的科室
        department_list = [Department.objects.get(id=department_id)]
        patient.department.add(*department_list)

        # 更新该科室的病人数量
        departmentObj.count += 1
        departmentObj.save()

        try:

            # 生成音频文件
            # name = newPatientInfo.basicInfo.name
            # speech(name, departmentObj.arabic_name, patient.patientID)

            name = newPatientInfo.basicInfo.name
            text1 = 'إلى عِيَادَةِ'
            textToAudio = name + ',' + text1 + ',' + departmentObj.arabic_name

            language = 'ar'
            myCall = gTTS(text=textToAudio, lang=language, slow=False)

            myCall.save("C:/his/media/calling/"f'{newPatientInfo.patientID}.mp3')

            return redirect('/basicInfoPolyclinic/' + str(newPatientInfo.id))

        except:

            return redirect('/basicInfoPolyclinic/' + str(newPatientInfo.id))

    return render(request, 'polyclinic/reenterPolyclinicPatient.html', locals())


@login_required
def indexPolyclinic(request):

    user = User.objects.all().get(name=request.session['name'])

    # 自动更新所有科室的病人数量
    departments = Department.objects.filter(status=True, types=1)
    for department in departments:
        department.count = PatientInfo.objects.filter(condition__range=(5, 7), department=department).count()
        department.save()

    # 更新当前模板内容
    user.currentTemplateUrl = 'indexPolyclinic'
    user.save()

    if user.authorityDepartment.name == 'Polyclinic':
        # 前天的门诊病人自动出院
        allPolyclinicPatient = PatientInfo.objects.filter(condition__range=(5, 7))
        timeNow = datetime.now().day
        for patient in allPolyclinicPatient:

            if timeNow - patient.enterDate.day != 0:
                patient.condition = 8
                patient.save()

                # 更新该科室的病人数量
                departments = patient.department.all()
                for department in departments:
                    department.count = 0
                    department.save()

    # 统计科室的病人
    departments = Department.objects.filter(Q(status=True, types=2) | Q(status=True, types=3))
    countOfTotal = departments.aggregate(Sum('count'))['count__sum']

    # 待就诊病人
    waitPatients = PatientInfo.objects.filter(department=user.authorityDepartment,
                                              condition=5, arrive=True, ).order_by('arriveDate')
    # 已就诊病人
    finishPatients = PatientInfo.objects.filter(department=user.authorityDepartment,
                                                condition=6, arrive=True)
    # 缺席的病人
    absencePatients = PatientInfo.objects.filter(department=user.authorityDepartment,
                                                 condition=7, arrive=True)

    # 统计等待，结束，缺席病人
    countOfWait = waitPatients.count()
    countOfFinish = finishPatients.count()
    countOfAbsence = absencePatients.count()

    return render(request, 'polyclinic/indexPolyclinic.html', locals())


@login_required
def arrived(request, patient_id, url_str, url_num):

    patient = PatientInfo.objects.get(id=patient_id)
    patient.arrive = True
    patient.arriveDate = datetime.now()
    patient.save()

    url = "/" + url_str + "/" + url_num

    return redirect(url)


@login_required
def notArrived(request, patient_id, url_str, url_num):

    patient = PatientInfo.objects.get(id=patient_id)
    patient.arrive = False
    patient.save()

    url = "/" + url_str + "/" + url_num

    return redirect(url)


@login_required
def changeNumber(request, url_str, url_num):

    if request.method == 'POST':

        patient_ids = request.POST.getlist('patient_id')

        length = len(patient_ids)

        url = "/" + url_str + "/" + url_num

        if length == 2:
            try:
                patient1 = PatientInfo.objects.get(id=patient_ids[0])
                patient2 = PatientInfo.objects.get(id=patient_ids[1])

                temp = patient1.arriveDate
                patient1.arriveDate = patient2.arriveDate
                patient2.arriveDate = temp

                patient1.save()
                patient2.save()

                return redirect(url)

            except:

                return redirect(url)

        else:

            return redirect(url)


@login_required
def arrivedBasicInfo(request, patient_id):

    patient = PatientInfo.objects.get(id=patient_id)
    patient.arrive = True
    patient.arriveDate = datetime.now()
    patient.save()

    return redirect('/basicInfoPolyclinic/' + patient_id)


@login_required
def notArrivedBasicInfo(request, patient_id):

    patient = PatientInfo.objects.get(id=patient_id)
    patient.arrive = False
    patient.save()

    return redirect('/basicInfoPolyclinic/' + patient_id)


@login_required
def diagnosis(request, patient_id):

    user = User.objects.all().get(name=request.session['name'])

    patient = PatientInfo.objects.get(id=patient_id)

    if request.method == 'POST':
        diagnos = request.POST.get('diagnosis')
        patient.diagnosis = diagnos
        patient.save()

        return redirect('/basicInfoPolyclinic/' + patient_id, locals())


@login_required
def finishTest(request, patient_id):

    patient = PatientInfo.objects.get(id=patient_id)
    patient.condition = 6
    patient.save()

    return redirect('/basicInfoPolyclinic/' + patient_id)


@login_required
def absence(request, patient_id):

    patient = PatientInfo.objects.get(id=patient_id)
    patient.condition = 7
    patient.save()

    return redirect('/basicInfoPolyclinic/' + patient_id)


@login_required
def calling(request):

    patient_id = request.GET.get('id')

    patient = PatientInfo.objects.get(id=patient_id)

    patient.basicInfo.ses = True
    patient.basicInfo.save()

    # return redirect('/basicInfoPolyclinic/' + patient_id)
    return JsonResponse({'data': 4500})


@login_required
def speak(request):

    user = User.objects.all().get(name=request.session['name'])

    return render(request, 'polyclinic/speak.html', locals())


@login_required
def speakOrthopedic(request):

    user = User.objects.all().get(name=request.session['name'])

    return render(request, 'polyclinic/speakOrthopedic.html', locals())


@login_required
def getSpeak(request):

    # 当天所有的不为骨科的门诊病人
    patients = PatientInfo.objects.filter(condition__range=(5, 7), basicInfo__ses=True)

    departmentObj = Department.objects.get(name='Orthopedic')

    nameList = []
    for patient in patients:
        if departmentObj == patient.department.all().first():
            # if patient.polyclinicDepartment == 'Orthopedic' or patient.polyclinicDepartment == 'orthopedic':
            pass

        else:
            department = patient.department.all().first()
            arabic_name = department.arabic_name
            english_name = department.name
            nameList.append((patient.id, patient.basicInfo.name, arabic_name, english_name, patient.patientID))

    return JsonResponse({'data': nameList})


@login_required
def getSpeakOrthopedic(request):

    departmentObj = Department.objects.get(name='Orthopedic')

    # 当天所有的为骨科的门诊病人
    patients = PatientInfo.objects.filter(condition__range=(5, 7), basicInfo__ses=True)

    nameList = []

    for patient in patients:
        if departmentObj == patient.department.all().first():
            department = patient.department.all().first()
            arabic_name = department.arabic_name
            english_name = department.name
            nameList.append((patient.id, patient.basicInfo.name, arabic_name, english_name, patient.patientID))

    return JsonResponse({'data': nameList})


@login_required
def stopSpeaking(request):

    patient_id = request.GET.get('id')

    # 门诊病人
    patient = PatientInfo.objects.get(id=patient_id)

    patient.basicInfo.ses = False
    patient.basicInfo.save()

    return JsonResponse({'data': 4500})


@login_required
def polyclinicPatientList(request, pindex):
    """所有门诊病人"""

    username = request.session['name']
    user = User.objects.all().get(name=username)

    # patientObjs = PatientInfo.objects.filter(condition__range=(5, 8))
    # for patientObj in patientObjs:
    #
    #     departmentObj = Department.objects.filter(name=patientObj.polyclinicDepartment)
    #     for department in departmentObj:
    #         department_list = [department]
    #         patientObj.department.add(*department_list)

    # 当天的门诊病人
    patients = PatientInfo.objects.filter(condition__range=(5, 7))

    # 统计科室的病人
    departments = Department.objects.filter(Q(status=True, types=2) | Q(status=True, types=3))
    countOfTotal = departments.aggregate(Sum('count'))['count__sum']

    # 分页显示
    paginator = Paginator(patients, 20)
    if pindex == '':
        pindex = 1
    else:
        pindex = int(pindex)
    page = paginator.page(pindex)

    return render(request, 'polyclinic/polyclinicPatientList.html', locals())


@login_required
def searchPolyclinicPatient(request):

    user = User.objects.all().get(name=request.session['name'])

    # 统计科室的病人
    departments = Department.objects.filter(Q(status=True, types=2) | Q(status=True, types=3))
    countOfTotal = departments.aggregate(Sum('count'))['count__sum']

    # 当天的门诊病人
    allPolyclinicPatient = PatientInfo.objects.filter(condition__range=(5, 7))

    message = ''

    if request.method == 'POST':

        search = request.POST.get('search')

        page = PatientInfo.objects.filter(Q(basicInfo__name__contains=search, condition__range=(5, 8))
                                          | Q(patientID=search, condition__range=(5, 8)))

        if page:
            pass

        else:
            message = 'Not Found !'

    return render(request, 'polyclinic/polyclinicPatientList.html', locals())


@login_required
def searchDatePolyclinicPatient(request):

    user = User.objects.all().get(name=request.session['name'])

    # 统计科室的病人
    departments = Department.objects.filter(Q(status=True, types=2) | Q(status=True, types=3))
    countOfTotal = departments.aggregate(Sum('count'))['count__sum']

    # 当天的门诊病人
    allPolyclinicPatient = PatientInfo.objects.filter(condition__range=(5, 7))

    message = ''

    if request.method == 'POST':

        start = request.POST.get('start')
        end = request.POST.get('end')

        date = (start, end)

        page = PatientInfo.objects.filter(enterDate__range=date, condition__range=(5, 8))

        if page:

            pass

        else:
            message = 'Not Found !'

    return render(request, 'polyclinic/polyclinicPatientList.html', locals())


@login_required
def excelPolyclinicPatient(request):
    """导出excel文件"""

    if request.method == 'POST':
        start = request.POST.get('start')
        end = request.POST.get('end')

        date = (start, end)

        patients = PatientInfo.objects.filter(enterDate__range=date, condition__range=(5, 8))

        if patients:
            # 创建工作簿
            wb = xlwt.Workbook(encoding='utf8')

            # 添加第一页数据表
            ws = wb.add_sheet(u"Polyclinic Patients")

            # 写入表头
            ws.write(0, 0, u'اسم المريض')
            ws.write(0, 1, u'العمر')
            ws.write(0, 2, u'الجنس')
            ws.write(0, 3, u'الحالة العائلية')
            ws.write(0, 4, u'السكن')
            ws.write(0, 5, u'رقم هاتف')
            ws.write(0, 6, u'قسم القبول')
            ws.write(0, 7, u'تاريخ القبول')
            ws.write(0, 8, u'رقم المريض')
            ws.write(0, 9, u'تشخبص')
            ws.write(0, 10, u'العامل')

            # 写入每一行对应的数据
            excel_row = 1
            for patient in patients:
                ws.write(excel_row, 0, patient.basicInfo.name)
                ws.write(excel_row, 1, patient.basicInfo.age)
                ws.write(excel_row, 2, patient.basicInfo.sex)
                ws.write(excel_row, 3, patient.basicInfo.marriage)
                ws.write(excel_row, 4, patient.basicInfo.address)
                ws.write(excel_row, 5, patient.basicInfo.phone)

                # 登记科室
                ws.write(excel_row, 6, patient.department.all().first().arabic_name)

                ws.write(excel_row, 7, patient.enterDate.strftime("%Y-%m-%d, %H:%M:%S"))
                ws.write(excel_row, 8, patient.patientID)
                ws.write(excel_row, 9, patient.diagnosis)
                ws.write(excel_row, 10, patient.operator)

                excel_row += 1

            # 实现下载
            output = BytesIO()
            wb.save(output)
            # 重新定位到开始
            output.seek(0)

            response = StreamingHttpResponse(output)
            response['content_type'] = 'application/vnd.ms-excel'
            response['charset'] = 'utf-8'
            response['Content-Disposition'] = 'attachment; filename="{0}.xls"'.format(
                timezone.datetime.now().strftime('%Y%m%d%H%M'))

            return response

        else:
            return HttpResponse('There are no data !')


# 将excel数据写入mysql
def writePolyclinicPatient(filename, username):

    # 打开上传 excel 表格
    readBook = xlrd.open_workbook(settings.MEDIA_ROOT + "/excel/" + filename)
    sheet = readBook.sheet_by_index(0)

    # 获取excel的行和列
    nrows = sheet.nrows
    ncols = sheet.ncols

    for i in range(1, nrows):
        row = sheet.row_values(i)

        if row[0]:
            name = row[0]
            age = row[1]
            gender = row[2]
            marriage = row[3]
            address = row[4]
            phone = row[5]
            department_name = row[6]

            # 挂号的科室
            department = Department.objects.get(name=department_name)

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

            patient_exist = PatientInfo.objects.filter(basicInfo__name=name, basicInfo__age=age,
                                                       department=department).last()

            if patient_exist:

                if 5 <= patient_exist.condition <= 7:

                    # pass

                    try:

                        # 生成音频文件
                        # speech(name, department.arabic_name, patient_exist.patientID)

                        text1 = 'إلى العِيَادَةِ'
                        textToAudio = name + ',' + text1 + ',' + department.arabic_name

                        language = 'ar'
                        myCall = gTTS(text=textToAudio, lang=language, slow=False)

                        myCall.save("C:/his/media/calling/"f'{patient_exist.patientID}.mp3')

                        patient_exist.haveSes = True
                        patient_exist.save()

                    except:

                        patient_exist.haveSes = False
                        patient_exist.save()

                else:

                    patient_exist.basicInfo.marriage = marriage
                    patient_exist.basicInfo.address = address
                    patient_exist.basicInfo.phone = phone
                    patient_exist.basicInfo.save()

                    patient = PatientInfo.objects.create(basicInfo=patient_exist.basicInfo,
                                                         patientID=patient_exist.patientID,
                                                         condition=5, operator=username)
                    # 更新该科室的病人数量
                    department.count += 1
                    department.save()

                    # 病人所在的科室
                    department_list = [department]
                    patient.department.add(*department_list)
                    patient.save()

                    try:

                        # 生成音频文件
                        # speech(name, department.arabic_name, patient.patientID)

                        text1 = 'إلى العِيَادَة'
                        textToAudio = name + ',' + text1 + ',' + department.arabic_name

                        language = 'ar'
                        myCall = gTTS(text=textToAudio, lang=language, slow=False)

                        myCall.save("C:/his/media/calling/"f'{patient.patientID}.mp3')

                    except:

                        patient.haveSes = False
                        patient.save()

            else:
                numberID = IDCreator()

                basicInfo = BasicInfo.objects.create(name=name, birthday=birthday, sex=gender,
                                                     marriage=marriage, address=address,
                                                     phone=phone, age=tempAge, operator=username)

                patient = PatientInfo.objects.create(basicInfo=basicInfo, patientID=numberID,
                                                     condition=5, operator=username)
                # 更新该科室的病人数量
                department.count += 1
                department.save()

                # 病人所在的科室
                department_list = [department]
                patient.department.add(*department_list)
                patient.save()

                try:

                    # 生成音频文件
                    # speech(name, department.arabic_name, patient.patientID)

                    text1 = 'إلى العِيَادَة'
                    textToAudio = name + ',' + text1 + ',' + department.arabic_name

                    language = 'ar'
                    myCall = gTTS(text=textToAudio, lang=language, slow=False)

                    myCall.save("C:/his/media/calling/"f'{patient.patientID}.mp3')

                except:
                    patient.haveSes = False
                    patient.save()


def uploadPolyclinicPatient(request):

    user = User.objects.get(name=request.session['name'])
    file = request.FILES.get('file')

    # 创建upload文件夹
    if not os.path.exists(settings.MEDIA_ROOT):
        os.makedirs(settings.MEDIA_ROOT)

    try:
        if file is None:
            return HttpResponse('请选择要上传的文件')

        # 循环二进制写入
        with open(settings.MEDIA_ROOT + "/excel/" + file.name, 'wb') as f:
            for i in file.readlines():
                f.write(i)

        # 写入 mysql
        writePolyclinicPatient(file.name, user.arabic_name)

    except Exception as e:
        return HttpResponse(e)

    return redirect('/polyclinicPatientList/')
