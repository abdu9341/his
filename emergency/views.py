from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect
from user.views import login_required
from patient.models import *
from user.models import User
from patient.function import *
from django.urls import reverse
from laboratory.models import *
from discharge.models import Discharge
from datetime import datetime


@login_required
def indexEmergency(request):

    user = User.objects.all().get(name=request.session['name'])

    # 更新当前模板内容
    user.currentTemplateUrl = 'indexEmergency'
    user.save()

    # 急诊科病人
    emergencyMalePatients = PatientInfo.objects.filter(condition=2, basicInfo__sex='ذكر')
    emergencyFemalePatients = PatientInfo.objects.filter(condition=2, basicInfo__sex='انثى')

    # 急诊科病人数量
    countOfMale = emergencyMalePatients.count()
    countOfFemale = emergencyFemalePatients.count()

    return render(request, 'emergency/indexEmergency.html', locals())


@login_required
def emergencyPatientList(request, pindex):
    """病人基本信息"""

    username = request.session['name']
    user = User.objects.all().get(name=username)

    patients = PatientInfo.objects.filter(condition=2).order_by('-id')

    # 急诊科病人
    emergencyMalePatients = PatientInfo.objects.filter(condition=2, basicInfo__sex='ذكر')
    emergencyFemalePatients = PatientInfo.objects.filter(condition=2, basicInfo__sex='انثى')

    # 急诊科病人数量
    countOfMale = emergencyMalePatients.count()
    countOfFemale = emergencyFemalePatients.count()

    # 分页显示
    paginator = Paginator(patients, 20)
    if pindex == '':
        pindex = 1
    else:
        pindex = int(pindex)
    page = paginator.page(pindex)

    return render(request, 'emergency/emergencyPatientList.html', locals())


@login_required
def searchEmergencyPatient(request):

    user = User.objects.all().get(name=request.session['name'])

    # 急诊科病人
    emergencyMalePatients = PatientInfo.objects.filter(condition=2, basicInfo__sex='ذكر')
    emergencyFemalePatients = PatientInfo.objects.filter(condition=2, basicInfo__sex='انثى')

    # 急诊科病人数量
    countOfMale = emergencyMalePatients.count()
    countOfFemale = emergencyFemalePatients.count()

    message = ''

    if request.method == 'POST':

        search = request.POST.get('search')

        page = PatientInfo.objects.filter(Q(basicInfo__name__contains=search)
                                          | Q(patientID=search))

        if page:
            pass

        else:
            message = 'Not Found !'

    return render(request, 'emergency/emergencyPatientList.html', locals())


@login_required
def newEmergencyPatient(request):
    """添加病人基本信息"""

    # 获取当前需要的数据
    genders = ['', 'ذكر', 'انثى']

    user = User.objects.get(name=request.session['name'])
    departments = Department.objects.filter(status=True)
    sickroom = Ward.objects.get(name='Emergency Room')

    # 急诊科病人
    emergencyMalePatients = PatientInfo.objects.filter(condition=2, basicInfo__sex='ذكر')
    emergencyFemalePatients = PatientInfo.objects.filter(condition=2, basicInfo__sex='انثى')

    # 急诊科病人数量
    countOfMale = emergencyMalePatients.count()
    countOfFemale = emergencyFemalePatients.count()

    message = ''

    if request.method == 'POST':
        name = request.POST.get('name').title()
        age = request.POST.get('age')
        sex = request.POST.get('sex')
        types = request.POST.get('types')

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
            return render(request, 'emergency/newEmergencyPatient.html', locals())
        else:
            numberID = IDCreator()

            basicInfo = BasicInfo.objects.create(name=name, birthday=birthday, sex=sex,
                                                 age=tempAge, operator=user.name)

            patient = PatientInfo.objects.create(basicInfo=basicInfo, patientID=numberID, condition=2,
                                                 sickroom_id=sickroom.id, operator=user.arabic_name,
                                                 typeOfEmergency=types)
            # 增加病房病人数量
            sickroom.count += 1
            sickroom.save()

            # 病人所在的科室
            department_ids = request.POST.getlist('department')
            department_list = []
            for department_id in department_ids:
                department_list.append(Department.objects.get(id=department_id))
            patient.department.add(*department_list)

            url = reverse('emergencyPatientInfo', args=(patient.id, patient.patientID))
            return redirect(url)

    return render(request, 'emergency/newEmergencyPatient.html', locals())


@login_required
def emergencyPatientInfo(request, patient_id, patient_num):
    """查看病人基本信息"""

    username = request.session['name']
    user = User.objects.all().get(name=username)

    rights = False
    if user.authorityDepartment.name == 'Emergency':
        rights = True
    elif user.position.name == 'Manager':
        rights = True

    patient = PatientInfo.objects.get(id=patient_id)

    # 急诊科病人
    emergencyMalePatients = PatientInfo.objects.filter(condition=2, basicInfo__sex='ذكر')
    emergencyFemalePatients = PatientInfo.objects.filter(condition=2, basicInfo__sex='انثى')

    # 急诊科病人数量
    countOfMale = emergencyMalePatients.count()
    countOfFemale = emergencyFemalePatients.count()

    # departments = DepartmentPatient.objects.filter(patient_id=patient_id)

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

    return render(request, 'emergency/emergencyPatientInfo.html', locals())


@login_required
def editEmergencyPatientInfo(request, patient_id, patient_num):
    """编辑基本信息"""

    # 获取当前需要编辑数据
    genders = ['', 'ذكر', 'انثى']

    patient = PatientInfo.objects.get(id=patient_id)
    user = User.objects.get(name=request.session['name'])

    # 急诊科病人
    emergencyMalePatients = PatientInfo.objects.filter(condition=2, basicInfo__sex='ذكر')
    emergencyFemalePatients = PatientInfo.objects.filter(condition=2, basicInfo__sex='انثى')

    # 急诊科病人数量
    countOfMale = emergencyMalePatients.count()
    countOfFemale = emergencyFemalePatients.count()

    departments = Department.objects.filter(status=True)
    # patientDepartments = DepartmentPatient.objects.filter(patient_id=patient_id)
    sickroom = Ward.objects.get(name='Emergency Room')

    message = ''

    if request.method == 'POST':

        # 获取前台传递过来的数据
        name = request.POST.get('name').title()
        age = request.POST.get('age')
        sex = request.POST.get('sex')
        types = request.POST.get('types')

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
            message = 'المريض موجود '
            return render(request, 'emergency/editEmergencyPatientInfo.html', locals())

        else:
            # 对表中已存在数据进行修改
            patient.basicInfo.name = name
            patient.basicInfo.age = tempAge
            patient.basicInfo.birthday = birthday
            patient.basicInfo.sex = sex
            patient.sickroom_id = sickroom.id
            patient.typeOfEmergency = types
            patient.condition = 2
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

            url = reverse('emergencyPatientInfo', args=(patient.id, patient.patientID))
            return redirect(url)

    if patient.condition:

        return render(request, 'emergency/editEmergencyPatientInfo.html', locals())

    else:
        return HttpResponse('This Patient already discharged, you can\'t edit !')


@login_required
def reenterEmergencyPatient(request, patient_id, patient_num):
    """返回病人"""

    user = User.objects.all().get(name=request.session['name'])

    # 急诊科病人
    emergencyMalePatients = PatientInfo.objects.filter(condition=2, basicInfo__sex='ذكر')
    emergencyFemalePatients = PatientInfo.objects.filter(condition=2, basicInfo__sex='انثى')

    # 急诊科病人数量
    countOfMale = emergencyMalePatients.count()
    countOfFemale = emergencyFemalePatients.count()

    patient = PatientInfo.objects.get(id=patient_id)
    message = ''
    patientInfos = PatientInfo.objects.filter(basicInfo=patient.basicInfo)

    for patientInfo in patientInfos:
        if patientInfo.condition == 0 or patientInfo.condition == 8:
            pass

        else:
            message = 'المريض موجود '

            return HttpResponse(message)

    departments = Department.objects.filter(status=True).order_by('name')
    ward = Ward.objects.get(name='Emergency Room')

    if request.method == 'POST':

        # 要住院的病人更新的信息
        types = request.POST.get('types')
        department_ids = request.POST.getlist('department')

        newPatientInfo = PatientInfo.objects.create(basicInfo=patient.basicInfo, typeOfEmergency=types,
                                                    sickroom_id=ward.id, condition=2,
                                                    patientID=patient.patientID, operator=user.arabic_name)
        # 增加病房病人数量
        ward.count += 1
        ward.save()

        # 记录这次的住院科室
        department_list = []
        for department_id in department_ids:
            department_list.append(Department.objects.get(id=department_id))
        newPatientInfo.department.add(*department_list)

        url = reverse('emergencyPatientInfo', args=(newPatientInfo.id, patient.patientID))
        return redirect(url)

    return render(request, 'emergency/reenterEmergencyPatient.html', locals())


@login_required
def emergencyPatientLaboratory(request, patient_id, patient_num):

    # 当前需要的信息
    user = User.objects.get(name=request.session['name'])

    patient = PatientInfo.objects.all().get(id=patient_id)

    # 急诊科病人
    emergencyMalePatients = PatientInfo.objects.filter(condition=2, basicInfo__sex='ذكر')
    emergencyFemalePatients = PatientInfo.objects.filter(condition=2, basicInfo__sex='انثى')

    # 急诊科病人数量
    countOfMale = emergencyMalePatients.count()
    countOfFemale = emergencyFemalePatients.count()

    cbcs = CBC.objects.filter(patient_id=patient_id).order_by('-date')
    for cbc in cbcs:
        if cbc.rbc:
            rbc_cbc = cbc.rbc
        if cbc.mcv:
            mcv = cbc.mcv
        if cbc.mch:
            mch = cbc.mch
        if cbc.mchc:
            mchc = cbc.mchc
        if cbc.rdw:
            rdw = cbc.rdw
        if cbc.bloodGroup:
            bloodGroup = cbc.bloodGroup
        if cbc.hemoglobin:
            hemoglobin = cbc.hemoglobin
        if cbc.hematocrite:
            hematocrite = cbc.hematocrite
        if cbc.wbc:
            wbc_cbc = cbc.wbc
        if cbc.gran:
            gran = cbc.gran
        if cbc.lym:
            lym = cbc.lym
        if cbc.mid:
            mid = cbc.mid
        if cbc.plt:
            plt = cbc.plt
        if cbc.esrH1:
            esrH1 = cbc.esrH1
        if cbc.esrH2:
            esrH2 = cbc.esrH2

    coagulations = Coagulation.objects.filter(patient_id=patient_id).order_by('-date')
    for coagulation in coagulations:
        if coagulation.pt:
            pt = coagulation.pt
        if coagulation.inr:
            inr = coagulation.inr
        if coagulation.aptt:
            aptt = coagulation.aptt
        if coagulation.bleedTime:
            bleedTime = coagulation.bleedTime
        if coagulation.clotTime:
            clotTime = coagulation.clotTime
        if coagulation.act:
            act = coagulation.act

    biochemistrys = Biochemistry.objects.filter(patient_id=patient_id).order_by('-date')
    for biochemistry in biochemistrys:
        if biochemistry.glucose:
            glucose_bio = biochemistry.glucose
        if biochemistry.urea:
            urea = biochemistry.urea
        if biochemistry.creatine:
            creatine_bio = biochemistry.creatine
        if biochemistry.sgpt:
            sgpt = biochemistry.sgpt
        if biochemistry.sgot:
            sgot = biochemistry.sgot
        if biochemistry.biliTotal:
            biliTotal = biochemistry.biliTotal
        if biochemistry.biliDirect:
            biliDirect = biochemistry.biliDirect
        if biochemistry.biliIndirect:
            biliIndirect = biochemistry.biliIndirect
        if biochemistry.alp:
            alp = biochemistry.alp
        if biochemistry.amylase:
            amylase = biochemistry.amylase
        if biochemistry.ldh:
            ldh = biochemistry.ldh
        if biochemistry.albumin:
            albumin = biochemistry.albumin
        if biochemistry.totalProtein:
            totalProtein = biochemistry.totalProtein
        if biochemistry.ck:
            ck = biochemistry.ck
        if biochemistry.ck_mb:
            ck_mb = biochemistry.ck_mb
        if biochemistry.lipase:
            lipase = biochemistry.lipase
        if biochemistry.uric_acid:
            uric_acid = biochemistry.uric_acid
        if biochemistry.triglycerid:
            triglycerid = biochemistry.triglycerid
        if biochemistry.cholesterol:
            cholesterol = biochemistry.cholesterol
        if biochemistry.crp:
            crp = biochemistry.crp
        if biochemistry.aslo:
            aslo = biochemistry.aslo
        if biochemistry.rf:
            rf = biochemistry.rf

    electrolytess = Electrolytes.objects.filter(patient_id=patient_id).order_by('-date')
    for electrolytes in electrolytess:
        if electrolytes.na:
            na_elec = electrolytes.na
        if electrolytes.k:
            k_elec = electrolytes.k
        if electrolytes.cl:
            cl = electrolytes.cl
        if electrolytes.tca:
            tca = electrolytes.tca
        if electrolytes.nca:
            nca = electrolytes.nca
        if electrolytes.ica:
            ica = electrolytes.ica
        if electrolytes.iron:
            iron = electrolytes.iron
        if electrolytes.mg:
            mg = electrolytes.mg
        if electrolytes.phosphorus:
            phosphorus = electrolytes.phosphorus

    abgs = ABG.objects.filter(patient_id=patient_id).order_by('-date')
    for abg in abgs:
        if abg.ph:
            ph_abg = abg.ph
        if abg.pc02:
            pc02 = abg.pc02
        if abg.p02:
            p02 = abg.p02
        if abg.na:
            na_abg = abg.na
        if abg.k:
            k_abg = abg.k
        if abg.ca1:
            ca1 = abg.ca1
        if abg.glucose:
            glucose_abg = abg.glucose
        if abg.lac:
            lac = abg.lac
        if abg.hc03:
            hc03 = abg.hc03
        if abg.beecf:
            beecf = abg.beecf
        if abg.s02c:
            s02c = abg.s02c
        if abg.fi02:
            fi02 = abg.fi02

    serologys = Serology.objects.filter(patient_id=patient_id).order_by('-date')
    for serology in serologys:

        if serology.hbs_Ag:
            hbs_Ag = serology.hbs_Ag
        if serology.hiv:
            hiv = serology.hiv
        if serology.hcv:
            hcv = serology.hcv
        if serology.hcg:
            hcg = serology.hcg
        if serology.fob:
            fob = serology.fob
        if serology.widal_o:
            widal_o = serology.widal_o
        if serology.widal_h:
            widal_h = serology.widal_h
        if serology.wrigh_a:
            wrigh_a = serology.wrigh_a
        if serology.wrigh_b:
            wrigh_b = serology.wrigh_b

    urineAnalysiss = UrineAnalysis.objects.filter(patient_id=patient_id).order_by('-date')
    for urineAnalysis in urineAnalysiss:
        if urineAnalysis.color:
            color = urineAnalysis.color
        if urineAnalysis.spGravity:
            spGravity = urineAnalysis.spGravity
        if urineAnalysis.netrit:
            netrit = urineAnalysis.netrit
        if urineAnalysis.wbc:
            wbc_urine = urineAnalysis.wbc
        if urineAnalysis.urates:
            urates = urineAnalysis.urates
        if urineAnalysis.uric_acid:
            uric_acid = urineAnalysis.uric_acid
        if urineAnalysis.appearance:
            appearance = urineAnalysis.appearance
        if urineAnalysis.glucose:
            glucose = urineAnalysis.glucose
        if urineAnalysis.keton:
            keton = urineAnalysis.keton
        if urineAnalysis.rbc:
            rbc = urineAnalysis.rbc
        if urineAnalysis.bacteria:
            bacteria = urineAnalysis.bacteria
        if urineAnalysis.mucus:
            mucus = urineAnalysis.mucus
        if urineAnalysis.ph:
            ph = urineAnalysis.ph
        if urineAnalysis.blood:
            blood = urineAnalysis.blood
        if urineAnalysis.protein:
            protein = urineAnalysis.protein
        if urineAnalysis.epCells:
            epCells = urineAnalysis.epCells
        if urineAnalysis.ox_calcium:
            ox_calcium = urineAnalysis.ox_calcium
        if urineAnalysis.casts:
            casts = urineAnalysis.casts
        if urineAnalysis.fungi:
            fungi = urineAnalysis.fungi
        if urineAnalysis.yeast:
            yeast = urineAnalysis.yeast
        if urineAnalysis.pus_cell:
            pus_cell = urineAnalysis.pus_cell
        if urineAnalysis.triple_phospate:
            triple_phospate = urineAnalysis.triple_phospate

    csfs = CSF.objects.filter(patient_id=patient_id).order_by('-date')
    for csf in csfs:
        if csf.color:
            color_csf = csf.color
        if csf.appearance:
            appearance = csf.appearance
        if csf.rbc:
            rbc_csf = csf.rbc
        if csf.wbc:
            wbc_csf = csf.wbc
        if csf.glucose:
            glucose_csf = csf.glucose
        if csf.protein:
            protien_csf = csf.protein

    antibiotics = Antibiotics.objects.filter(patient_id=patient_id).order_by('-date')
    for antibiotic in antibiotics:
        if antibiotic.cephradine:
            cephradine = antibiotic.cephradine
        if antibiotic.ciprofloxacin:
            ciprofloxacin = antibiotic.ciprofloxacin
        if antibiotic.gentamicin:
            gentamicin = antibiotic.gentamicin
        if antibiotic.nitrofurantoin:
            nitrofurantoin = antibiotic.nitrofurantoin
        if antibiotic.ofloxacin:
            ofloxacin = antibiotic.ofloxacin
        if antibiotic.cefoxitin:
            cefoxitin = antibiotic.cefoxitin
        if antibiotic.cefaclor:
            cefaclor = antibiotic.cefaclor
        if antibiotic.amikacin:
            amikacin = antibiotic.amikacin
        if antibiotic.ceftriaxone:
            ceftriaxone = antibiotic.ceftriaxone
        if antibiotic.amoxicillin_clavulanic_acid:
            amoxicillin_clavulanic_acid = antibiotic.amoxicillin_clavulanic_acid
        if antibiotic.cefadroxil:
            cefadroxil = antibiotic.cefadroxil
        if antibiotic.cefixime:
            cefixime = antibiotic.cefixime
        if antibiotic.cefotaxime:
            cefotaxime = antibiotic.cefotaxime
        if antibiotic.cefuroxime:
            cefuroxime = antibiotic.cefuroxime
        if antibiotic.imipenem:
            imipenem = antibiotic.imipenem
        if antibiotic.ampicillin_sulbactam:
            ampicillin_sulbactam = antibiotic.ampicillin_sulbactam
        if antibiotic.amoxicillin:
            amoxicillin = antibiotic.amoxicillin
        if antibiotic.azithromycin:
            azithromycin = antibiotic.azithromycin
        if antibiotic.levofloxacin:
            levofloxacin = antibiotic.levofloxacin
        if antibiotic.neomycin:
            neomycin = antibiotic.neomycin
        if antibiotic.doxycycline:
            doxycycline = antibiotic.doxycycline
        if antibiotic.pipemidic_acid:
            pipemidic_acid = antibiotic.pipemidic_acid
        if antibiotic.meropenem:
            meropenem = antibiotic.meropenem
        if antibiotic.cloxacillin:
            cloxacillin = antibiotic.cloxacillin
        if antibiotic.trimethoprim_sulphamethoxazole:
            trimethoprim_sulphamethoxazole = antibiotic.trimethoprim_sulphamethoxazole
        if antibiotic.norfloxacin:
            norfloxacin = antibiotic.norfloxacin

    hormones = Hormones.objects.filter(patient_id=patient_id).order_by('-date')
    for hormone in hormones:
        if hormone.hba1c:
            hba1c = hormone.hba1c
        if hormone.tsh:
            tsh = hormone.tsh
        if hormone.ft4:
            ft4 = hormone.ft4
        if hormone.t4:
            t4 = hormone.t4
        if hormone.t3:
            t3 = hormone.t3
        if hormone.lh:
            lh = hormone.lh
        if hormone.fsh:
            fsh = hormone.fsh
        if hormone.prolactin:
            prolactin = hormone.prolactin
        if hormone.testosterone:
            testosterone = hormone.testosterone
        if hormone.cortisol:
            cortisol = hormone.cortisol
        if hormone.vit_d:
            vit_d = hormone.vit_d
        if hormone.ferritin:
            ferritin = hormone.ferritin
        if hormone.d_dimer:
            d_dimer = hormone.d_dimer
        if hormone.b_hcg:
            b_hcg = hormone.b_hcg
        if hormone.troponin_i:
            troponin_i = hormone.troponin_i
        if hormone.troponin_t:
            troponin_t = hormone.troponin_t
        if hormone.amh:
            amh = hormone.amh
        if hormone.psa:
            psa = hormone.psa
        if hormone.cea:
            cea = hormone.cea
        if hormone.afp:
            afp = hormone.afp
        if hormone.toxo_igg_igm:
            toxo_igg_igm = hormone.toxo_igg_igm

    return render(request, 'emergency/emergencyPatientLaboratory.html', locals())


@login_required
def emergencyPatientTransfer(request, patient_id, patient_num):
    """转科"""

    patient = PatientInfo.objects.get(id=patient_id)
    user = User.objects.all().get(name=request.session['name'])

    # departmentObj = DepartmentPatient.objects.filter(patient_id=patient_id)

    departments = Department.objects.filter(status=True)

    emergencyRoom = Ward.objects.get(name='Emergency Room')

    # 急诊科病人
    emergencyMalePatients = PatientInfo.objects.filter(condition=2, basicInfo__sex='ذكر')
    emergencyFemalePatients = PatientInfo.objects.filter(condition=2, basicInfo__sex='انثى')

    # 急诊科病人数量
    countOfMale = emergencyMalePatients.count()
    countOfFemale = emergencyFemalePatients.count()

    wards = Ward.objects.filter(status=True)
    message = ''

    if request.method == 'POST':
        transferSickroom_id = request.POST.get('sickroom')
        date = datetime.now()

        # department_ids = request.POST.getlist('department')

        patient.sickroom_id = transferSickroom_id
        patient.transferDate = date
        patient.condition = 1
        patient.save()

        message = 'Successful transfer !'

        sickroomObj = Ward.objects.get(id=transferSickroom_id)

        # 更新病房病人数量
        emergencyRoom.count -= 1
        emergencyRoom.save()

        sickroomObj.count += 1
        sickroomObj.save()

        url = reverse('emergencyPatientInfo', args=(patient_id, patient_num))

        return redirect(url)

    if patient.condition:

        return render(request, 'emergency/emergencyPatientTransfer.html', locals())

    else:
        return HttpResponse('This Patient already discharged, you can\'t transfer !')


@login_required
def emergencyPatientDischarge(request, patient_id, patient_num):
    """执行出院"""

    # 用户信息
    user = User.objects.all().get(name=request.session['name'])

    # 病人基本信息
    patient = PatientInfo.objects.all().get(id=patient_id)

    # 急诊科病人
    emergencyMalePatients = PatientInfo.objects.filter(condition=2, basicInfo__sex='ذكر')
    emergencyFemalePatients = PatientInfo.objects.filter(condition=2, basicInfo__sex='انثى')

    # 急诊科病人数量
    countOfMale = emergencyMalePatients.count()
    countOfFemale = emergencyFemalePatients.count()

    # 获取前端数据
    if request.method == 'POST':
        leaveDate = datetime.now()
        dischargeStatus = request.POST.get('discharge')

        Discharge.objects.create(leaveDate=leaveDate, dischargeStatus=dischargeStatus,
                                 patient_id=patient_id, operator=user.name,
                                 leavingDepartment="اسعاف")
        #  更新在院状态
        patient.condition = 3
        patient.save()

        # 更新病房病人数量
        emergencyRoom = Ward.objects.get(name='Emergency Room')
        emergencyRoom.count -= 1
        emergencyRoom.save()

        return redirect('/indexEmergency/')

    if patient.condition:

        return render(request, 'emergency/emergencyPatientDischarge.html', locals())

    else:
        return HttpResponse('This patient already discharged !')
