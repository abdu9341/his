from django.db.models import Q, Sum
from django.http import StreamingHttpResponse, HttpResponse
from django.shortcuts import render, redirect
from department.models import *
from user.views import login_required
from laboratory.models import *
from operation.models import Operation
from discharge.models import Discharge
from patient.models import *
from user.models import User
from django.utils import timezone
from icu.models import VitalSigns
from io import BytesIO
import xlwt


@login_required
def index(request):

    user = User.objects.all().get(name=request.session['name'])

    # 更新当前模板内容
    user.currentTemplateUrl = 'index'
    user.save()

    # 该用户能访问的病人
    patientsDoctor = PatientInfo.objects.filter(condition=1, department=user.authorityDepartment)
    patientsNurse = PatientInfo.objects.filter(condition=1, sickroom__in=user.authorityWard.all())

    # 统计病房病人
    wards = user.authorityWard.filter(status=True)
    countOfTotal = wards.aggregate(Sum('count'))['count__sum']

    return render(request, 'home/index.html', locals())


@login_required
def statistics(request):
    """统计病人"""

    user = User.objects.all().get(name=request.session['name'])

    # 统计病房病人
    wards = user.authorityWard.filter(status=True)
    countOfTotal = wards.aggregate(Sum('count'))['count__sum']

    patients = PatientInfo()
    if request.method == 'POST':
        types = request.POST.get('types')
        startDate = request.POST.get('startDate')
        endDate = request.POST.get('endDate')

        date = (startDate, endDate)

        if types == 'Hospitalization':
            patients = PatientInfo.objects.filter(condition=1, enterDate__range=date)

        elif types == 'Operation':
            operations = Operation.objects.filter(begin__range=date)

        elif types == 'Discharge':
            patients = PatientInfo.objects.filter(discharge__leaveDate__range=date)

        elif types == 'BothOfThem':
            patients = PatientInfo.objects.filter(Q(enterDate__range=date) | Q(discharge__leaveDate__range=date))

        count = patients.count()

    return render(request, 'home/index.html', locals())


@login_required
def excelPatientInfo(request):
    """导出excel文件"""

    if request.method == 'POST':
        types = request.POST.get('types')
        start = request.POST.get('start')
        end = request.POST.get('end')

        date = (start, end)

        if types == 'Hospitalization':
            patients = PatientInfo.objects.filter(condition=1, enterDate__range=date)

            if patients:

                # 创建工作簿
                patientPage = xlwt.Workbook(encoding='utf8')

                # 添加第一页数据表
                patientInfo = patientPage.add_sheet(u"PatientInfo")

                # 写入表头
                patientInfo.write(0, 0, u'اسم المريض')
                patientInfo.write(0, 1, u'العمر')
                patientInfo.write(0, 2, u'الجنس')
                patientInfo.write(0, 3, u'الحالة العائلية')
                patientInfo.write(0, 4, u'السكن')
                patientInfo.write(0, 5, u'رقم هاتف')
                patientInfo.write(0, 6, u'تاريخ القبول')
                patientInfo.write(0, 7, u'رقم المريض')
                patientInfo.write(0, 8, u'جناح')
                patientInfo.write(0, 9, u'تشخبص')
                patientInfo.write(0, 10, u'قسم القبول')
                patientInfo.write(0, 11, u'العامل')

                # 写入每一行对应的数据
                excel_row = 1
                for patient in patients:
                    patientInfo.write(excel_row, 0, patient.basicInfo.name)
                    patientInfo.write(excel_row, 1, patient.basicInfo.age)
                    patientInfo.write(excel_row, 2, patient.basicInfo.sex)
                    patientInfo.write(excel_row, 3, patient.basicInfo.marriage)
                    patientInfo.write(excel_row, 4, patient.basicInfo.address)
                    patientInfo.write(excel_row, 5, patient.basicInfo.phone)
                    patientInfo.write(excel_row, 6, patient.enterDate.strftime("%Y-%m-%d, %H:%M:%S"))
                    patientInfo.write(excel_row, 7, patient.patientID)
                    patientInfo.write(excel_row, 8, patient.sickroom.arabic_name)
                    patientInfo.write(excel_row, 9, patient.diagnosis)

                    # 登记科室
                    department_list = []
                    departments = patient.department.all()
                    for department in departments:
                        department_list.append("  ")
                        department_list.append(department.arabic_name)

                    patientInfo.write(excel_row, 10, department_list)

                    patientInfo.write(excel_row, 11, patient.operator)

                    excel_row += 1

                # 实现下载
                output = BytesIO()
                patientPage.save(output)
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

        elif types == 'Operation':
            operations = Operation.objects.filter(begin__range=date)

            if operations:

                # 创建工作簿
                patientPage = xlwt.Workbook(encoding='utf8')

                # 添加第一页数据表
                patientInfo = patientPage.add_sheet(u"OperationInfo")

                # 写入表头
                patientInfo.write(0, 0, u'اسم المريض')
                patientInfo.write(0, 1, u'العمر')
                patientInfo.write(0, 2, u'الجنس')
                patientInfo.write(0, 3, u'الحالة العائلية')
                patientInfo.write(0, 4, u'السكن')
                patientInfo.write(0, 5, u'العمل الجراحي')
                patientInfo.write(0, 6, u'الطبيب الجراح')
                patientInfo.write(0, 7, u'الطبيب المساعد')
                patientInfo.write(0, 8, u'فني عمليات')
                patientInfo.write(0, 9, u'المخدر')
                patientInfo.write(0, 10, u'نوع التخدير')
                patientInfo.write(0, 11, u'نوع العمل')
                patientInfo.write(0, 12, u'القاعة')
                patientInfo.write(0, 13, u'التاريخ')
                patientInfo.write(0, 14, u'ساعة:مدة')
                patientInfo.write(0, 15, u'العامل')

                # 写入每一行对应的数据
                excel_row = 1
                for operation in operations:
                    patientInfo.write(excel_row, 0, operation.patient.basicInfo.name)
                    patientInfo.write(excel_row, 1, operation.patient.basicInfo.age)
                    patientInfo.write(excel_row, 2, operation.patient.basicInfo.sex)
                    patientInfo.write(excel_row, 3, operation.patient.basicInfo.marriage)
                    patientInfo.write(excel_row, 4, operation.patient.basicInfo.address)
                    patientInfo.write(excel_row, 5, operation.name)
                    patientInfo.write(excel_row, 6, operation.doctor)
                    patientInfo.write(excel_row, 7, operation.assistant)
                    patientInfo.write(excel_row, 8, operation.surgicalNurse)
                    patientInfo.write(excel_row, 9, operation.anesthetist)
                    patientInfo.write(excel_row, 10, operation.typesNarcosis)
                    patientInfo.write(excel_row, 11, operation.typesOperation)
                    patientInfo.write(excel_row, 12, operation.roomNo)
                    patientInfo.write(excel_row, 13, operation.begin.strftime("%Y-%m-%d, %H:%M:%S"))
                    patientInfo.write(excel_row, 14, operation.timeOfOperation)
                    patientInfo.write(excel_row, 15, operation.operator)

                    excel_row += 1

                # 实现下载
                output = BytesIO()
                patientPage.save(output)
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

        elif types == 'Polyclinic':
            patients = PatientInfo.objects.filter(condition__range=(5, 8), enterDate__range=date)

            if patients:

                # 创建工作簿
                patientPage = xlwt.Workbook(encoding='utf8')

                # 添加第一页数据表
                patientInfo = patientPage.add_sheet(u"PatientInfo")

                # 写入表头
                patientInfo.write(0, 0, u'اسم المريض')
                patientInfo.write(0, 1, u'العمر')
                patientInfo.write(0, 2, u'الجنس')
                patientInfo.write(0, 3, u'الحالة العائلية')
                patientInfo.write(0, 4, u'السكن')
                patientInfo.write(0, 5, u'رقم هاتف')
                patientInfo.write(0, 6, u'تاريخ القبول')
                patientInfo.write(0, 7, u'رقم المريض')
                patientInfo.write(0, 8, u'جناح')
                patientInfo.write(0, 9, u'تشخبص')
                patientInfo.write(0, 10, u'قسم القبول')
                patientInfo.write(0, 11, u'العامل')

                # 写入每一行对应的数据
                excel_row = 1
                for patient in patients:
                    patientInfo.write(excel_row, 0, patient.basicInfo.name)
                    patientInfo.write(excel_row, 1, patient.basicInfo.age)
                    patientInfo.write(excel_row, 2, patient.basicInfo.sex)
                    patientInfo.write(excel_row, 3, patient.basicInfo.marriage)
                    patientInfo.write(excel_row, 4, patient.basicInfo.address)
                    patientInfo.write(excel_row, 5, patient.basicInfo.phone)
                    patientInfo.write(excel_row, 6, patient.enterDate.strftime("%Y-%m-%d, %H:%M:%S"))
                    patientInfo.write(excel_row, 7, patient.patientID)
                    patientInfo.write(excel_row, 8, "عيادة")
                    patientInfo.write(excel_row, 9, patient.diagnosis)

                    # 登记科室
                    department_list = []
                    departments = patient.department.all()
                    for department in departments:
                        department_list.append("  ")
                        department_list.append(department.arabic_name)

                    patientInfo.write(excel_row, 10, department_list)

                    patientInfo.write(excel_row, 11, patient.operator)

                    excel_row += 1

                # 实现下载
                output = BytesIO()
                patientPage.save(output)
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

        elif types == 'Emergency':
            patients = PatientInfo.objects.filter(condition__range=(2, 3), enterDate__range=date)

            if patients:

                # 创建工作簿
                patientPage = xlwt.Workbook(encoding='utf8')

                # 添加第一页数据表
                patientInfo = patientPage.add_sheet(u"PatientInfo")

                # 写入表头
                patientInfo.write(0, 0, u'اسم المريض')
                patientInfo.write(0, 1, u'العمر')
                patientInfo.write(0, 2, u'الجنس')
                patientInfo.write(0, 3, u'تاريخ القبول')
                patientInfo.write(0, 4, u'جناح')
                patientInfo.write(0, 5, u'قسم القبول')
                patientInfo.write(0, 6, u'العامل')

                # 写入每一行对应的数据
                excel_row = 1
                for patient in patients:
                    patientInfo.write(excel_row, 0, patient.basicInfo.name)
                    patientInfo.write(excel_row, 1, patient.basicInfo.age)
                    patientInfo.write(excel_row, 2, patient.basicInfo.sex)
                    patientInfo.write(excel_row, 3, patient.enterDate.strftime("%Y-%m-%d, %H:%M:%S"))
                    patientInfo.write(excel_row, 4, "اسعاف")

                    # 登记科室
                    department_list = []
                    departments = patient.department.all()
                    for department in departments:
                        department_list.append("  ")
                        department_list.append(department.arabic_name)
                    patientInfo.write(excel_row, 5, department_list)

                    patientInfo.write(excel_row, 6, patient.operator)

                    excel_row += 1

                # 实现下载
                output = BytesIO()
                patientPage.save(output)
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

        elif types == 'Discharge':
            patients = PatientInfo.objects.filter(condition=0, enterDate__range=date)

            if patients:

                # 创建工作簿
                patientPage = xlwt.Workbook(encoding='utf8')

                # 添加第一页数据表
                patientInfo = patientPage.add_sheet(u"PatientInfo")

                # 写入表头
                patientInfo.write(0, 0, u'اسم المريض')
                patientInfo.write(0, 1, u'العمر')
                patientInfo.write(0, 2, u'الجنس')
                patientInfo.write(0, 3, u'الحالة العائلية')
                patientInfo.write(0, 4, u'السكن')
                patientInfo.write(0, 5, u'رقم هاتف')
                patientInfo.write(0, 6, u'تاريخ القبول')
                patientInfo.write(0, 7, u'رقم المريض')
                patientInfo.write(0, 8, u'جناح')
                patientInfo.write(0, 9, u'تشخبص')
                patientInfo.write(0, 10, u'قسم القبول')
                patientInfo.write(0, 11, u'حالة التخريج')
                patientInfo.write(0, 12, u'تاريخ التخريج')
                patientInfo.write(0, 13, u'قسم التخريج')
                patientInfo.write(0, 14, u'العامل')

                # 写入每一行对应的数据
                excel_row = 1
                for patient in patients:
                    patientInfo.write(excel_row, 0, patient.basicInfo.name)
                    patientInfo.write(excel_row, 1, patient.basicInfo.age)
                    patientInfo.write(excel_row, 2, patient.basicInfo.sex)
                    patientInfo.write(excel_row, 3, patient.basicInfo.marriage)
                    patientInfo.write(excel_row, 4, patient.basicInfo.address)
                    patientInfo.write(excel_row, 5, patient.basicInfo.phone)
                    patientInfo.write(excel_row, 6, patient.enterDate.strftime("%Y-%m-%d, %H:%M:%S"))
                    patientInfo.write(excel_row, 7, patient.patientID)
                    patientInfo.write(excel_row, 8, patient.sickroom.arabic_name)
                    patientInfo.write(excel_row, 9, patient.diagnosis)

                    # 登记科室
                    department_list = []
                    departments = patient.department.all()
                    for department in departments:
                        department_list.append("  ")
                        department_list.append(department.arabic_name)
                    patientInfo.write(excel_row, 10, department_list)

                    # 出院记录
                    discharge = Discharge.objects.filter(patient=patient).first()
                    patientInfo.write(excel_row, 11, discharge.dischargeStatus)
                    patientInfo.write(excel_row, 12, discharge.leaveDate.strftime("%Y-%m-%d, %H:%M:%S"))
                    patientInfo.write(excel_row, 13, discharge.leavingDepartment)

                    patientInfo.write(excel_row, 14, patient.operator)

                    excel_row += 1

                # 实现下载
                output = BytesIO()
                patientPage.save(output)
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

        elif types == 'AllPatients':
            patients = PatientInfo.objects.filter(enterDate__range=date)

            if patients:

                # 创建工作簿
                patientPage = xlwt.Workbook(encoding='utf8')

                # 添加第一页数据表
                patientInfo = patientPage.add_sheet(u"PatientInfo")

                # 写入表头
                patientInfo.write(0, 0, u'اسم المريض')
                patientInfo.write(0, 1, u'العمر')
                patientInfo.write(0, 2, u'الجنس')
                patientInfo.write(0, 3, u'الحالة العائلية')
                patientInfo.write(0, 4, u'السكن')
                patientInfo.write(0, 5, u'رقم هاتف')
                patientInfo.write(0, 6, u'تاريخ القبول')
                patientInfo.write(0, 7, u'رقم المريض')
                patientInfo.write(0, 8, u'جناح')
                patientInfo.write(0, 9, u'تشخبص')
                patientInfo.write(0, 10, u'قسم القبول')
                patientInfo.write(0, 11, u'حالة التخريج')
                patientInfo.write(0, 12, u'تاريخ التخريج')
                patientInfo.write(0, 13, u'قسم التخريج')
                patientInfo.write(0, 14, u'العامل')

                # 写入每一行对应的数据
                excel_row = 1
                for patient in patients:
                    patientInfo.write(excel_row, 0, patient.basicInfo.name)
                    patientInfo.write(excel_row, 1, patient.basicInfo.age)
                    patientInfo.write(excel_row, 2, patient.basicInfo.sex)
                    patientInfo.write(excel_row, 3, patient.basicInfo.marriage)
                    patientInfo.write(excel_row, 4, patient.basicInfo.address)
                    patientInfo.write(excel_row, 5, patient.basicInfo.phone)
                    patientInfo.write(excel_row, 6, patient.enterDate.strftime("%Y-%m-%d, %H:%M:%S"))
                    patientInfo.write(excel_row, 7, patient.patientID)

                    # 住院病房
                    if patient.sickroom:
                        patientInfo.write(excel_row, 8, patient.sickroom.arabic_name)

                    patientInfo.write(excel_row, 9, patient.diagnosis)

                    # 登记科室
                    department_list = []
                    departments = patient.department.all()
                    for department in departments:
                        department_list.append("  ")
                        department_list.append(department.arabic_name)

                    patientInfo.write(excel_row, 10, department_list)

                    # 出院记录
                    discharge = Discharge.objects.filter(patient=patient).first()
                    if discharge:
                        patientInfo.write(excel_row, 11, discharge.dischargeStatus)
                        patientInfo.write(excel_row, 12, discharge.leaveDate.strftime("%Y-%m-%d, %H:%M:%S"))
                        patientInfo.write(excel_row, 13, discharge.leavingDepartment)

                    patientInfo.write(excel_row, 14, patient.operator)

                    excel_row += 1

                # 实现下载
                output = BytesIO()
                patientPage.save(output)
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

        elif types == 'Laboratory':
            cbcObj = CBC.objects.filter(date__range=date)
            coagulationObj = Coagulation.objects.filter(date__range=date)
            biochemistryObj = Biochemistry.objects.filter(date__range=date)
            electrolytesObj = Electrolytes.objects.filter(date__range=date)
            abgObj = ABG.objects.filter(date__range=date)
            serologyObj = Serology.objects.filter(date__range=date)
            urineAnalysisObj = UrineAnalysis.objects.filter(date__range=date)
            csfObj = CSF.objects.filter(date__range=date)
            antibioticsObj = Antibiotics.objects.filter(date__range=date)
            hormonesObj = Hormones.objects.filter(date__range=date)

            # 创建工作簿
            laboratoryPage = xlwt.Workbook(encoding='utf8')

            if cbcObj:

                # 添加第一页数据表
                cbcInfo = laboratoryPage.add_sheet(u"CBC")

                # 写入表头
                cbcInfo.write(0, 0, u'اسم المريض')
                cbcInfo.write(0, 1, u'العمر')
                cbcInfo.write(0, 2, u'الجنس')
                cbcInfo.write(0, 3, u'رقم المريض')
                cbcInfo.write(0, 4, u'RBC')
                cbcInfo.write(0, 5, u'MCV')
                cbcInfo.write(0, 6, u'MCH')
                cbcInfo.write(0, 7, u'MCHC')
                cbcInfo.write(0, 8, u'RDW')
                cbcInfo.write(0, 9, u'Blood Group')
                cbcInfo.write(0, 10, u'Hemoglobin')
                cbcInfo.write(0, 11, u'Hematocrite')
                cbcInfo.write(0, 12, u'WBC')
                cbcInfo.write(0, 13, u'Gran')
                cbcInfo.write(0, 14, u'LYM')
                cbcInfo.write(0, 15, u'MID')
                cbcInfo.write(0, 16, u'PLT')
                cbcInfo.write(0, 17, u'EsrH1')
                cbcInfo.write(0, 18, u'EsrH2')
                cbcInfo.write(0, 19, u'Date')
                cbcInfo.write(0, 20, u'Recorder')

                # 写入每一行对应的数据
                excel_row = 1

                for cbc in cbcObj:
                    cbcInfo.write(excel_row, 0, cbc.patient.basicInfo.name)
                    cbcInfo.write(excel_row, 1, cbc.patient.basicInfo.age)
                    cbcInfo.write(excel_row, 2, cbc.patient.basicInfo.sex)
                    cbcInfo.write(excel_row, 3, cbc.patient.patientID)
                    cbcInfo.write(excel_row, 4, cbc.rbc)
                    cbcInfo.write(excel_row, 5, cbc.mcv)
                    cbcInfo.write(excel_row, 6, cbc.mch)
                    cbcInfo.write(excel_row, 7, cbc.mchc)
                    cbcInfo.write(excel_row, 8, cbc.rdw)
                    cbcInfo.write(excel_row, 9, cbc.bloodGroup)
                    cbcInfo.write(excel_row, 10, cbc.hemoglobin)
                    cbcInfo.write(excel_row, 11, cbc.hematocrite)
                    cbcInfo.write(excel_row, 12, cbc.wbc)
                    cbcInfo.write(excel_row, 13, cbc.gran)
                    cbcInfo.write(excel_row, 14, cbc.lym)
                    cbcInfo.write(excel_row, 15, cbc.mid)
                    cbcInfo.write(excel_row, 16, cbc.plt)
                    cbcInfo.write(excel_row, 17, cbc.esrH1)
                    cbcInfo.write(excel_row, 18, cbc.esrH2)
                    cbcInfo.write(excel_row, 19, cbc.date.strftime("%Y-%m-%d, %H:%M:%S"))
                    cbcInfo.write(excel_row, 20, cbc.recorder)

                    excel_row += 1

            if coagulationObj:
                coagulationInfo = laboratoryPage.add_sheet(u"Coagulation")

                # 写入表头
                coagulationInfo.write(0, 0, u'اسم المريض')
                coagulationInfo.write(0, 1, u'العمر')
                coagulationInfo.write(0, 2, u'الجنس')
                coagulationInfo.write(0, 3, u'رقم المريض')
                coagulationInfo.write(0, 4, u'PT')
                coagulationInfo.write(0, 5, u'INR')
                coagulationInfo.write(0, 6, u'APTT')
                coagulationInfo.write(0, 7, u'Bleed Time')
                coagulationInfo.write(0, 8, u'Clot Time')
                coagulationInfo.write(0, 9, u'Act')
                coagulationInfo.write(0, 10, u'Date')
                coagulationInfo.write(0, 11, u'Recorder')

                # 写入每一行对应的数据
                excel_row = 1

                for coagulation in coagulationObj:
                    coagulationInfo.write(excel_row, 0, coagulation.patient.basicInfo.name)
                    coagulationInfo.write(excel_row, 1, coagulation.patient.basicInfo.age)
                    coagulationInfo.write(excel_row, 2, coagulation.patient.basicInfo.sex)
                    coagulationInfo.write(excel_row, 3, coagulation.patient.patientID)
                    coagulationInfo.write(excel_row, 4, coagulation.pt)
                    coagulationInfo.write(excel_row, 5, coagulation.inr)
                    coagulationInfo.write(excel_row, 6, coagulation.aptt)
                    coagulationInfo.write(excel_row, 7, coagulation.bleedTime)
                    coagulationInfo.write(excel_row, 8, coagulation.clotTime)
                    coagulationInfo.write(excel_row, 9, coagulation.act)
                    coagulationInfo.write(excel_row, 10, coagulation.date.strftime("%Y-%m-%d, %H:%M:%S"))
                    coagulationInfo.write(excel_row, 11, coagulation.recorder)

                    excel_row += 1

            if biochemistryObj:
                biochemistryInfo = laboratoryPage.add_sheet(u"Biochemistry")

                # 写入表头
                biochemistryInfo.write(0, 0, u'اسم المريض')
                biochemistryInfo.write(0, 1, u'العمر')
                biochemistryInfo.write(0, 2, u'الجنس')
                biochemistryInfo.write(0, 3, u'رقم المريض')
                biochemistryInfo.write(0, 4, u'Glucose')
                biochemistryInfo.write(0, 5, u'Urea')
                biochemistryInfo.write(0, 6, u'Creatine')
                biochemistryInfo.write(0, 7, u'SGPT')
                biochemistryInfo.write(0, 8, u'SGOT')
                biochemistryInfo.write(0, 9, u'BiliTotal')
                biochemistryInfo.write(0, 10, u'BiliDirect')
                biochemistryInfo.write(0, 11, u'BiliIndirect')
                biochemistryInfo.write(0, 12, u'ALP')
                biochemistryInfo.write(0, 13, u'Amylase')
                biochemistryInfo.write(0, 14, u'LDH')
                biochemistryInfo.write(0, 15, u'Albumin')
                biochemistryInfo.write(0, 16, u'Total Protein')
                biochemistryInfo.write(0, 17, u'Ck')
                biochemistryInfo.write(0, 18, u'Ck Mb')
                biochemistryInfo.write(0, 19, u'Lipase')
                biochemistryInfo.write(0, 20, u'Uric Acid')
                biochemistryInfo.write(0, 21, u'Triglycerid')
                biochemistryInfo.write(0, 22, u'Cholesterol')
                biochemistryInfo.write(0, 23, u'Crp')
                biochemistryInfo.write(0, 24, u'Aslo')
                biochemistryInfo.write(0, 25, u'Rf')
                biochemistryInfo.write(0, 26, u'Date')
                biochemistryInfo.write(0, 27, u'Recorder')

                # 写入每一行对应的数据
                excel_row = 1

                for biochemistry in biochemistryObj:
                    biochemistryInfo.write(excel_row, 0, biochemistry.patient.basicInfo.name)
                    biochemistryInfo.write(excel_row, 1, biochemistry.patient.basicInfo.age)
                    biochemistryInfo.write(excel_row, 2, biochemistry.patient.basicInfo.sex)
                    biochemistryInfo.write(excel_row, 3, biochemistry.patient.patientID)
                    biochemistryInfo.write(excel_row, 4, biochemistry.glucose)
                    biochemistryInfo.write(excel_row, 5, biochemistry.urea)
                    biochemistryInfo.write(excel_row, 6, biochemistry.creatine)
                    biochemistryInfo.write(excel_row, 7, biochemistry.sgpt)
                    biochemistryInfo.write(excel_row, 8, biochemistry.sgot)
                    biochemistryInfo.write(excel_row, 9, biochemistry.biliTotal)
                    biochemistryInfo.write(excel_row, 10, biochemistry.biliDirect)
                    biochemistryInfo.write(excel_row, 11, biochemistry.biliIndirect)
                    biochemistryInfo.write(excel_row, 12, biochemistry.alp)
                    biochemistryInfo.write(excel_row, 13, biochemistry.amylase)
                    biochemistryInfo.write(excel_row, 14, biochemistry.ldh)
                    biochemistryInfo.write(excel_row, 15, biochemistry.albumin)
                    biochemistryInfo.write(excel_row, 16, biochemistry.totalProtein)
                    biochemistryInfo.write(excel_row, 17, biochemistry.ck)
                    biochemistryInfo.write(excel_row, 18, biochemistry.ck_mb)
                    biochemistryInfo.write(excel_row, 19, biochemistry.lipase)
                    biochemistryInfo.write(excel_row, 20, biochemistry.uric_acid)
                    biochemistryInfo.write(excel_row, 21, biochemistry.triglycerid)
                    biochemistryInfo.write(excel_row, 22, biochemistry.cholesterol)
                    biochemistryInfo.write(excel_row, 23, biochemistry.crp)
                    biochemistryInfo.write(excel_row, 24, biochemistry.aslo)
                    biochemistryInfo.write(excel_row, 25, biochemistry.rf)
                    biochemistryInfo.write(excel_row, 26, biochemistry.date.strftime("%Y-%m-%d, %H:%M:%S"))
                    biochemistryInfo.write(excel_row, 27, biochemistry.recorder)

                    excel_row += 1

            if electrolytesObj:
                electrolytesInfo = laboratoryPage.add_sheet(u"Electrolytes")

                # 写入表头
                electrolytesInfo.write(0, 0, u'اسم المريض')
                electrolytesInfo.write(0, 1, u'العمر')
                electrolytesInfo.write(0, 2, u'الجنس')
                electrolytesInfo.write(0, 3, u'رقم المريض')
                electrolytesInfo.write(0, 4, u'Na')
                electrolytesInfo.write(0, 5, u'K')
                electrolytesInfo.write(0, 6, u'Cl')
                electrolytesInfo.write(0, 7, u'TCa')
                electrolytesInfo.write(0, 8, u'NCa')
                electrolytesInfo.write(0, 9, u'ICa')
                electrolytesInfo.write(0, 10, u'Iron')
                electrolytesInfo.write(0, 11, u'Mg')
                electrolytesInfo.write(0, 12, u'Phosphorus')
                electrolytesInfo.write(0, 13, u'Date')
                electrolytesInfo.write(0, 14, u'Recorder')

                # 写入每一行对应的数据
                excel_row = 1

                for electrolytes in electrolytesObj:
                    electrolytesInfo.write(excel_row, 0, electrolytes.patient.basicInfo.name)
                    electrolytesInfo.write(excel_row, 1, electrolytes.patient.basicInfo.age)
                    electrolytesInfo.write(excel_row, 2, electrolytes.patient.basicInfo.sex)
                    electrolytesInfo.write(excel_row, 3, electrolytes.patient.patientID)
                    electrolytesInfo.write(excel_row, 4, electrolytes.na)
                    electrolytesInfo.write(excel_row, 5, electrolytes.k)
                    electrolytesInfo.write(excel_row, 6, electrolytes.cl)
                    electrolytesInfo.write(excel_row, 7, electrolytes.tca)
                    electrolytesInfo.write(excel_row, 8, electrolytes.nca)
                    electrolytesInfo.write(excel_row, 9, electrolytes.ica)
                    electrolytesInfo.write(excel_row, 10, electrolytes.iron)
                    electrolytesInfo.write(excel_row, 11, electrolytes.mg)
                    electrolytesInfo.write(excel_row, 12, electrolytes.phosphorus)
                    electrolytesInfo.write(excel_row, 13, electrolytes.date.strftime("%Y-%m-%d, %H:%M:%S"))
                    electrolytesInfo.write(excel_row, 14, electrolytes.recorder)

                    excel_row += 1

            if abgObj:
                abgInfo = laboratoryPage.add_sheet(u"ABG")

                # 写入表头
                abgInfo.write(0, 0, u'اسم المريض')
                abgInfo.write(0, 1, u'العمر')
                abgInfo.write(0, 2, u'الجنس')
                abgInfo.write(0, 3, u'رقم المريض')
                abgInfo.write(0, 4, u'PH')
                abgInfo.write(0, 5, u'Pc02')
                abgInfo.write(0, 6, u'P02')
                abgInfo.write(0, 7, u'Na')
                abgInfo.write(0, 8, u'K')
                abgInfo.write(0, 9, u'Ca1')
                abgInfo.write(0, 10, u'Glucose')
                abgInfo.write(0, 11, u'Lac')
                abgInfo.write(0, 12, u'HC03')
                abgInfo.write(0, 13, u'Beecf')
                abgInfo.write(0, 14, u'S02c')
                abgInfo.write(0, 15, u'Fi02')
                abgInfo.write(0, 16, u'Date')
                abgInfo.write(0, 17, u'Recorder')

                # 写入每一行对应的数据
                excel_row = 1

                for abg in abgObj:
                    abgInfo.write(excel_row, 0, abg.patient.basicInfo.name)
                    abgInfo.write(excel_row, 1, abg.patient.basicInfo.age)
                    abgInfo.write(excel_row, 2, abg.patient.basicInfo.sex)
                    abgInfo.write(excel_row, 3, abg.patient.patientID)
                    abgInfo.write(excel_row, 4, abg.ph)
                    abgInfo.write(excel_row, 5, abg.pc02)
                    abgInfo.write(excel_row, 6, abg.p02)
                    abgInfo.write(excel_row, 7, abg.na)
                    abgInfo.write(excel_row, 8, abg.k)
                    abgInfo.write(excel_row, 9, abg.ca1)
                    abgInfo.write(excel_row, 10, abg.glucose)
                    abgInfo.write(excel_row, 11, abg.lac)
                    abgInfo.write(excel_row, 12, abg.hc03)
                    abgInfo.write(excel_row, 13, abg.beecf)
                    abgInfo.write(excel_row, 14, abg.s02c)
                    abgInfo.write(excel_row, 15, abg.fi02)
                    abgInfo.write(excel_row, 16, abg.date.strftime("%Y-%m-%d, %H:%M:%S"))
                    abgInfo.write(excel_row, 17, abg.recorder)

                    excel_row += 1

            if serologyObj:
                serologyInfo = laboratoryPage.add_sheet(u"Serology")

                # 写入表头
                serologyInfo.write(0, 0, u'اسم المريض')
                serologyInfo.write(0, 1, u'العمر')
                serologyInfo.write(0, 2, u'الجنس')
                serologyInfo.write(0, 3, u'رقم المريض')
                serologyInfo.write(0, 4, u'HBS Ag')
                serologyInfo.write(0, 5, u'HIV')
                serologyInfo.write(0, 6, u'HCV')
                serologyInfo.write(0, 7, u'HCG')
                serologyInfo.write(0, 8, u'FOB')
                serologyInfo.write(0, 9, u'Widal O')
                serologyInfo.write(0, 10, u'Widal H')
                serologyInfo.write(0, 11, u'Wrigh A')
                serologyInfo.write(0, 12, u'Wrigh B')
                serologyInfo.write(0, 13, u'Date')
                serologyInfo.write(0, 14, u'Recorder')

                # 写入每一行对应的数据
                excel_row = 1

                for serology in serologyObj:
                    serologyInfo.write(excel_row, 0, serology.patient.basicInfo.name)
                    serologyInfo.write(excel_row, 1, serology.patient.basicInfo.age)
                    serologyInfo.write(excel_row, 2, serology.patient.basicInfo.sex)
                    serologyInfo.write(excel_row, 3, serology.patient.patientID)
                    serologyInfo.write(excel_row, 4, serology.hbs_Ag)
                    serologyInfo.write(excel_row, 5, serology.hiv)
                    serologyInfo.write(excel_row, 6, serology.hcv)
                    serologyInfo.write(excel_row, 7, serology.hcg)
                    serologyInfo.write(excel_row, 8, serology.fob)
                    serologyInfo.write(excel_row, 9, serology.widal_o)
                    serologyInfo.write(excel_row, 10, serology.widal_h)
                    serologyInfo.write(excel_row, 11, serology.wrigh_a)
                    serologyInfo.write(excel_row, 12, serology.wrigh_b)
                    serologyInfo.write(excel_row, 13, serology.date.strftime("%Y-%m-%d, %H:%M:%S"))
                    serologyInfo.write(excel_row, 14, serology.recorder)

                    excel_row += 1

            if urineAnalysisObj:
                urineAnalysisInfo = laboratoryPage.add_sheet(u"UrineAnalysis")

                # 写入表头
                urineAnalysisInfo.write(0, 0, u'اسم المريض')
                urineAnalysisInfo.write(0, 1, u'العمر')
                urineAnalysisInfo.write(0, 2, u'الجنس')
                urineAnalysisInfo.write(0, 3, u'رقم المريض')
                urineAnalysisInfo.write(0, 4, u'Color')
                urineAnalysisInfo.write(0, 5, u'SpGravity')
                urineAnalysisInfo.write(0, 6, u'Netrit')
                urineAnalysisInfo.write(0, 7, u'WBC')
                urineAnalysisInfo.write(0, 8, u'Urates')
                urineAnalysisInfo.write(0, 9, u'Uric Acid')
                urineAnalysisInfo.write(0, 10, u'Appearance')
                urineAnalysisInfo.write(0, 11, u'Glucose')
                urineAnalysisInfo.write(0, 12, u'Keton')
                urineAnalysisInfo.write(0, 13, u'RBC')
                urineAnalysisInfo.write(0, 14, u'Bacteria')
                urineAnalysisInfo.write(0, 15, u'Mucus')
                urineAnalysisInfo.write(0, 16, u'PH')
                urineAnalysisInfo.write(0, 17, u'Blood')
                urineAnalysisInfo.write(0, 18, u'Protein')
                urineAnalysisInfo.write(0, 19, u'EP.Cells')
                urineAnalysisInfo.write(0, 20, u'OX.Calcium')
                urineAnalysisInfo.write(0, 21, u'Casts')
                urineAnalysisInfo.write(0, 22, u'Fungi')
                urineAnalysisInfo.write(0, 23, u'Yeast')
                urineAnalysisInfo.write(0, 24, u'Pus Cell')
                urineAnalysisInfo.write(0, 25, u'Triple Phospate')
                urineAnalysisInfo.write(0, 26, u'Date')
                urineAnalysisInfo.write(0, 27, u'Recorder')

                # 写入每一行对应的数据
                excel_row = 1

                for urineAnalysis in urineAnalysisObj:
                    urineAnalysisInfo.write(excel_row, 0, urineAnalysis.patient.basicInfo.name)
                    urineAnalysisInfo.write(excel_row, 1, urineAnalysis.patient.basicInfo.age)
                    urineAnalysisInfo.write(excel_row, 2, urineAnalysis.patient.basicInfo.sex)
                    urineAnalysisInfo.write(excel_row, 3, urineAnalysis.patient.patientID)
                    urineAnalysisInfo.write(excel_row, 4, urineAnalysis.color)
                    urineAnalysisInfo.write(excel_row, 5, urineAnalysis.spGravity)
                    urineAnalysisInfo.write(excel_row, 6, urineAnalysis.netrit)
                    urineAnalysisInfo.write(excel_row, 7, urineAnalysis.wbc)
                    urineAnalysisInfo.write(excel_row, 8, urineAnalysis.urates)
                    urineAnalysisInfo.write(excel_row, 9, urineAnalysis.uric_acid)
                    urineAnalysisInfo.write(excel_row, 10, urineAnalysis.appearance)
                    urineAnalysisInfo.write(excel_row, 11, urineAnalysis.glucose)
                    urineAnalysisInfo.write(excel_row, 12, urineAnalysis.keton)
                    urineAnalysisInfo.write(excel_row, 13, urineAnalysis.rbc)
                    urineAnalysisInfo.write(excel_row, 14, urineAnalysis.bacteria)
                    urineAnalysisInfo.write(excel_row, 15, urineAnalysis.mucus)
                    urineAnalysisInfo.write(excel_row, 16, urineAnalysis.ph)
                    urineAnalysisInfo.write(excel_row, 17, urineAnalysis.blood)
                    urineAnalysisInfo.write(excel_row, 18, urineAnalysis.protein)
                    urineAnalysisInfo.write(excel_row, 19, urineAnalysis.epCells)
                    urineAnalysisInfo.write(excel_row, 20, urineAnalysis.ox_calcium)
                    urineAnalysisInfo.write(excel_row, 21, urineAnalysis.casts)
                    urineAnalysisInfo.write(excel_row, 22, urineAnalysis.fungi)
                    urineAnalysisInfo.write(excel_row, 23, urineAnalysis.yeast)
                    urineAnalysisInfo.write(excel_row, 24, urineAnalysis.pus_cell)
                    urineAnalysisInfo.write(excel_row, 25, urineAnalysis.triple_phospate)
                    urineAnalysisInfo.write(excel_row, 26, urineAnalysis.date.strftime("%Y-%m-%d, %H:%M:%S"))
                    urineAnalysisInfo.write(excel_row, 27, urineAnalysis.recorder)

                    excel_row += 1

            if csfObj:
                csfInfo = laboratoryPage.add_sheet(u"CSF")

                # 写入表头
                csfInfo.write(0, 0, u'اسم المريض')
                csfInfo.write(0, 1, u'العمر')
                csfInfo.write(0, 2, u'الجنس')
                csfInfo.write(0, 3, u'رقم المريض')
                csfInfo.write(0, 4, u'Color')
                csfInfo.write(0, 5, u'Appearance')
                csfInfo.write(0, 6, u'RBC')
                csfInfo.write(0, 7, u'WBC')
                csfInfo.write(0, 8, u'Glucose')
                csfInfo.write(0, 9, u'Protein')
                csfInfo.write(0, 10, u'Date')
                csfInfo.write(0, 11, u'Recorder')

                # 写入每一行对应的数据
                excel_row = 1

                for csf in csfObj:
                    csfInfo.write(excel_row, 0, csf.patient.basicInfo.name)
                    csfInfo.write(excel_row, 1, csf.patient.basicInfo.age)
                    csfInfo.write(excel_row, 2, csf.patient.basicInfo.sex)
                    csfInfo.write(excel_row, 3, csf.patient.patientID)
                    csfInfo.write(excel_row, 4, csf.color)
                    csfInfo.write(excel_row, 5, csf.appearance)
                    csfInfo.write(excel_row, 6, csf.rbc)
                    csfInfo.write(excel_row, 7, csf.wbc)
                    csfInfo.write(excel_row, 8, csf.glucose)
                    csfInfo.write(excel_row, 9, csf.protein)
                    csfInfo.write(excel_row, 10, csf.date.strftime("%Y-%m-%d, %H:%M:%S"))
                    csfInfo.write(excel_row, 11, csf.recorder)

                    excel_row += 1

            if antibioticsObj:

                # 添加第一页数据表
                antibioticsInfo = laboratoryPage.add_sheet(u"Antibiotics")

                # 写入表头
                antibioticsInfo.write(0, 0, u'اسم المريض')
                antibioticsInfo.write(0, 1, u'العمر')
                antibioticsInfo.write(0, 2, u'الجنس')
                antibioticsInfo.write(0, 3, u'رقم المريض')
                antibioticsInfo.write(0, 4, u'Cephradine')
                antibioticsInfo.write(0, 5, u'Ciprofloxacin')
                antibioticsInfo.write(0, 6, u'Gentamicin')
                antibioticsInfo.write(0, 7, u'Nitrofurantoin')
                antibioticsInfo.write(0, 8, u'Ofloxacin')
                antibioticsInfo.write(0, 9, u'Cefoxitin')
                antibioticsInfo.write(0, 10, u'Cefaclor')
                antibioticsInfo.write(0, 11, u'Amikacin')
                antibioticsInfo.write(0, 12, u'Ceftriaxone')
                antibioticsInfo.write(0, 13, u'Amoxicillin Clavulanic Acid')
                antibioticsInfo.write(0, 14, u'Cefadroxil')
                antibioticsInfo.write(0, 15, u'Cefixime')
                antibioticsInfo.write(0, 16, u'Cefotaxime')
                antibioticsInfo.write(0, 17, u'Cefuroxime')
                antibioticsInfo.write(0, 18, u'Imipenem')
                antibioticsInfo.write(0, 19, u'Ampicillin Sulbactam')
                antibioticsInfo.write(0, 20, u'Amoxicillin')
                antibioticsInfo.write(0, 21, u'Azithromycin')
                antibioticsInfo.write(0, 22, u'Levofloxacin')
                antibioticsInfo.write(0, 23, u'Neomycin')
                antibioticsInfo.write(0, 24, u'Doxycycline')
                antibioticsInfo.write(0, 25, u'pipemidic Acid')
                antibioticsInfo.write(0, 26, u'Meropenem')
                antibioticsInfo.write(0, 27, u'Cloxacillin')
                antibioticsInfo.write(0, 28, u'Trimethoprim Sulphamethoxazole')
                antibioticsInfo.write(0, 29, u'Norfloxacin')
                antibioticsInfo.write(0, 30, u'Date')
                antibioticsInfo.write(0, 31, u'Recorder')

                # 写入每一行对应的数据
                excel_row = 1

                for antibiotics in antibioticsObj:
                    antibioticsInfo.write(excel_row, 0, antibiotics.patient.basicInfo.name)
                    antibioticsInfo.write(excel_row, 1, antibiotics.patient.basicInfo.age)
                    antibioticsInfo.write(excel_row, 2, antibiotics.patient.basicInfo.sex)
                    antibioticsInfo.write(excel_row, 3, antibiotics.patient.patientID)
                    antibioticsInfo.write(excel_row, 4, antibiotics.cephradine)
                    antibioticsInfo.write(excel_row, 5, antibiotics.ciprofloxacin)
                    antibioticsInfo.write(excel_row, 6, antibiotics.gentamicin)
                    antibioticsInfo.write(excel_row, 7, antibiotics.nitrofurantoin)
                    antibioticsInfo.write(excel_row, 8, antibiotics.ofloxacin)
                    antibioticsInfo.write(excel_row, 9, antibiotics.cefoxitin)
                    antibioticsInfo.write(excel_row, 10, antibiotics.cefaclor)
                    antibioticsInfo.write(excel_row, 11, antibiotics.amikacin)
                    antibioticsInfo.write(excel_row, 12, antibiotics.ceftriaxone)
                    antibioticsInfo.write(excel_row, 13, antibiotics.amoxicillin_clavulanic_acid)
                    antibioticsInfo.write(excel_row, 14, antibiotics.cefadroxil)
                    antibioticsInfo.write(excel_row, 15, antibiotics.cefixime)
                    antibioticsInfo.write(excel_row, 16, antibiotics.cefotaxime)
                    antibioticsInfo.write(excel_row, 17, antibiotics.cefuroxime)
                    antibioticsInfo.write(excel_row, 18, antibiotics.imipenem)
                    antibioticsInfo.write(excel_row, 19, antibiotics.ampicillin_sulbactam)
                    antibioticsInfo.write(excel_row, 20, antibiotics.amoxicillin)
                    antibioticsInfo.write(excel_row, 21, antibiotics.azithromycin)
                    antibioticsInfo.write(excel_row, 22, antibiotics.levofloxacin)
                    antibioticsInfo.write(excel_row, 23, antibiotics.neomycin)
                    antibioticsInfo.write(excel_row, 24, antibiotics.doxycycline)
                    antibioticsInfo.write(excel_row, 25, antibiotics.pipemidic_acid)
                    antibioticsInfo.write(excel_row, 26, antibiotics.meropenem)
                    antibioticsInfo.write(excel_row, 27, antibiotics.cloxacillin)
                    antibioticsInfo.write(excel_row, 28, antibiotics.trimethoprim_sulphamethoxazole)
                    antibioticsInfo.write(excel_row, 29, antibiotics.norfloxacin)
                    antibioticsInfo.write(excel_row, 30, antibiotics.date.strftime("%Y-%m-%d, %H:%M:%S"))
                    antibioticsInfo.write(excel_row, 31, antibiotics.recorder)

                    excel_row += 1

            if hormonesObj:

                # 添加第一页数据表
                hormonesInfo = laboratoryPage.add_sheet(u"Hormones")

                # 写入表头
                hormonesInfo.write(0, 0, u'اسم المريض')
                hormonesInfo.write(0, 1, u'العمر')
                hormonesInfo.write(0, 2, u'الجنس')
                hormonesInfo.write(0, 3, u'رقم المريض')
                hormonesInfo.write(0, 4, u'Hba1c')
                hormonesInfo.write(0, 5, u'Tsh')
                hormonesInfo.write(0, 6, u'Ft4')
                hormonesInfo.write(0, 7, u'T4')
                hormonesInfo.write(0, 8, u'T3')
                hormonesInfo.write(0, 9, u'Lh')
                hormonesInfo.write(0, 10, u'Fsh')
                hormonesInfo.write(0, 11, u'Prolactin')
                hormonesInfo.write(0, 12, u'Testosterone')
                hormonesInfo.write(0, 13, u'Cortisol')
                hormonesInfo.write(0, 14, u'Vit D')
                hormonesInfo.write(0, 15, u'Ferritin')
                hormonesInfo.write(0, 16, u'D Dimer')
                hormonesInfo.write(0, 17, u'B Hcg')
                hormonesInfo.write(0, 18, u'Troponin I')
                hormonesInfo.write(0, 19, u'Troponin T')
                hormonesInfo.write(0, 20, u'Amh')
                hormonesInfo.write(0, 21, u'Psa')
                hormonesInfo.write(0, 22, u'Cea')
                hormonesInfo.write(0, 23, u'Afp')
                hormonesInfo.write(0, 24, u'Toxo_igg_igm')
                hormonesInfo.write(0, 25, u'Date')
                hormonesInfo.write(0, 26, u'Recorder')

                # 写入每一行对应的数据
                excel_row = 1

                for hormones in hormonesObj:
                    hormonesInfo.write(excel_row, 0, hormones.patient.basicInfo.name)
                    hormonesInfo.write(excel_row, 1, hormones.patient.basicInfo.age)
                    hormonesInfo.write(excel_row, 2, hormones.patient.basicInfo.sex)
                    hormonesInfo.write(excel_row, 3, hormones.patient.patientID)
                    hormonesInfo.write(excel_row, 4, hormones.hba1c)
                    hormonesInfo.write(excel_row, 5, hormones.tsh)
                    hormonesInfo.write(excel_row, 6, hormones.ft4)
                    hormonesInfo.write(excel_row, 7, hormones.t4)
                    hormonesInfo.write(excel_row, 8, hormones.t3)
                    hormonesInfo.write(excel_row, 9, hormones.lh)
                    hormonesInfo.write(excel_row, 10, hormones.fsh)
                    hormonesInfo.write(excel_row, 11, hormones.prolactin)
                    hormonesInfo.write(excel_row, 12, hormones.testosterone)
                    hormonesInfo.write(excel_row, 13, hormones.cortisol)
                    hormonesInfo.write(excel_row, 14, hormones.vit_d)
                    hormonesInfo.write(excel_row, 15, hormones.ferritin)
                    hormonesInfo.write(excel_row, 16, hormones.d_dimer)
                    hormonesInfo.write(excel_row, 17, hormones.b_hcg)
                    hormonesInfo.write(excel_row, 18, hormones.troponin_i)
                    hormonesInfo.write(excel_row, 19, hormones.troponin_t)
                    hormonesInfo.write(excel_row, 20, hormones.amh)
                    hormonesInfo.write(excel_row, 21, hormones.psa)
                    hormonesInfo.write(excel_row, 22, hormones.cea)
                    hormonesInfo.write(excel_row, 23, hormones.afp)
                    hormonesInfo.write(excel_row, 24, hormones.toxo_igg_igm)
                    hormonesInfo.write(excel_row, 25, hormones.date.strftime("%Y-%m-%d, %H:%M:%S"))
                    hormonesInfo.write(excel_row, 26, hormones.recorder)

                    excel_row += 1

                # 实现下载
                output = BytesIO()
                laboratoryPage.save(output)
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

        else:
            return HttpResponse('There are no data !')
