from io import BytesIO
from django.db.models import Sum
from django.http import HttpResponse, StreamingHttpResponse
from django.shortcuts import render, redirect
from datetime import datetime
import time
from django.urls import reverse
from django.utils import timezone
from department.models import Ward
from his import settings
from icu.part import func
from user.models import User
from user.views import login_required
from patient.models import PatientInfo
from icu.models import VitalSigns, DatesInICU
from django.core.paginator import Paginator
import os
import xlwt
import xlrd


@login_required
def addVitalSigns(request, patient_id, patient_num):
    """添加生命体征"""

    # 当前所需数据
    bloodPressureAverage = None
    patient = PatientInfo.objects.all().get(id=patient_id)
    username = request.session['name']
    user = User.objects.get(name=username)

    # 统计病房病人
    wards = user.authorityWard.filter(status=True)
    countOfTotal = wards.aggregate(Sum('count'))['count__sum']

    # 该用户能访问的病人
    patientsDoctor = PatientInfo.objects.filter(condition=1, department=user.authorityDepartment)
    patientsNurse = PatientInfo.objects.filter(condition=1, sickroom__in=user.authorityWard.all())

    # 获取前台传递过来的数据
    if request.method == 'POST':
        pulse = request.POST.get('pulse')
        bloodPressureMax = request.POST.get('bloodPressureMax')
        bloodPressureMin = request.POST.get('bloodPressureMin')
        if bloodPressureMax and bloodPressureMin:
            bloodPressureAverage = int(bloodPressureMin) + (int(bloodPressureMax) - int(bloodPressureMin)) / 3
        spo2 = request.POST.get('spo2')
        temperature = request.POST.get('temperature')
        breathingRate = request.POST.get('breathingRate')
        urineOutput = request.POST.get('urineOutput')
        oxygen = request.POST.get('oxygen')
        glucose = request.POST.get('glucose')
        frequency = request.POST.get('frequency')
        mode = request.POST.get('mode')
        vt = request.POST.get('vt')
        fio2 = request.POST.get('fio2')
        psv = request.POST.get('psv')
        peep = request.POST.get('peep')
        date = request.POST.get('date')
        recorder = username
        vitalSigns = VitalSigns.objects.create(recorder=recorder, patient_id=patient_id)
        if pulse:
            vitalSigns.pulse = pulse
        if bloodPressureMax:
            vitalSigns.bloodPressureMax = bloodPressureMax
        if bloodPressureMin:
            vitalSigns.bloodPressureMin = bloodPressureMin
        if bloodPressureAverage:
            vitalSigns.bloodPressureAverage = bloodPressureAverage
        if spo2:
            vitalSigns.spo2 = spo2
        if temperature:
            vitalSigns.temperature = temperature
        if breathingRate:
            vitalSigns.breathingRate = breathingRate
        if urineOutput:
            vitalSigns.urineOutput = urineOutput
        if oxygen:
            vitalSigns.oxygen = oxygen
        if glucose:
            vitalSigns.glucose = glucose
        if frequency:
            vitalSigns.frequency = frequency
        if mode:
            vitalSigns.mode = mode
        if vt:
            vitalSigns.vt = vt
        if fio2:
            vitalSigns.fio2 = fio2
        if psv:
            vitalSigns.psv = psv
        if peep:
            vitalSigns.peep = peep
        vitalSigns.date = date
        vitalSigns.save()

        return redirect('/viewVitalSigns/' + patient_id)

    if patient.condition:

        return render(request, 'icu/addVitalSigns.html', locals())

    else:
        return HttpResponse('This Patient already discharged, you can\'t add vitalSigns !')


@login_required
def viewVitalSigns(request, pindex, patient_id):
    """查看生命体征"""

    # 当前需要的信息
    patient = PatientInfo.objects.all().get(id=patient_id)
    username = request.session['name']
    user = User.objects.all().get(name=username)

    # 统计病房病人
    wards = user.authorityWard.filter(status=True)
    countOfTotal = wards.aggregate(Sum('count'))['count__sum']

    # 该用户能访问的病人
    patientsDoctor = PatientInfo.objects.filter(condition=1, department=user.authorityDepartment)
    patientsNurse = PatientInfo.objects.filter(condition=1, sickroom__in=user.authorityWard.all())

    # 通过病人id查找对应的信息
    vitalSignss = VitalSigns.objects.filter(patient_id=patient_id).order_by('-id')
    #
    # 分页
    paginator = Paginator(vitalSignss, 24)
    # 2. 获取pindex的数据
    if pindex == '':
        pindex = 1
    else:
        pindex = int(pindex)
    page = paginator.page(pindex)

    return render(request, 'icu/viewVitalSigns.html', locals())


@login_required
def editVitalSigns(request, vital_signs_id, patient_id, patient_num):
    """编辑"""

    # 获取当前需要编辑数据
    bloodPressureAverage = None
    patient = PatientInfo.objects.all().get(id=patient_id)
    username = request.session['name']
    user = User.objects.all().get(name=username)

    # 统计病房病人
    wards = user.authorityWard.filter(status=True)
    countOfTotal = wards.aggregate(Sum('count'))['count__sum']

    # 该用户能访问的病人
    patientsDoctor = PatientInfo.objects.filter(condition=1, department=user.authorityDepartment)
    patientsNurse = PatientInfo.objects.filter(condition=1, sickroom__in=user.authorityWard.all())

    # 通过医嘱id查找对应的生命体征
    vitalSigns = VitalSigns.objects.all().get(id=vital_signs_id)
    # 获取前台传递过来的数据
    if request.method == 'POST':
        pulse = request.POST.get('pulse')
        bloodPressureMax = request.POST.get('bloodPressureMax')
        bloodPressureMin = request.POST.get('bloodPressureMin')
        if bloodPressureMax and bloodPressureMin:
            bloodPressureAverage = int(bloodPressureMin) + (int(bloodPressureMax) - int(bloodPressureMin)) / 3
        spo2 = request.POST.get('spo2')
        temperature = request.POST.get('temperature')
        breathingRate = request.POST.get('breathingRate')
        urineOutput = request.POST.get('urineOutput')
        oxygen = request.POST.get('oxygen')
        glucose = request.POST.get('glucose')
        frequency = request.POST.get('frequency')
        mode = request.POST.get('mode')
        vt = request.POST.get('vt')
        fio2 = request.POST.get('fio2')
        psv = request.POST.get('psv')
        peep = request.POST.get('peep')
        date = request.POST.get('date')
        recorder = username
        # 更新数据库
        if pulse:
            vitalSigns.pulse = pulse
        else:
            vitalSigns.pulse = None

        if bloodPressureMax:
            vitalSigns.bloodPressureMax = bloodPressureMax
        else:
            vitalSigns.bloodPressureMax = None

        if bloodPressureMin:
            vitalSigns.bloodPressureMin = bloodPressureMin
        else:
            vitalSigns.bloodPressureMin = None

        if bloodPressureAverage:
            vitalSigns.bloodPressureAverage = bloodPressureAverage
        else:
            vitalSigns.bloodPressureAverage = None

        if spo2:
            vitalSigns.spo2 = spo2
        else:
            vitalSigns.spo2 = None

        if temperature:
            vitalSigns.temperature = temperature
        else:
            vitalSigns.temperature = None

        if breathingRate:
            vitalSigns.breathingRate = breathingRate
        else:
            vitalSigns.breathingRate = None

        if urineOutput:
            vitalSigns.urineOutput = urineOutput
        else:
            vitalSigns.urineOutput = None

        if oxygen:
            vitalSigns.oxygen = oxygen
        else:
            vitalSigns.oxygen = None

        if glucose:
            vitalSigns.glucose = glucose
        else:
            vitalSigns.glucose = None

        if frequency:
            vitalSigns.frequency = frequency
        else:
            vitalSigns.frequency = None

        if mode:
            vitalSigns.mode = mode
        else:
            vitalSigns.mode = None

        if vt:
            vitalSigns.vt = vt
        else:
            vitalSigns.vt = None

        if fio2:
            vitalSigns.fio2 = fio2
        else:
            vitalSigns.fio2 = None

        if psv:
            vitalSigns.psv = psv
        else:
            vitalSigns.psv = None

        if peep:
            vitalSigns.peep = peep
        else:
            vitalSigns.peep = None

        if date:
            vitalSigns.date = date
        vitalSigns.recorder = recorder
        vitalSigns.save()

        return redirect('/viewVitalSigns/' + patient_id)

    if patient.condition:

        return render(request, 'icu/editVitalSigns.html', locals())

    else:
        return HttpResponse('This Patient already discharged, you can\'t edit vitalSigns !')


@login_required
def deleteVitalSigns(request, vital_signs_id, patient_id):
    """删除"""

    patient = PatientInfo.objects.get(id=patient_id)

    if patient.condition:

        vitalSign = VitalSigns.objects.all().get(id=vital_signs_id)
        vitalSign.delete()

        return redirect('/viewVitalSigns/' + patient_id)

    else:
        return HttpResponse('This Patient already discharged, you can\'t delete !')


@login_required
def graphics(request, patient_id, patient_num):
    """折线图"""

    # 当前需要的信息
    patient = PatientInfo.objects.all().get(id=patient_id)
    username = request.session['name']
    user = User.objects.all().get(name=username)

    # 统计病房病人
    wards = user.authorityWard.filter(status=True)
    countOfTotal = wards.aggregate(Sum('count'))['count__sum']

    # 该用户能访问的病人
    patientsDoctor = PatientInfo.objects.filter(condition=1, department=user.authorityDepartment)
    patientsNurse = PatientInfo.objects.filter(condition=1, sickroom__in=user.authorityWard.all())

    vitalSignss = VitalSigns.objects.filter(patient_id=patient_id)

    # 计算入住ICU的天数
    dates = DatesInICU.objects.all().filter(icuPatient_id=patient_id).order_by('-id')

    for ic in dates:
        numOfDays = datetime.now() - ic.date
        numOfDays = numOfDays.days
        break

    pulse = []

    bloodPressureMax = []
    bloodPressureMin = []
    bloodPressureAverage = []

    spo2 = []

    temperature = []

    breathingRate = []

    urineOutput = []

    oxygen = []

    glucose = []

    date = []

    dateOfGraphic = 0
    part = 24
    if request.method == 'POST':
        dateOfGraphic = int(request.POST.get('date'))

    for signs in vitalSignss:

        if signs.pulse:
            pulse.append(signs.pulse)
            # datePulse.append(int(signs.date.strftime("%H")))
            this_date = datetime.strptime(str(signs.date), '%Y-%m-%d %H:%M:%S')
            this_date = time.mktime(this_date.timetuple())
            # date.append(this_date * 1000 - 25200000)
            # date.append(this_date * 1000 + 7200000)
            date.append(this_date * 1000 + 10800000)

            # timestamp = time.mktime(signs.date.timetuple())
            # date.append(int(timestamp * 1000))

            tempUp = func(pulse, part)  # 用func函数把数据分成几块，每块的数量为24
            tempDown = func(date, part)
            tempPulse = {}  # 这个字典的键：保存第几块，值：保存这块中的数据
            tempDate = {}
            count = []  # 记录总共有几块
            j = 1
            for i in tempUp:
                tempPulse[j] = i
                count.append(j)
                j += 1

            j = 1
            for i in tempDown:
                tempDate[j] = i
                j += 1

            dataPulse = []  # 存储每块的数据
            dateAll = []

            for key in tempPulse:
                if dateOfGraphic == 0:
                    dataPulse = pulse
                elif key == dateOfGraphic:
                    dataPulse = tempPulse[key]

            for key in tempDate:
                if dateOfGraphic == 0:
                    dateAll = date
                elif key == dateOfGraphic:
                    dateAll = tempDate[key]

        if signs.bloodPressureMax and signs.bloodPressureMin:
            bloodPressureMax.append(signs.bloodPressureMax)
            bloodPressureMin.append(signs.bloodPressureMin)
            bloodPressureAverage.append(signs.bloodPressureAverage)

            tempMax = func(bloodPressureMax, part)  # 用func函数把数据分成几块，每块的数量为24
            tempMin = func(bloodPressureMin, part)  # 用func函数把数据分成几块，每块的数量为24
            tempAverage = func(bloodPressureAverage, part)  # 用func函数把数据分成几块，每块的数量为24
            tempPressureMax = {}  # 这个字典的键：保存第几块，值：保存这块中的数据
            tempPressureMin = {}  # 这个字典的键：保存第几块，值：保存这块中的数据
            tempPressureAverage = {}  # 这个字典的键：保存第几块，值：保存这块中的数据

            j = 1
            for i in tempMax:
                tempPressureMax[j] = i
                j += 1

            j = 1
            for i in tempMin:
                tempPressureMin[j] = i
                j += 1

            j = 1
            for i in tempAverage:
                tempPressureAverage[j] = i
                j += 1

            dataPressureMax = []  # 存储每块的数据
            dataPressureMin = []  # 存储每块的数据
            dataPressureAverage = []  # 存储每块的数据

            for key in tempPressureMax:
                if dateOfGraphic == 0:
                    dataPressureMax = bloodPressureMax
                elif key == dateOfGraphic:
                    dataPressureMax = tempPressureMax[key]

            for key in tempPressureMin:
                if dateOfGraphic == 0:
                    dataPressureMin = bloodPressureMin
                elif key == dateOfGraphic:
                    dataPressureMin = tempPressureMin[key]

            for key in tempPressureAverage:
                if dateOfGraphic == 0:
                    dataPressureAverage = bloodPressureAverage
                elif key == dateOfGraphic:
                    dataPressureAverage = tempPressureAverage[key]

        if signs.spo2:
            spo2.append(signs.spo2)

            temp = func(spo2, part)  # 用func函数把数据分成几块，每块的数量为24
            tempSpo2 = {}  # 这个字典的键：保存第几块，值：保存这块中的数据

            j = 1
            for i in temp:
                tempSpo2[j] = i
                j += 1

            dataSpo2 = []  # 存储每块的数据

            for key in tempSpo2:
                if dateOfGraphic == 0:
                    dataSpo2 = spo2
                elif key == dateOfGraphic:
                    dataSpo2 = tempSpo2[key]

        if signs.temperature:
            temperature.append(signs.temperature)

            temp = func(temperature, part)  # 用func函数把数据分成几块，每块的数量为24
            tempTemperature = {}  # 这个字典的键：保存第几块，值：保存这块中的数据

            j = 1
            for i in temp:
                tempTemperature[j] = i
                j += 1

            dataTemperature = []  # 存储每块的数据

            for key in tempTemperature:
                if dateOfGraphic == 0:
                    dataTemperature = temperature
                elif key == dateOfGraphic:
                    dataTemperature = tempTemperature[key]

        if signs.breathingRate:
            breathingRate.append(signs.breathingRate)

            temp = func(breathingRate, part)  # 用func函数把数据分成几块，每块的数量为24
            tempBreathingRate = {}  # 这个字典的键：保存第几块，值：保存这块中的数据

            j = 1
            for i in temp:
                tempBreathingRate[j] = i
                j += 1

            dataBreathingRate = []  # 存储每块的数据

            for key in tempBreathingRate:
                if dateOfGraphic == 0:
                    dataBreathingRate = breathingRate
                elif key == dateOfGraphic:
                    dataBreathingRate = tempBreathingRate[key]

        if signs.urineOutput:
            urineOutput.append(signs.urineOutput)

            temp = func(urineOutput, part)  # 用func函数把数据分成几块，每块的数量为24
            tempUrineOutput = {}  # 这个字典的键：保存第几块，值：保存这块中的数据

            j = 1
            for i in temp:
                tempUrineOutput[j] = i
                j += 1

            dataUrineOutput = []  # 存储每块的数据

            for key in tempUrineOutput:
                if dateOfGraphic == 0:
                    dataUrineOutput = urineOutput
                elif key == dateOfGraphic:
                    dataUrineOutput = tempUrineOutput[key]

        if signs.oxygen:
            oxygen.append(signs.oxygen)

            temp = func(oxygen, part)  # 用func函数把数据分成几块，每块的数量为24
            tempOxygen = {}  # 这个字典的键：保存第几块，值：保存这块中的数据

            j = 1
            for i in temp:
                tempOxygen[j] = i
                j += 1

            dataOxygen = []  # 存储每块的数据

            for key in tempOxygen:
                if dateOfGraphic == 0:
                    dataOxygen = oxygen
                elif key == dateOfGraphic:
                    dataOxygen = tempOxygen[key]

        if signs.glucose:
            glucose.append(signs.glucose)

            temp = func(glucose, part)  # 用func函数把数据分成几块，每块的数量为24
            tempGlucose = {}  # 这个字典的键：保存第几块，值：保存这块中的数据

            j = 1
            for i in temp:
                tempGlucose[j] = i
                j += 1

            dataGlucose = []  # 存储每块的数据

            for key in tempGlucose:
                if dateOfGraphic == 0:
                    dataGlucose = glucose
                elif key == dateOfGraphic:
                    dataGlucose = tempGlucose[key]

    return render(request, 'icu/graphics.html', locals())
