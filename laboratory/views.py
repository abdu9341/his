from django.shortcuts import render, redirect, HttpResponse
from django.urls import reverse
from department.models import Ward
from laboratory.models import *
from patient.function import IDCreator
from patient.models import BasicInfo, PatientInfo
from user.views import login_required
from django.db.models import Q, Sum
from user.models import User
from datetime import datetime
import time


@login_required
def indexLaboratory(request):

    user = User.objects.all().get(name=request.session['name'])

    # 更新当前模板内容
    user.currentTemplateUrl = 'indexLaboratory'
    user.save()

    # 病房
    wards = user.authorityWard.filter(status=True)

    return render(request, 'laboratory/indexLaboratory.html', locals())


@login_required
def allLaboratoryResults(request, patient_id, patient_num):

    # 当前需要的信息
    user = User.objects.get(name=request.session['name'])

    patient = PatientInfo.objects.all().get(id=patient_id)

    # 统计病房病人
    wards = user.authorityWard.filter(status=True)
    countOfTotal = wards.aggregate(Sum('count'))['count__sum']

    # 该用户能访问的病人
    patientsDoctor = PatientInfo.objects.filter(condition=1, department=user.authorityDepartment)
    patientsNurse = PatientInfo.objects.filter(condition=1, sickroom__in=user.authorityWard.all())

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

    return render(request, 'laboratory/allLaboratoryResults.html', locals())


@login_required
def graphicLaboratory(request, patient_id, big_item, small_item):
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

    date = []
    result = []

    if big_item == 'CBC':

        cbcObj = CBC.objects.filter(patient_id=patient_id, status=True).order_by('-date')
        for cbc in cbcObj:
            if small_item == 'RBC':
                if cbc.rbc:
                    this_date = datetime.strptime(str(cbc.date), '%Y-%m-%d %H:%M:%S.%f')
                    this_date = time.mktime(this_date.timetuple())
                    date.append(this_date * 1000 + 10800000)
                    result.append(float(cbc.rbc))
            elif small_item == 'MCV':
                if cbc.mcv:
                    this_date = datetime.strptime(str(cbc.date), '%Y-%m-%d %H:%M:%S.%f')
                    this_date = time.mktime(this_date.timetuple())
                    date.append(this_date * 1000 + 10800000)
                    result.append(float(cbc.mcv))
            elif small_item == 'MCH':
                if cbc.mch:
                    this_date = datetime.strptime(str(cbc.date), '%Y-%m-%d %H:%M:%S.%f')
                    this_date = time.mktime(this_date.timetuple())
                    date.append(this_date * 1000 + 10800000)
                    result.append(float(cbc.mch))
            elif small_item == 'MCHC':
                if cbc.mchc:
                    this_date = datetime.strptime(str(cbc.date), '%Y-%m-%d %H:%M:%S.%f')
                    this_date = time.mktime(this_date.timetuple())
                    date.append(this_date * 1000 + 10800000)
                    result.append(float(cbc.mchc))
            elif small_item == 'RDW':
                if cbc.rdw:
                    this_date = datetime.strptime(str(cbc.date), '%Y-%m-%d %H:%M:%S.%f')
                    this_date = time.mktime(this_date.timetuple())
                    date.append(this_date * 1000 + 10800000)
                    result.append(float(cbc.rdw))
            elif small_item == 'Hemoglobin':
                if cbc.hemoglobin:
                    this_date = datetime.strptime(str(cbc.date), '%Y-%m-%d %H:%M:%S.%f')
                    this_date = time.mktime(this_date.timetuple())
                    date.append(this_date * 1000 + 10800000)
                    result.append(float(cbc.hemoglobin))
            elif small_item == 'Hematocrite':
                if cbc.hematocrite:
                    this_date = datetime.strptime(str(cbc.date), '%Y-%m-%d %H:%M:%S.%f')
                    this_date = time.mktime(this_date.timetuple())
                    date.append(this_date * 1000 + 10800000)
                    result.append(float(cbc.hematocrite))
            elif small_item == 'GRAN':
                if cbc.gran:
                    this_date = datetime.strptime(str(cbc.date), '%Y-%m-%d %H:%M:%S.%f')
                    this_date = time.mktime(this_date.timetuple())
                    date.append(this_date * 1000 + 10800000)
                    result.append(float(cbc.gran))
            elif small_item == 'LYM':
                if cbc.lym:
                    this_date = datetime.strptime(str(cbc.date), '%Y-%m-%d %H:%M:%S.%f')
                    this_date = time.mktime(this_date.timetuple())
                    date.append(this_date * 1000 + 10800000)
                    result.append(float(cbc.lym))
            elif small_item == 'MID':
                if cbc.mid:
                    this_date = datetime.strptime(str(cbc.date), '%Y-%m-%d %H:%M:%S.%f')
                    this_date = time.mktime(this_date.timetuple())
                    date.append(this_date * 1000 + 10800000)
                    result.append(float(cbc.mid))
            elif small_item == 'PLT':
                if cbc.plt:
                    this_date = datetime.strptime(str(cbc.date), '%Y-%m-%d %H:%M:%S.%f')
                    this_date = time.mktime(this_date.timetuple())
                    date.append(this_date * 1000 + 10800000)
                    result.append(float(cbc.plt))
            elif small_item == 'EsrH1':
                if cbc.esrH1:
                    this_date = datetime.strptime(str(cbc.date), '%Y-%m-%d %H:%M:%S.%f')
                    this_date = time.mktime(this_date.timetuple())
                    date.append(this_date * 1000 + 10800000)
                    result.append(float(cbc.esrH1))
            elif small_item == 'EsrH2':
                if cbc.esrH2:
                    this_date = datetime.strptime(str(cbc.date), '%Y-%m-%d %H:%M:%S.%f')
                    this_date = time.mktime(this_date.timetuple())
                    date.append(this_date * 1000 + 10800000)
                    result.append(float(cbc.esrH2))

    elif big_item == 'Coagulation':
        coagulationObj = Coagulation.objects.filter(patient_id=patient_id, status=True).order_by('-date')
        for coagulation in coagulationObj:
            if small_item == 'PT':
                if coagulation.pt:
                    this_date = datetime.strptime(str(coagulation.date), '%Y-%m-%d %H:%M:%S.%f')
                    this_date = time.mktime(this_date.timetuple())
                    date.append(this_date * 1000 + 10800000)
                    result.append(float(coagulation.pt))
            elif small_item == 'INR':
                if coagulation.inr:
                    this_date = datetime.strptime(str(coagulation.date), '%Y-%m-%d %H:%M:%S.%f')
                    this_date = time.mktime(this_date.timetuple())
                    date.append(this_date * 1000 + 10800000)
                    result.append(float(coagulation.inr))
            elif small_item == 'APPT':
                if coagulation.aptt:
                    this_date = datetime.strptime(str(coagulation.date), '%Y-%m-%d %H:%M:%S.%f')
                    this_date = time.mktime(this_date.timetuple())
                    date.append(this_date * 1000 + 10800000)
                    result.append(float(coagulation.aptt))
            elif small_item == 'BleedTime':
                if coagulation.inr:
                    this_date = datetime.strptime(str(coagulation.date), '%Y-%m-%d %H:%M:%S.%f')
                    this_date = time.mktime(this_date.timetuple())
                    date.append(this_date * 1000 + 10800000)
                    result.append(float(coagulation.bleedTime))
            elif small_item == 'ClotTime':
                if coagulation.inr:
                    this_date = datetime.strptime(str(coagulation.date), '%Y-%m-%d %H:%M:%S.%f')
                    this_date = time.mktime(this_date.timetuple())
                    date.append(this_date * 1000 + 10800000)
                    result.append(float(coagulation.clotTime))
            elif small_item == 'Act':
                if coagulation.act:
                    this_date = datetime.strptime(str(coagulation.date), '%Y-%m-%d %H:%M:%S.%f')
                    this_date = time.mktime(this_date.timetuple())
                    date.append(this_date * 1000 + 10800000)
                    result.append(float(coagulation.act))

    elif big_item == 'Biochemistry':
        biochemistryObj = Biochemistry.objects.filter(patient_id=patient_id, status=True).order_by('-date')
        for biochemistry in biochemistryObj:
            if small_item == 'Glucose':
                if biochemistry.glucose:
                    this_date = datetime.strptime(str(biochemistry.date), '%Y-%m-%d %H:%M:%S.%f')
                    this_date = time.mktime(this_date.timetuple())
                    date.append(this_date * 1000 + 10800000)
                    result.append(float(biochemistry.glucose))
            elif small_item == 'Urea':
                if biochemistry.urea:
                    this_date = datetime.strptime(str(biochemistry.date), '%Y-%m-%d %H:%M:%S.%f')
                    this_date = time.mktime(this_date.timetuple())
                    date.append(this_date * 1000 + 10800000)
                    result.append(float(biochemistry.urea))
            elif small_item == 'Creatine':
                if biochemistry.creatine:
                    this_date = datetime.strptime(str(biochemistry.date), '%Y-%m-%d %H:%M:%S.%f')
                    this_date = time.mktime(this_date.timetuple())
                    date.append(this_date * 1000 + 10800000)
                    result.append(float(biochemistry.creatine))
            elif small_item == 'SGPT':
                if biochemistry.sgpt:
                    this_date = datetime.strptime(str(biochemistry.date), '%Y-%m-%d %H:%M:%S.%f')
                    this_date = time.mktime(this_date.timetuple())
                    date.append(this_date * 1000 + 10800000)
                    result.append(float(biochemistry.sgpt))
            elif small_item == 'SGOT':
                if biochemistry.sgot:
                    this_date = datetime.strptime(str(biochemistry.date), '%Y-%m-%d %H:%M:%S.%f')
                    this_date = time.mktime(this_date.timetuple())
                    date.append(this_date * 1000 + 10800000)
                    result.append(float(biochemistry.sgot))
            elif small_item == 'BiliTotal':
                if biochemistry.biliTotal:
                    this_date = datetime.strptime(str(biochemistry.date), '%Y-%m-%d %H:%M:%S.%f')
                    this_date = time.mktime(this_date.timetuple())
                    date.append(this_date * 1000 + 10800000)
                    result.append(float(biochemistry.biliTotal))
            elif small_item == 'BiliDirect':
                if biochemistry.biliDirect:
                    this_date = datetime.strptime(str(biochemistry.date), '%Y-%m-%d %H:%M:%S.%f')
                    this_date = time.mktime(this_date.timetuple())
                    date.append(this_date * 1000 + 10800000)
                    result.append(float(biochemistry.biliDirect))
            elif small_item == 'BiliIndirect':
                if biochemistry.biliIndirect:
                    this_date = datetime.strptime(str(biochemistry.date), '%Y-%m-%d %H:%M:%S.%f')
                    this_date = time.mktime(this_date.timetuple())
                    date.append(this_date * 1000 + 10800000)
                    result.append(float(biochemistry.biliIndirect))
            elif small_item == 'ALP':
                if biochemistry.alp:
                    this_date = datetime.strptime(str(biochemistry.date), '%Y-%m-%d %H:%M:%S.%f')
                    this_date = time.mktime(this_date.timetuple())
                    date.append(this_date * 1000 + 10800000)
                    result.append(float(biochemistry.alp))
            elif small_item == 'Amylase':
                if biochemistry.amylase:
                    this_date = datetime.strptime(str(biochemistry.date), '%Y-%m-%d %H:%M:%S.%f')
                    this_date = time.mktime(this_date.timetuple())
                    date.append(this_date * 1000 + 10800000)
                    result.append(float(biochemistry.amylase))
            elif small_item == 'LDH':
                if biochemistry.ldh:
                    this_date = datetime.strptime(str(biochemistry.date), '%Y-%m-%d %H:%M:%S.%f')
                    this_date = time.mktime(this_date.timetuple())
                    date.append(this_date * 1000 + 10800000)
                    result.append(float(biochemistry.ldh))
            elif small_item == 'Albumin':
                if biochemistry.albumin:
                    this_date = datetime.strptime(str(biochemistry.date), '%Y-%m-%d %H:%M:%S.%f')
                    this_date = time.mktime(this_date.timetuple())
                    date.append(this_date * 1000 + 10800000)
                    result.append(float(biochemistry.albumin))
            elif small_item == 'TotalProtein':
                if biochemistry.totalProtein:
                    this_date = datetime.strptime(str(biochemistry.date), '%Y-%m-%d %H:%M:%S.%f')
                    this_date = time.mktime(this_date.timetuple())
                    date.append(this_date * 1000 + 10800000)
                    result.append(float(biochemistry.totalProtein))
            elif small_item == 'CK':
                if biochemistry.ck:
                    this_date = datetime.strptime(str(biochemistry.date), '%Y-%m-%d %H:%M:%S.%f')
                    this_date = time.mktime(this_date.timetuple())
                    date.append(this_date * 1000 + 10800000)
                    result.append(float(biochemistry.ck))
            elif small_item == 'CK_MB':
                if biochemistry.ck_mb:
                    this_date = datetime.strptime(str(biochemistry.date), '%Y-%m-%d %H:%M:%S.%f')
                    this_date = time.mktime(this_date.timetuple())
                    date.append(this_date * 1000 + 10800000)
                    result.append(float(biochemistry.ck_mb))
            elif small_item == 'Lipase':
                if biochemistry.lipase:
                    this_date = datetime.strptime(str(biochemistry.date), '%Y-%m-%d %H:%M:%S.%f')
                    this_date = time.mktime(this_date.timetuple())
                    date.append(this_date * 1000 + 10800000)
                    result.append(float(biochemistry.lipase))
            elif small_item == 'UricAcid':
                if biochemistry.uric_acid:
                    this_date = datetime.strptime(str(biochemistry.date), '%Y-%m-%d %H:%M:%S.%f')
                    this_date = time.mktime(this_date.timetuple())
                    date.append(this_date * 1000 + 10800000)
                    result.append(float(biochemistry.uric_acid))
            elif small_item == 'Triglycerid':
                if biochemistry.triglycerid:
                    this_date = datetime.strptime(str(biochemistry.date), '%Y-%m-%d %H:%M:%S.%f')
                    this_date = time.mktime(this_date.timetuple())
                    date.append(this_date * 1000 + 10800000)
                    result.append(float(biochemistry.triglycerid))
            elif small_item == 'Cholesterol':
                if biochemistry.cholesterol:
                    this_date = datetime.strptime(str(biochemistry.date), '%Y-%m-%d %H:%M:%S.%f')
                    this_date = time.mktime(this_date.timetuple())
                    date.append(this_date * 1000 + 10800000)
                    result.append(float(biochemistry.cholesterol))
            elif small_item == 'CRP':
                if biochemistry.crp:
                    this_date = datetime.strptime(str(biochemistry.date), '%Y-%m-%d %H:%M:%S.%f')
                    this_date = time.mktime(this_date.timetuple())
                    date.append(this_date * 1000 + 10800000)
                    result.append(float(biochemistry.crp))
            elif small_item == 'Aslo':
                if biochemistry.aslo:
                    this_date = datetime.strptime(str(biochemistry.date), '%Y-%m-%d %H:%M:%S.%f')
                    this_date = time.mktime(this_date.timetuple())
                    date.append(this_date * 1000 + 10800000)
                    result.append(float(biochemistry.aslo))
            elif small_item == 'RF':
                if biochemistry.rf:
                    this_date = datetime.strptime(str(biochemistry.date), '%Y-%m-%d %H:%M:%S.%f')
                    this_date = time.mktime(this_date.timetuple())
                    date.append(this_date * 1000 + 10800000)
                    result.append(float(biochemistry.rf))

    elif big_item == 'Electrolytes':
        electrolytesObj = Electrolytes.objects.filter(patient_id=patient_id, status=True).order_by('-date')
        for electrolytes in electrolytesObj:
            if small_item == 'Na':
                if electrolytes.na:
                    this_date = datetime.strptime(str(electrolytes.date), '%Y-%m-%d %H:%M:%S.%f')
                    this_date = time.mktime(this_date.timetuple())
                    date.append(this_date * 1000 + 10800000)
                    result.append(float(electrolytes.na))
            elif small_item == 'K':
                if electrolytes.k:
                    this_date = datetime.strptime(str(electrolytes.date), '%Y-%m-%d %H:%M:%S.%f')
                    this_date = time.mktime(this_date.timetuple())
                    date.append(this_date * 1000 + 10800000)
                    result.append(float(electrolytes.k))
            elif small_item == 'Cl':
                if electrolytes.cl:
                    this_date = datetime.strptime(str(electrolytes.date), '%Y-%m-%d %H:%M:%S.%f')
                    this_date = time.mktime(this_date.timetuple())
                    date.append(this_date * 1000 + 10800000)
                    result.append(float(electrolytes.cl))
            elif small_item == 'TCa':
                if electrolytes.tca:
                    this_date = datetime.strptime(str(electrolytes.date), '%Y-%m-%d %H:%M:%S.%f')
                    this_date = time.mktime(this_date.timetuple())
                    date.append(this_date * 1000 + 10800000)
                    result.append(float(electrolytes.tca))
            elif small_item == 'NCa':
                if electrolytes.nca:
                    this_date = datetime.strptime(str(electrolytes.date), '%Y-%m-%d %H:%M:%S.%f')
                    this_date = time.mktime(this_date.timetuple())
                    date.append(this_date * 1000 + 10800000)
                    result.append(float(electrolytes.nca))
            elif small_item == 'ICa':
                if electrolytes.ica:
                    this_date = datetime.strptime(str(electrolytes.date), '%Y-%m-%d %H:%M:%S.%f')
                    this_date = time.mktime(this_date.timetuple())
                    date.append(this_date * 1000 + 10800000)
                    result.append(float(electrolytes.ica))
            elif small_item == 'Iron':
                if electrolytes.iron:
                    this_date = datetime.strptime(str(electrolytes.date), '%Y-%m-%d %H:%M:%S.%f')
                    this_date = time.mktime(this_date.timetuple())
                    date.append(this_date * 1000 + 10800000)
                    result.append(float(electrolytes.iron))
            elif small_item == 'Mg':
                if electrolytes.mg:
                    this_date = datetime.strptime(str(electrolytes.date), '%Y-%m-%d %H:%M:%S.%f')
                    this_date = time.mktime(this_date.timetuple())
                    date.append(this_date * 1000 + 10800000)
                    result.append(float(electrolytes.mg))
            elif small_item == 'Phosphorus':
                if electrolytes.phosphorus:
                    this_date = datetime.strptime(str(electrolytes.date), '%Y-%m-%d %H:%M:%S.%f')
                    this_date = time.mktime(this_date.timetuple())
                    date.append(this_date * 1000 + 10800000)
                    result.append(float(electrolytes.phosphorus))

    elif big_item == 'ABG':
        abgObj = ABG.objects.filter(patient_id=patient_id, status=True).order_by('-date')
        for abg in abgObj:
            if small_item == 'PH':
                if abg.ph:
                    this_date = datetime.strptime(str(abg.date), '%Y-%m-%d %H:%M:%S.%f')
                    this_date = time.mktime(this_date.timetuple())
                    date.append(this_date * 1000 + 10800000)
                    result.append(float(abg.ph))
            elif small_item == 'Pc02':
                if abg.pc02:
                    this_date = datetime.strptime(str(abg.date), '%Y-%m-%d %H:%M:%S.%f')
                    this_date = time.mktime(this_date.timetuple())
                    date.append(this_date * 1000 + 10800000)
                    result.append(float(abg.pc02))
            elif small_item == 'P02':
                if abg.p02:
                    this_date = datetime.strptime(str(abg.date), '%Y-%m-%d %H:%M:%S.%f')
                    this_date = time.mktime(this_date.timetuple())
                    date.append(this_date * 1000 + 10800000)
                    result.append(float(abg.p02))
            elif small_item == 'Na':
                if abg.na:
                    this_date = datetime.strptime(str(abg.date), '%Y-%m-%d %H:%M:%S.%f')
                    this_date = time.mktime(this_date.timetuple())
                    date.append(this_date * 1000 + 10800000)
                    result.append(float(abg.na))
            elif small_item == 'K':
                if abg.k:
                    this_date = datetime.strptime(str(abg.date), '%Y-%m-%d %H:%M:%S.%f')
                    this_date = time.mktime(this_date.timetuple())
                    date.append(this_date * 1000 + 10800000)
                    result.append(float(abg.k))
            elif small_item == 'Ca1':
                if abg.ca1:
                    this_date = datetime.strptime(str(abg.date), '%Y-%m-%d %H:%M:%S.%f')
                    this_date = time.mktime(this_date.timetuple())
                    date.append(this_date * 1000 + 10800000)
                    result.append(float(abg.ca1))
            elif small_item == 'Glucose':
                if abg.glucose:
                    this_date = datetime.strptime(str(abg.date), '%Y-%m-%d %H:%M:%S.%f')
                    this_date = time.mktime(this_date.timetuple())
                    date.append(this_date * 1000 + 10800000)
                    result.append(float(abg.glucose))
            elif small_item == 'Lac':
                if abg.lac:
                    this_date = datetime.strptime(str(abg.date), '%Y-%m-%d %H:%M:%S.%f')
                    this_date = time.mktime(this_date.timetuple())
                    date.append(this_date * 1000 + 10800000)
                    result.append(float(abg.lac))
            elif small_item == 'HC03':
                if abg.hc03:
                    this_date = datetime.strptime(str(abg.date), '%Y-%m-%d %H:%M:%S.%f')
                    this_date = time.mktime(this_date.timetuple())
                    date.append(this_date * 1000 + 10800000)
                    result.append(float(abg.hc03))
            elif small_item == 'Beecf':
                if abg.beecf:
                    this_date = datetime.strptime(str(abg.date), '%Y-%m-%d %H:%M:%S.%f')
                    this_date = time.mktime(this_date.timetuple())
                    date.append(this_date * 1000 + 10800000)
                    result.append(float(abg.beecf))
            elif small_item == 'S02c':
                if abg.s02c:
                    this_date = datetime.strptime(str(abg.date), '%Y-%m-%d %H:%M:%S.%f')
                    this_date = time.mktime(this_date.timetuple())
                    date.append(this_date * 1000 + 10800000)
                    result.append(float(abg.s02c))
            elif small_item == 'Fi02':
                if abg.fi02:
                    this_date = datetime.strptime(str(abg.date), '%Y-%m-%d %H:%M:%S.%f')
                    this_date = time.mktime(this_date.timetuple())
                    date.append(this_date * 1000 + 10800000)
                    result.append(float(abg.fi02))

    elif big_item == 'Serology':
        date = []
        result = []
        serologyObj = Serology.objects.filter(patient_id=patient_id, status=True).order_by('-date')
        for serology in serologyObj:
            if small_item == 'Fob':
                if serology.fob:
                    this_date = datetime.strptime(str(serology.date), '%Y-%m-%d %H:%M:%S.%f')
                    this_date = time.mktime(this_date.timetuple())
                    date.append(this_date * 1000 + 10800000)
                    result.append(float(serology.fob))

    elif big_item == 'UrineAnalysis':
        urineAnalysisObj = UrineAnalysis.objects.filter(patient_id=patient_id, status=True).order_by('-date')
        for urineAnalysis in urineAnalysisObj:
            if small_item == 'PH':
                if urineAnalysis.ph:
                    this_date = datetime.strptime(str(urineAnalysis.date), '%Y-%m-%d %H:%M:%S.%f')
                    this_date = time.mktime(this_date.timetuple())
                    date.append(this_date * 1000 + 10800000)
                    result.append(float(urineAnalysis.ph))
            elif small_item == 'SpGravity':
                if urineAnalysis.spGravity:
                    this_date = datetime.strptime(str(urineAnalysis.date), '%Y-%m-%d %H:%M:%S.%f')
                    this_date = time.mktime(this_date.timetuple())
                    date.append(this_date * 1000 + 10800000)
                    result.append(float(urineAnalysis.spGravity))
            elif small_item == 'K':
                if urineAnalysis.k:
                    this_date = datetime.strptime(str(urineAnalysis.date), '%Y-%m-%d %H:%M:%S.%f')
                    this_date = time.mktime(this_date.timetuple())
                    date.append(this_date * 1000 + 10800000)
                    result.append(float(urineAnalysis.k))
            elif small_item == 'Na':
                if urineAnalysis.na:
                    this_date = datetime.strptime(str(urineAnalysis.date), '%Y-%m-%d %H:%M:%S.%f')
                    this_date = time.mktime(this_date.timetuple())
                    date.append(this_date * 1000 + 10800000)
                    result.append(float(urineAnalysis.na))
            elif small_item == 'Creatinine':
                if urineAnalysis.creatinine:
                    this_date = datetime.strptime(str(urineAnalysis.date), '%Y-%m-%d %H:%M:%S.%f')
                    this_date = time.mktime(this_date.timetuple())
                    date.append(this_date * 1000 + 10800000)
                    result.append(float(urineAnalysis.creatinine))
            elif small_item == 'Amylase':
                if urineAnalysis.amylase:
                    this_date = datetime.strptime(str(urineAnalysis.date), '%Y-%m-%d %H:%M:%S.%f')
                    this_date = time.mktime(this_date.timetuple())
                    date.append(this_date * 1000 + 10800000)
                    result.append(float(urineAnalysis.amylase))

    elif big_item == 'CSF':
        csfObj = CSF.objects.filter(patient_id=patient_id, status=True).order_by('-date')
        for csf in csfObj:
            if small_item == 'RBC':
                if csf.rbc:
                    this_date = datetime.strptime(str(csf.date), '%Y-%m-%d %H:%M:%S.%f')
                    this_date = time.mktime(this_date.timetuple())
                    date.append(this_date * 1000 + 10800000)
                    result.append(float(csf.rbc))
            elif small_item == 'Glucose':
                if csf.glucose:
                    this_date = datetime.strptime(str(csf.date), '%Y-%m-%d %H:%M:%S.%f')
                    this_date = time.mktime(this_date.timetuple())
                    date.append(this_date * 1000 + 10800000)
                    result.append(float(csf.glucose))
            elif small_item == 'WBC':
                if csf.wbc:
                    this_date = datetime.strptime(str(csf.date), '%Y-%m-%d %H:%M:%S.%f')
                    this_date = time.mktime(this_date.timetuple())
                    date.append(this_date * 1000 + 10800000)
                    result.append(float(csf.wbc))
            elif small_item == 'Protein':
                if csf.protein:
                    this_date = datetime.strptime(str(csf.date), '%Y-%m-%d %H:%M:%S.%f')
                    this_date = time.mktime(this_date.timetuple())
                    date.append(this_date * 1000 + 10800000)
                    result.append(float(csf.protein))

    return render(request, 'laboratory/graphicsLaboratory.html', locals())


@login_required
def todayPatients(request):
    """所有的病人"""

    username = request.session['name']
    user = User.objects.all().get(name=username)

    # 病房
    wards = user.authorityWard.filter(status=True)

    date = datetime.today().date()

    patientsOfToday = PatientInfo.objects.filter(enterDate__date=date, condition=1).order_by('sickroom__name')

    return render(request, 'laboratory/todayPatients.html', locals())


@login_required
def searchLaboratoryPatient(request):

    user = User.objects.all().get(name=request.session['name'])

    # 病房
    wards = user.authorityWard.filter(status=True)

    message = ''

    if request.method == 'POST':

        search = request.POST.get('search')

        patients = PatientInfo.objects.filter(Q(basicInfo__name__contains=search, condition__gt=0) |
                                              Q(patientID=search, condition__gt=0))

        if patients:

            return render(request, 'laboratory/searchLaboratoryPatient.html', locals())

        else:
            message = 'Not Found !'

            return render(request, 'laboratory/searchLaboratoryPatient.html', locals())


@login_required
def laboratory(request, patient_id, patient_num):
    """显示当前病人的检验报告"""

    user = User.objects.get(name=request.session['name'])

    # 病房
    wards = user.authorityWard.filter(status=True)

    bloodTypes = ['', 'A: Neg-', 'A: Pos+', 'B: Neg-', 'B: Pos+',
                  'AB:Neg-', 'AB:Pos+', 'O: Neg-', 'O: Pos+']

    colors = ['', 'Yellow', 'Dp Yellow', 'Lt Yellow', 'Red', 'Black', 'Brown', 'Green']

    patient = PatientInfo.objects.get(id=patient_id)

    return render(request, 'laboratory/laboratory.html', locals())


@login_required
def write_cbc(request, patient_id, patient_num):

    # 当前需要的信息
    user = User.objects.get(name=request.session['name'])

    if request.method == "POST":
        rbc = request.POST.get('rbc')
        mcv = request.POST.get('mcv')
        mch = request.POST.get('mch')
        mchc = request.POST.get('mchc')
        rdw = request.POST.get('rdw')
        bloodGroup = request.POST.get('bloodGroup')
        hemoglobin = request.POST.get('hemoglobin')
        hematocrite = request.POST.get('hematocrite')
        wbc = request.POST.get('wbc')
        gran = request.POST.get('gran')
        lym = request.POST.get('lym')
        mid = request.POST.get('mid')
        plt = request.POST.get('plt')
        esrH1 = request.POST.get('esrH1')
        esrH2 = request.POST.get('esrH2')

        if rbc or mcv or mch or mchc or rdw or bloodGroup or hemoglobin or hematocrite or wbc or gran or lym or mid or plt or esrH1 or esrH2:
            cbc = CBC.objects.create(recorder=user.arabic_name, patient_id=patient_id)

            if rbc:
                cbc.rbc = rbc
            if mcv:
                cbc.mcv = mcv
            if mch:
                cbc.mch = mch
            if mchc:
                cbc.mchc = mchc
            if rdw:
                cbc.rdw = rdw
            if bloodGroup:
                cbc.bloodGroup = bloodGroup
            if hemoglobin:
                cbc.hemoglobin = hemoglobin
            if hematocrite:
                cbc.hematocrite = hematocrite
            if wbc:
                cbc.wbc = wbc
            if gran:
                cbc.gran = gran
            if lym:
                cbc.lym = lym
            if mid:
                cbc.mid = mid
            if plt:
                cbc.plt = plt
            if esrH1:
                cbc.esrH1 = esrH1
            if esrH2:
                cbc.esrH2 = esrH2

            cbc.save()

            # 标记已完成化验单
            patient = PatientInfo.objects.get(id=patient_id)
            patient.haveLaboratoryTest = 2
            patient.save()

            url = reverse('laboratory', args=(patient_id, patient_num))

            return redirect(url)

        else:

            message = 'Please input data !'

            url = reverse('laboratory', args=(patient_id, patient_num))

            return redirect(url, locals())


@login_required
def write_coagulation(request, patient_id, patient_num):

    # 当前需要的信息
    patient = PatientInfo.objects.all().get(id=patient_id)
    user = User.objects.get(name=request.session['name'])

    if request.method == "POST":
        pt = request.POST.get('pt')
        inr = request.POST.get('inr')
        aptt = request.POST.get('aptt')
        bleedTime = request.POST.get('bleedTime')
        clotTime = request.POST.get('clotTime')
        act = request.POST.get('act')

        if pt or inr or aptt or bleedTime or clotTime or act:

            coagulation = Coagulation.objects.create(recorder=user.arabic_name, patient_id=patient_id)

            if pt:
                coagulation.pt = pt
            if inr:
                coagulation.inr = inr
            if aptt:
                coagulation.aptt = aptt
            if bleedTime:
                coagulation.bleedTime = bleedTime
            if clotTime:
                coagulation.clotTime = clotTime
            if act:
                coagulation.act = act

            coagulation.save()

            # 标记已完成化验单
            patient = PatientInfo.objects.get(id=patient_id)
            patient.haveLaboratoryTest = 2
            patient.save()

            url = reverse('laboratory', args=(patient_id, patient_num))

            return redirect(url)

        else:

            message = 'Please input data !'

            url = reverse('laboratory', args=(patient_id, patient_num))

            return redirect(url, locals())
            # return render(request, 'laboratory/laboratory.html', locals())


@login_required
def write_biochemistry(request, patient_id, patient_num):

    # 当前需要的信息
    user = User.objects.get(name=request.session['name'])

    if request.method == "POST":
        glucose = request.POST.get('glucose')
        urea = request.POST.get('urea')
        creatine = request.POST.get('creatine')
        sgpt = request.POST.get('sgpt')
        sgot = request.POST.get('sgot')
        biliTotal = request.POST.get('biliTotal')
        biliDirect = request.POST.get('biliDirect')
        biliIndirect = request.POST.get('biliIndirect')
        alp = request.POST.get('alp')
        amylase = request.POST.get('amylase')
        ldh = request.POST.get('ldh')
        albumin = request.POST.get('albumin')
        totalProtein = request.POST.get('totalProtein')
        ck = request.POST.get('ck')
        ck_mb = request.POST.get('ck_mb')
        lipase = request.POST.get('lipase')
        uric_acid = request.POST.get('uric_acid')
        triglycerid = request.POST.get('triglycerid')
        cholesterol = request.POST.get('cholesterol')
        crp = request.POST.get('crp')
        aslo = request.POST.get('aslo')
        rf = request.POST.get('rf')

        if glucose or urea or creatine or sgpt or sgot or biliTotal or biliDirect or \
                biliIndirect or alp or amylase or ldh or albumin or totalProtein or ck or \
                ck_mb or lipase or uric_acid or triglycerid or cholesterol or crp or aslo or rf:
            biochemistry = Biochemistry.objects.create(recorder=user.arabic_name, patient_id=patient_id)

            if glucose:
                biochemistry.glucose = glucose
            if urea:
                biochemistry.urea = urea
            if creatine:
                biochemistry.creatine = creatine
            if sgpt:
                biochemistry.sgpt = sgpt
            if sgot:
                biochemistry.sgot = sgot
            if biliTotal:
                biochemistry.biliTotal = biliTotal
            if biliDirect:
                biochemistry.biliDirect = biliDirect
            if biliIndirect:
                biochemistry.biliIndirect = biliIndirect
            if alp:
                biochemistry.alp = alp
            if amylase:
                biochemistry.amylase = amylase
            if ldh:
                biochemistry.ldh = ldh
            if albumin:
                biochemistry.albumin = albumin
            if totalProtein:
                biochemistry.totalProtein = totalProtein
            if ck:
                biochemistry.ck = ck
            if ck_mb:
                biochemistry.ck_mb = ck_mb
            if lipase:
                biochemistry.lipase = lipase
            if uric_acid:
                biochemistry.uric_acid = uric_acid
            if triglycerid:
                biochemistry.triglycerid = triglycerid
            if cholesterol:
                biochemistry.cholesterol = cholesterol
            if crp:
                biochemistry.crp = crp
            if aslo:
                biochemistry.aslo = aslo
            if rf:
                biochemistry.rf = rf

            biochemistry.save()

            # 标记已完成化验单
            patient = PatientInfo.objects.get(id=patient_id)
            patient.haveLaboratoryTest = 2
            patient.save()

            url = reverse('laboratory', args=(patient_id, patient_num))

            return redirect(url)

        else:

            message = 'Please input data !'

            url = reverse('laboratory', args=(patient_id, patient_num))

            return redirect(url, locals())


@login_required
def write_electrolytes(request, patient_id, patient_num):

    # 当前需要的信息
    user = User.objects.get(name=request.session['name'])

    if request.method == "POST":
        na = request.POST.get('na')
        k = request.POST.get('k')
        cl = request.POST.get('cl')
        tca = request.POST.get('tca')
        nca = request.POST.get('nca')
        ica = request.POST.get('ica')
        iron = request.POST.get('iron')
        mg = request.POST.get('mg')
        phosphorus = request.POST.get('phosphorus')

        if na or k or cl or tca or nca or ica or iron or mg or phosphorus:
            electrolytes = Electrolytes.objects.create(recorder=user.arabic_name, patient_id=patient_id)

            if na:
                electrolytes.na = na
            if k:
                electrolytes.k = k
            if cl:
                electrolytes.cl = cl
            if tca:
                electrolytes.tca = tca
            if nca:
                electrolytes.nca = nca
            if ica:
                electrolytes.ica = ica
            if iron:
                electrolytes.iron = iron
            if mg:
                electrolytes.mg = mg
            if phosphorus:
                electrolytes.phosphorus = phosphorus

            electrolytes.save()

            # 标记已完成化验单
            patient = PatientInfo.objects.get(id=patient_id)
            patient.haveLaboratoryTest = 2
            patient.save()

            url = reverse('laboratory', args=(patient_id, patient_num))

            return redirect(url)

        else:

            message = 'Please input data !'

            url = reverse('laboratory', args=(patient_id, patient_num))

            return redirect(url, locals())


@login_required
def write_abg(request, patient_id, patient_num):

    # 当前需要的信息
    user = User.objects.get(name=request.session['name'])

    if request.method == "POST":
        ph = request.POST.get('ph')
        pc02 = request.POST.get('pc02')
        p02 = request.POST.get('p02')
        na = request.POST.get('na')
        k = request.POST.get('k')
        ca1 = request.POST.get('ca1')
        glucose = request.POST.get('glucose')
        lac = request.POST.get('lac')
        hc03 = request.POST.get('hc03')
        beecf = request.POST.get('beecf')
        s02c = request.POST.get('s02c')
        fi02 = request.POST.get('fi02')

        if ph or pc02 or p02 or na or k or ca1 or glucose or lac or hc03 or beecf or s02c or fi02:
            abg = ABG.objects.create(recorder=user.arabic_name, patient_id=patient_id)

            if ph:
                abg.ph = ph
            if pc02:
                abg.pc02 = pc02
            if p02:
                abg.p02 = p02
            if na:
                abg.na = na
            if k:
                abg.k = k
            if ca1:
                abg.ca1 = ca1
            if glucose:
                abg.glucose = glucose
            if lac:
                abg.lac = lac
            if hc03:
                abg.hc03 = hc03
            if beecf:
                abg.beecf = beecf
            if s02c:
                abg.s02c = s02c
            if fi02:
                abg.fi02 = fi02

            abg.save()

            # 标记已完成化验单
            patient = PatientInfo.objects.get(id=patient_id)
            patient.haveLaboratoryTest = 2
            patient.save()

            url = reverse('laboratory', args=(patient_id, patient_num))

            return redirect(url)

        else:

            message = 'Please input data !'

            url = reverse('laboratory', args=(patient_id, patient_num))

            return redirect(url, locals())


@login_required
def write_serology(request, patient_id, patient_num):

    # 当前需要的信息
    user = User.objects.get(name=request.session['name'])

    if request.method == "POST":
        hbs_Ag = request.POST.get('hbs_Ag')
        hiv = request.POST.get('hiv')
        hcv = request.POST.get('hcv')
        hcg = request.POST.get('hcg')
        fob = request.POST.get('fob')
        widal_o = request.POST.get('widal_o')
        widal_h = request.POST.get('widal_h')
        wrigh_a = request.POST.get('wrigh_a')
        wrigh_b = request.POST.get('wrigh_b')

        if hbs_Ag or hiv or hcv or hcg or fob or widal_o or widal_h or wrigh_a or wrigh_b:
            serology = Serology.objects.create(recorder=user.arabic_name, patient_id=patient_id)

            if hbs_Ag:
                serology.hbs_Ag = hbs_Ag
            if hiv:
                serology.hiv = hiv
            if hcv:
                serology.hcv = hcv
            if hcg:
                serology.hcg = hcg
            if fob:
                serology.fob = fob
            if widal_o:
                serology.widal_o = widal_o
            if widal_h:
                serology.widal_h = widal_h
            if wrigh_a:
                serology.wrigh_a = wrigh_a
            if wrigh_b:
                serology.wrigh_b = wrigh_b

            serology.save()

            # 标记已完成化验单
            patient = PatientInfo.objects.get(id=patient_id)
            patient.haveLaboratoryTest = 2
            patient.save()

            url = reverse('laboratory', args=(patient_id, patient_num))

            return redirect(url)

        else:

            message = 'Please input data !'

            url = reverse('laboratory', args=(patient_id, patient_num))

            return redirect(url, locals())


@login_required
def write_urineAnalysis(request, patient_id, patient_num):

    # 当前需要的信息
    user = User.objects.get(name=request.session['name'])

    if request.method == "POST":
        color = request.POST.get('color')
        spGravity = request.POST.get('spGravity')
        netrit = request.POST.get('netrit')
        wbc = request.POST.get('wbc')
        urates = request.POST.get('urates')
        uric_acid = request.POST.get('uric_acid')
        appearance = request.POST.get('appearance')
        glucose = request.POST.get('glucose')
        keton = request.POST.get('keton')
        rbc = request.POST.get('rbc')
        bacteria = request.POST.get('bacteria')
        mucus = request.POST.get('mucus')
        ph = request.POST.get('ph')
        blood = request.POST.get('blood')
        protein = request.POST.get('protein')
        epCells = request.POST.get('epCells')
        ox_calcium = request.POST.get('ox_calcium')
        casts = request.POST.get('casts')
        fungi = request.POST.get('fungi')
        yeast = request.POST.get('yeast')
        pus_cell = request.POST.get('pus_cell')
        triple_phospate = request.POST.get('triple_phospate')

        if color or spGravity or netrit or wbc or urates or uric_acid or appearance or glucose or\
           keton or rbc or bacteria or mucus or ph or blood or protein or epCells or ox_calcium or \
           casts or fungi or yeast or pus_cell or triple_phospate:
            urineAnalysis = UrineAnalysis.objects.create(recorder=user.arabic_name, patient_id=patient_id)

            if color:
                urineAnalysis.color = color
            if spGravity:
                urineAnalysis.spGravity = spGravity
            if netrit:
                urineAnalysis.netrit = netrit
            if wbc:
                urineAnalysis.wbc = wbc
            if urates:
                urineAnalysis.urates = urates
            if uric_acid:
                urineAnalysis.uric_acid = uric_acid
            if appearance:
                urineAnalysis.appearance = appearance
            if glucose:
                urineAnalysis.glucose = glucose
            if keton:
                urineAnalysis.keton = keton
            if rbc:
                urineAnalysis.rbc = rbc
            if bacteria:
                urineAnalysis.bacteria = bacteria
            if mucus:
                urineAnalysis.mucus = mucus
            if ph:
                urineAnalysis.ph = ph
            if blood:
                urineAnalysis.blood = blood
            if protein:
                urineAnalysis.protein = protein
            if epCells:
                urineAnalysis.epCells = epCells
            if ox_calcium:
                urineAnalysis.ox_calcium = ox_calcium
            if casts:
                urineAnalysis.casts = casts
            if fungi:
                urineAnalysis.fungi = fungi
            if yeast:
                urineAnalysis.yeast = yeast
            if pus_cell:
                urineAnalysis.pus_cell = pus_cell
            if triple_phospate:
                urineAnalysis.triple_phospate = triple_phospate

            urineAnalysis.save()

            # 标记已完成化验单
            patient = PatientInfo.objects.get(id=patient_id)
            patient.haveLaboratoryTest = 2
            patient.save()

            url = reverse('laboratory', args=(patient_id, patient_num))

            return redirect(url)

        else:

            message = 'Please input data !'

            url = reverse('laboratory', args=(patient_id, patient_num))

            return redirect(url, locals())


@login_required
def write_csf(request, patient_id, patient_num):

    # 当前需要的信息
    patient = PatientInfo.objects.all().get(id=patient_id)
    user = User.objects.get(name=request.session['name'])

    if request.method == "POST":
        color = request.POST.get('color')
        appearance = request.POST.get('appearance')
        rbc = request.POST.get('rbc')
        wbc = request.POST.get('wbc')
        glucose = request.POST.get('glucose')
        protein = request.POST.get('protein')

        if color or appearance or rbc or wbc or glucose or protein:

            csf = CSF.objects.create(recorder=user.arabic_name, patient_id=patient_id)

            if color:
                csf.color = color
            if appearance:
                csf.appearance = appearance
            if rbc:
                csf.rbc = rbc
            if wbc:
                csf.wbc = wbc
            if glucose:
                csf.glucose = glucose
            if protein:
                csf.protein = protein

            csf.save()

            # 标记已完成化验单
            patient = PatientInfo.objects.get(id=patient_id)
            patient.haveLaboratoryTest = 2
            patient.save()

            url = reverse('laboratory', args=(patient_id, patient_num))

            return redirect(url)

        else:

            message = 'Please input data !'

            url = reverse('laboratory', args=(patient_id, patient_num))

            return redirect(url, locals())
            # return render(request, 'laboratory/laboratory.html', locals())


@login_required
def write_antibiotics(request, patient_id, patient_num):

    # 当前需要的信息
    patient = PatientInfo.objects.all().get(id=patient_id)
    user = User.objects.get(name=request.session['name'])

    if request.method == "POST":
        cephradine = request.POST.get('cephradine')
        ciprofloxacin = request.POST.get('ciprofloxacin')
        gentamicin = request.POST.get('gentamicin')
        nitrofurantoin = request.POST.get('nitrofurantoin')
        ofloxacin = request.POST.get('ofloxacin')
        cefoxitin = request.POST.get('cefoxitin')
        cefaclor = request.POST.get('cefaclor')
        amikacin = request.POST.get('amikacin')
        ceftriaxone = request.POST.get('ceftriaxone')
        amoxicillin_clavulanic_acid = request.POST.get('amoxicillin_clavulanic_acid')
        cefadroxil = request.POST.get('cefadroxil')
        cefixime = request.POST.get('cefixime')
        cefotaxime = request.POST.get('cefotaxime')
        cefuroxime = request.POST.get('cefuroxime')
        imipenem = request.POST.get('imipenem')
        ampicillin_sulbactam = request.POST.get('ampicillin_sulbactam')
        amoxicillin = request.POST.get('amoxicillin')
        azithromycin = request.POST.get('azithromycin')
        levofloxacin = request.POST.get('levofloxacin')
        neomycin = request.POST.get('neomycin')
        doxycycline = request.POST.get('doxycycline')
        pipemidic_acid = request.POST.get('pipemidic_acid')
        meropenem = request.POST.get('meropenem')
        cloxacillin = request.POST.get('cloxacillin')
        trimethoprim_sulphamethoxazole = request.POST.get('trimethoprim_sulphamethoxazole')
        norfloxacin = request.POST.get('norfloxacin')

        if cephradine or ciprofloxacin or gentamicin or nitrofurantoin or ofloxacin or cefoxitin or \
                cefaclor or amikacin or ceftriaxone or amoxicillin_clavulanic_acid or cefadroxil or \
                cefixime or cefotaxime or cefuroxime or imipenem or ampicillin_sulbactam or amoxicillin or \
                azithromycin or levofloxacin or neomycin or doxycycline or pipemidic_acid or meropenem or \
                cloxacillin or trimethoprim_sulphamethoxazole or norfloxacin:

            antibiotics = Antibiotics.objects.create(recorder=user.arabic_name, patient_id=patient_id)

            if cephradine:
                antibiotics.cephradine = cephradine
            if ciprofloxacin:
                antibiotics.ciprofloxacin = ciprofloxacin
            if gentamicin:
                antibiotics.gentamicin = gentamicin
            if nitrofurantoin:
                antibiotics.nitrofurantoin = nitrofurantoin
            if ofloxacin:
                antibiotics.ofloxacin = ofloxacin
            if cefoxitin:
                antibiotics.cefoxitin = cefoxitin
            if cefaclor:
                antibiotics.cefaclor = cefaclor
            if amikacin:
                antibiotics.amikacin = amikacin
            if ceftriaxone:
                antibiotics.ceftriaxone = ceftriaxone
            if amoxicillin_clavulanic_acid:
                antibiotics.amoxicillin_clavulanic_acid = amoxicillin_clavulanic_acid
            if cefadroxil:
                antibiotics.cefadroxil = cefadroxil
            if cefixime:
                antibiotics.cefixime = cefixime
            if cefotaxime:
                antibiotics.cefotaxime = cefotaxime
            if cefuroxime:
                antibiotics.cefuroxime = cefuroxime
            if imipenem:
                antibiotics.imipenem = imipenem
            if ampicillin_sulbactam:
                antibiotics.ampicillin_sulbactam = ampicillin_sulbactam
            if amoxicillin:
                antibiotics.amoxicillin = amoxicillin
            if azithromycin:
                antibiotics.azithromycin = azithromycin
            if levofloxacin:
                antibiotics.levofloxacin = levofloxacin
            if neomycin:
                antibiotics.neomycin = neomycin
            if doxycycline:
                antibiotics.doxycycline = doxycycline
            if pipemidic_acid:
                antibiotics.pipemidic_acid = pipemidic_acid
            if meropenem:
                antibiotics.meropenem = meropenem
            if cloxacillin:
                antibiotics.cloxacillin = cloxacillin
            if trimethoprim_sulphamethoxazole:
                antibiotics.trimethoprim_sulphamethoxazole = trimethoprim_sulphamethoxazole
            if norfloxacin:
                antibiotics.norfloxacin = norfloxacin

            antibiotics.save()

            # 标记已完成化验单
            patient = PatientInfo.objects.get(id=patient_id)
            patient.haveLaboratoryTest = 2
            patient.save()

            url = reverse('laboratory', args=(patient_id, patient_num))

            return redirect(url)

        else:

            message = 'Please input data !'

            url = reverse('laboratory', args=(patient_id, patient_num))

            return redirect(url, locals())


@login_required
def write_hormones(request, patient_id, patient_num):

    # 当前需要的信息
    patient = PatientInfo.objects.all().get(id=patient_id)
    user = User.objects.get(name=request.session['name'])

    if request.method == "POST":
        hba1c = request.POST.get('hba1c')
        tsh = request.POST.get('tsh')
        ft4 = request.POST.get('ft4')
        t4 = request.POST.get('t4')
        t3 = request.POST.get('t3')
        lh = request.POST.get('lh')
        fsh = request.POST.get('fsh')
        prolactin = request.POST.get('prolactin')
        testosterone = request.POST.get('testosterone')
        cortisol = request.POST.get('cortisol')
        vit_d = request.POST.get('vit_d')
        ferritin = request.POST.get('ferritin')
        d_dimer = request.POST.get('d_dimer')
        b_hcg = request.POST.get('b_hcg')
        troponin_i = request.POST.get('troponin_i')
        troponin_t = request.POST.get('troponin_t')
        amh = request.POST.get('amh')
        psa = request.POST.get('psa')
        cea = request.POST.get('cea')
        afp = request.POST.get('afp')
        toxo_igg_igm = request.POST.get('toxo_igg_igm')

        if hba1c or tsh or ft4 or t4 or t3 or lh or fsh or prolactin or testosterone or cortisol or \
           vit_d or ferritin or d_dimer or b_hcg or troponin_i or troponin_t or amh or psa or \
           cea or afp or toxo_igg_igm:

            hormones = Hormones.objects.create(recorder=user.arabic_name, patient_id=patient_id)

            if hba1c:
                hormones.hba1c = hba1c
            if tsh:
                hormones.tsh = tsh
            if ft4:
                hormones.ft4 = ft4
            if t4:
                hormones.t4 = t4
            if t3:
                hormones.t3 = t3
            if lh:
                hormones.lh = lh
            if fsh:
                hormones.fsh = fsh
            if prolactin:
                hormones.prolactin = prolactin
            if testosterone:
                hormones.testosterone = testosterone
            if cortisol:
                hormones.cortisol = cortisol
            if vit_d:
                hormones.vit_d = vit_d
            if ferritin:
                hormones.ferritin = ferritin
            if d_dimer:
                hormones.d_dimer = d_dimer
            if b_hcg:
                hormones.b_hcg = b_hcg
            if troponin_i:
                hormones.troponin_i = troponin_i
            if troponin_t:
                hormones.troponin_t = troponin_t
            if amh:
                hormones.amh = amh
            if psa:
                hormones.psa = psa
            if cea:
                hormones.cea = cea
            if afp:
                hormones.afp = afp
            if toxo_igg_igm:
                hormones.toxo_igg_igm = toxo_igg_igm

            hormones.save()

            # 标记已完成化验单
            patient = PatientInfo.objects.get(id=patient_id)
            patient.haveLaboratoryTest = 2
            patient.save()

            url = reverse('laboratory', args=(patient_id, patient_num))

            return redirect(url)

        else:

            message = 'Please input data !'

            url = reverse('laboratory', args=(patient_id, patient_num))

            return redirect(url, locals())


@login_required
def edit_cbc(request, laboratory_id, patient_id, patient_num):

    # 当前需要的信息
    cbc = CBC.objects.get(id=laboratory_id)
    user = User.objects.get(name=request.session['name'])

    if request.method == "POST":
        rbc = request.POST.get('rbc')
        mcv = request.POST.get('mcv')
        mch = request.POST.get('mch')
        mchc = request.POST.get('mchc')
        rdw = request.POST.get('rdw')
        bloodGroup = request.POST.get('bloodGroup')
        hemoglobin = request.POST.get('hemoglobin')
        hematocrite = request.POST.get('hematocrite')
        wbc = request.POST.get('wbc')
        gran = request.POST.get('gran')
        lym = request.POST.get('lym')
        mid = request.POST.get('mid')
        plt = request.POST.get('plt')
        esrH1 = request.POST.get('esrH1')
        esrH2 = request.POST.get('esrH2')

        if rbc or mcv or mch or mchc or rdw or bloodGroup or hemoglobin or hematocrite or wbc or gran or lym or mid or plt or esrH1 or esrH2:

            if rbc:
                cbc.rbc = rbc
            else:
                cbc.rbc = None
            if mcv:
                cbc.mcv = mcv
            else:
                cbc.mcv = None
            if mch:
                cbc.mch = mch
            else:
                cbc.mch = None
            if mchc:
                cbc.mchc = mchc
            else:
                cbc.mchc = None
            if rdw:
                cbc.rdw = rdw
            else:
                cbc.rdw = None
            if bloodGroup:
                cbc.bloodGroup = bloodGroup
            else:
                cbc.bloodGroup = None
            if hemoglobin:
                cbc.hemoglobin = hemoglobin
            else:
                cbc.hemoglobin = None
            if hematocrite:
                cbc.hematocrite = hematocrite
            else:
                cbc.hematocrite = None
            if wbc:
                cbc.wbc = wbc
            else:
                cbc.wbc = None
            if gran:
                cbc.gran = gran
            else:
                cbc.gran = None
            if lym:
                cbc.lym = lym
            else:
                cbc.lym = None
            if mid:
                cbc.mid = mid
            else:
                cbc.mid = None
            if plt:
                cbc.plt = plt
            else:
                cbc.plt = None
            if esrH1:
                cbc.esrH1 = esrH1
            else:
                cbc.esrH1 = None
            if esrH2:
                cbc.esrH2 = esrH2
            else:
                cbc.esrH2 = None

            cbc.recorder = user.arabic_name
            cbc.save()

            url = reverse('results', args=(patient_id, patient_num))

            return redirect(url)

        else:

            message = 'Please input data !'

            return render(request, 'laboratory/results.html', locals())


@login_required
def edit_coagulation(request, laboratory_id, patient_id, patient_num):

    # 当前需要的信息
    coagulation = Coagulation.objects.get(id=laboratory_id)
    user = User.objects.get(name=request.session['name'])

    if request.method == "POST":
        pt = request.POST.get('pt')
        inr = request.POST.get('inr')
        aptt = request.POST.get('aptt')
        bleedTime = request.POST.get('bleedTime')
        clotTime = request.POST.get('clotTime')
        act = request.POST.get('act')

        if pt or inr or aptt or bleedTime or clotTime or act:

            if pt:
                coagulation.pt = pt
            else:
                coagulation.pt = None
            if inr:
                coagulation.inr = inr
            else:
                coagulation.inr = None
            if aptt:
                coagulation.aptt = aptt
            else:
                coagulation.aptt = None
            if bleedTime:
                coagulation.bleedTime = bleedTime
            else:
                coagulation.bleedTime = None
            if clotTime:
                coagulation.clotTime = clotTime
            else:
                coagulation.clotTime = None
            if act:
                coagulation.act = act
            else:
                coagulation.act = None

            coagulation.recorder = user.arabic_name
            coagulation.save()

            url = reverse('results', args=(patient_id, patient_num))

            return redirect(url)

        else:

            message = 'Please input data !'

            return render(request, 'laboratory/results.html', locals())


@login_required
def edit_biochemistry(request, laboratory_id, patient_id, patient_num):

    # 当前需要的信息
    biochemistry = Biochemistry.objects.get(id=laboratory_id)
    user = User.objects.get(name=request.session['name'])

    if request.method == "POST":
        glucose = request.POST.get('glucose')
        urea = request.POST.get('urea')
        creatine = request.POST.get('creatine')
        sgpt = request.POST.get('sgpt')
        sgot = request.POST.get('sgot')
        biliTotal = request.POST.get('biliTotal')
        biliDirect = request.POST.get('biliDirect')
        biliIndirect = request.POST.get('biliIndirect')
        alp = request.POST.get('alp')
        amylase = request.POST.get('amylase')
        ldh = request.POST.get('ldh')
        albumin = request.POST.get('albumin')
        totalProtein = request.POST.get('totalProtein')
        ck = request.POST.get('ck')
        ck_mb = request.POST.get('ck_mb')
        lipase = request.POST.get('lipase')
        uric_acid = request.POST.get('uric_acid')
        triglycerid = request.POST.get('triglycerid')
        cholesterol = request.POST.get('cholesterol')
        crp = request.POST.get('crp')
        aslo = request.POST.get('aslo')
        rf = request.POST.get('rf')

        if glucose or urea or creatine or sgpt or sgot or biliTotal or biliDirect or \
                biliIndirect or alp or amylase or ldh or albumin or totalProtein or ck or \
                ck_mb or lipase or uric_acid or triglycerid or cholesterol or crp or aslo or rf:

            if glucose:
                biochemistry.glucose = glucose
            else:
                biochemistry.glucose = None
            if urea:
                biochemistry.urea = urea
            else:
                biochemistry.urea = None
            if creatine:
                biochemistry.creatine = creatine
            else:
                biochemistry.creatine = None
            if sgpt:
                biochemistry.sgpt = sgpt
            else:
                biochemistry.sgpt = None
            if sgot:
                biochemistry.sgot = sgot
            else:
                biochemistry.sgot = None
            if biliTotal:
                biochemistry.biliTotal = biliTotal
            else:
                biochemistry.biliTotal = None
            if biliDirect:
                biochemistry.biliDirect = biliDirect
            else:
                biochemistry.biliDirect = None
            if biliIndirect:
                biochemistry.biliIndirect = biliIndirect
            else:
                biochemistry.biliIndirect = None
            if alp:
                biochemistry.alp = alp
            else:
                biochemistry.alp = None
            if amylase:
                biochemistry.amylase = amylase
            else:
                biochemistry.amylase = None
            if ldh:
                biochemistry.ldh = ldh
            else:
                biochemistry.ldh = None
            if albumin:
                biochemistry.albumin = albumin
            else:
                biochemistry.albumin = None
            if totalProtein:
                biochemistry.totalProtein = totalProtein
            else:
                biochemistry.totalProtein = None
            if ck:
                biochemistry.ck = ck
            else:
                biochemistry.ck = None
            if ck_mb:
                biochemistry.ck_mb = ck_mb
            else:
                biochemistry.ck_mb = None
            if lipase:
                biochemistry.lipase = lipase
            else:
                biochemistry.lipase = None
            if uric_acid:
                biochemistry.uric_acid = uric_acid
            else:
                biochemistry.uric_acid = None
            if triglycerid:
                biochemistry.triglycerid = triglycerid
            else:
                biochemistry.triglycerid = None
            if cholesterol:
                biochemistry.cholesterol = cholesterol
            else:
                biochemistry.cholesterol = None
            if crp:
                biochemistry.crp = crp
            else:
                biochemistry.crp = None
            if aslo:
                biochemistry.aslo = aslo
            else:
                biochemistry.aslo = None
            if rf:
                biochemistry.rf = rf
            else:
                biochemistry.rf = None

            biochemistry.recorder = user.arabic_name
            biochemistry.save()

            url = reverse('results', args=(patient_id, patient_num))

            return redirect(url)

        else:

            message = 'Please input data !'

            return render(request, 'laboratory/results.html', locals())


@login_required
def edit_electrolytes(request, laboratory_id, patient_id, patient_num):

    # 当前需要的信息
    electrolytes = Electrolytes.objects.get(id=laboratory_id)
    user = User.objects.get(name=request.session['name'])

    if request.method == "POST":
        na = request.POST.get('na')
        k = request.POST.get('k')
        cl = request.POST.get('cl')
        tca = request.POST.get('tca')
        nca = request.POST.get('nca')
        ica = request.POST.get('ica')
        iron = request.POST.get('iron')
        mg = request.POST.get('mg')
        phosphorus = request.POST.get('phosphorus')

        if na or k or cl or tca or nca or ica or iron or mg or phosphorus:

            if na:
                electrolytes.na = na
            else:
                electrolytes.na = None
            if k:
                electrolytes.k = k
            else:
                electrolytes.k = None
            if cl:
                electrolytes.cl = cl
            else:
                electrolytes.cl = None
            if tca:
                electrolytes.tca = tca
            else:
                electrolytes.tca = None
            if nca:
                electrolytes.nca = nca
            else:
                electrolytes.nca = None
            if ica:
                electrolytes.ica = ica
            else:
                electrolytes.ica = None
            if iron:
                electrolytes.iron = iron
            else:
                electrolytes.iron = None
            if mg:
                electrolytes.mg = mg
            else:
                electrolytes.mg = None
            if phosphorus:
                electrolytes.phosphorus = phosphorus
            else:
                electrolytes.phosphorus = None

            electrolytes.recorder = user.arabic_name
            electrolytes.save()

            url = reverse('results', args=(patient_id, patient_num))

            return redirect(url)

        else:

            message = 'Please input data !'

            return render(request, 'laboratory/results.html', locals())


@login_required
def edit_abg(request, laboratory_id, patient_id, patient_num):

    # 当前需要的信息
    abg = ABG.objects.get(id=laboratory_id)
    user = User.objects.get(name=request.session['name'])

    if request.method == "POST":
        ph = request.POST.get('ph')
        pc02 = request.POST.get('pc02')
        p02 = request.POST.get('p02')
        na = request.POST.get('na')
        k = request.POST.get('k')
        ca1 = request.POST.get('ca1')
        glucose = request.POST.get('glucose')
        lac = request.POST.get('lac')
        hc03 = request.POST.get('hc03')
        beecf = request.POST.get('beecf')
        s02c = request.POST.get('s02c')
        fi02 = request.POST.get('fi02')

        if ph or pc02 or p02 or na or k or ca1 or glucose or lac or hc03 or beecf or s02c or fi02:

            if ph:
                abg.ph = ph
            else:
                abg.ph = None
            if pc02:
                abg.pc02 = pc02
            else:
                abg.pc02 = None
            if p02:
                abg.p02 = p02
            else:
                abg.p02 = None
            if na:
                abg.na = na
            else:
                abg.na = None
            if k:
                abg.k = k
            else:
                abg.k = None
            if ca1:
                abg.ca1 = ca1
            else:
                abg.ca1 = None
            if glucose:
                abg.glucose = glucose
            else:
                abg.glucose = None
            if lac:
                abg.lac = lac
            else:
                abg.lac = None
            if hc03:
                abg.hc03 = hc03
            else:
                abg.hc03 = None
            if beecf:
                abg.beecf = beecf
            else:
                abg.beecf = None
            if s02c:
                abg.s02c = s02c
            else:
                abg.s02c = None
            if fi02:
                abg.fi02 = fi02
            else:
                abg.fi02 = None

            abg.recorder = user.arabic_name
            abg.save()

            url = reverse('results', args=(patient_id, patient_num))

            return redirect(url)

        else:

            message = 'Please input data !'

            return render(request, 'laboratory/results.html', locals())


@login_required
def edit_serology(request, laboratory_id, patient_id, patient_num):

    # 当前需要的信息
    serology = Serology.objects.get(id=laboratory_id)
    user = User.objects.get(name=request.session['name'])

    if request.method == "POST":
        hbs_Ag = request.POST.get('hbs_Ag')
        hiv = request.POST.get('hiv')
        hcv = request.POST.get('hcv')
        hcg = request.POST.get('hcg')
        fob = request.POST.get('fob')
        widal_o = request.POST.get('widal_o')
        widal_h = request.POST.get('widal_h')
        wrigh_a = request.POST.get('wrigh_a')
        wrigh_b = request.POST.get('wrigh_b')

        if hbs_Ag or hiv or hcv or hcg or fob or widal_o or widal_h or wrigh_a or wrigh_b:

            if hbs_Ag:
                serology.hbs_Ag = hbs_Ag
            else:
                serology.hbs_Ag = None
            if hiv:
                serology.hiv = hiv
            else:
                serology.hiv = None
            if hcv:
                serology.hcv = hcv
            else:
                serology.hcv = None
            if hcg:
                serology.hcg = hcg
            else:
                serology.hcg = None
            if fob:
                serology.fob = fob
            else:
                serology.fob = None
            if widal_o:
                serology.widal_o = widal_o
            else:
                serology.widal_o = None
            if widal_h:
                serology.widal_h = widal_h
            else:
                serology.widal_h = None
            if wrigh_a:
                serology.wrigh_a = wrigh_a
            else:
                serology.wrigh_a = None
            if wrigh_b:
                serology.wrigh_b = wrigh_b
            else:
                serology.wrigh_b = None

            serology.recorder = user.arabic_name
            serology.save()

            url = reverse('results', args=(patient_id, patient_num))

            return redirect(url)

        else:

            message = 'Please input data !'

            return render(request, 'laboratory/results.html', locals())


@login_required
def edit_urineAnalysis(request, laboratory_id, patient_id, patient_num):

    # 当前需要的信息
    urineAnalysis = UrineAnalysis.objects.get(id=laboratory_id)
    user = User.objects.get(name=request.session['name'])

    if request.method == "POST":
        color = request.POST.get('color')
        spGravity = request.POST.get('spGravity')
        netrit = request.POST.get('netrit')
        wbc = request.POST.get('wbc')
        urates = request.POST.get('urates')
        uric_acid = request.POST.get('uric_acid')
        appearance = request.POST.get('appearance')
        glucose = request.POST.get('glucose')
        keton = request.POST.get('keton')
        rbc = request.POST.get('rbc')
        bacteria = request.POST.get('bacteria')
        mucus = request.POST.get('mucus')
        ph = request.POST.get('ph')
        blood = request.POST.get('blood')
        protein = request.POST.get('protein')
        epCells = request.POST.get('epCells')
        ox_calcium = request.POST.get('ox_calcium')
        casts = request.POST.get('casts')
        fungi = request.POST.get('fungi')
        yeast = request.POST.get('yeast')
        pus_cell = request.POST.get('pus_cell')
        triple_phospate = request.POST.get('triple_phospate')

        if color or spGravity or netrit or wbc or urates or uric_acid or appearance or glucose or \
           keton or rbc or bacteria or mucus or ph or blood or protein or epCells or ox_calcium or \
            casts or fungi or yeast or pus_cell or triple_phospate:

            if color:
                urineAnalysis.color = color
            else:
                urineAnalysis.color = None
            if spGravity:
                urineAnalysis.spGravity = spGravity
            else:
                urineAnalysis.spGravity = None
            if netrit:
                urineAnalysis.netrit = netrit
            else:
                urineAnalysis.netrit = None
            if wbc:
                urineAnalysis.wbc = wbc
            else:
                urineAnalysis.wbc = None
            if urates:
                urineAnalysis.urates = urates
            else:
                urineAnalysis.urates = None
            if uric_acid:
                urineAnalysis.uric_acid = uric_acid
            else:
                urineAnalysis.uric_acid = None
            if appearance:
                urineAnalysis.appearance = appearance
            else:
                urineAnalysis.appearance = None
            if glucose:
                urineAnalysis.glucose = glucose
            else:
                urineAnalysis.glucose = None
            if keton:
                urineAnalysis.keton = keton
            else:
                urineAnalysis.keton = None
            if rbc:
                urineAnalysis.rbc = rbc
            else:
                urineAnalysis.rbc = None
            if bacteria:
                urineAnalysis.bacteria = bacteria
            else:
                urineAnalysis.bacteria = None
            if mucus:
                urineAnalysis.mucus = mucus
            else:
                urineAnalysis.mucus = None
            if ph:
                urineAnalysis.ph = ph
            else:
                urineAnalysis.ph = None
            if blood:
                urineAnalysis.blood = blood
            else:
                urineAnalysis.blood = None
            if protein:
                urineAnalysis.protein = protein
            else:
                urineAnalysis.protein = None
            if epCells:
                urineAnalysis.epCells = epCells
            else:
                urineAnalysis.epCells = None
            if ox_calcium:
                urineAnalysis.ox_calcium = ox_calcium
            else:
                urineAnalysis.ox_calcium = None
            if casts:
                urineAnalysis.casts = casts
            else:
                urineAnalysis.casts = None
            if fungi:
                urineAnalysis.fungi = fungi
            else:
                urineAnalysis.fungi = None
            if yeast:
                urineAnalysis.yeast = yeast
            else:
                urineAnalysis.yeast = None
            if pus_cell:
                urineAnalysis.pus_cell = pus_cell
            else:
                urineAnalysis.pus_cell = None
            if triple_phospate:
                urineAnalysis.triple_phospate = triple_phospate
            else:
                urineAnalysis.triple_phospate = None

            urineAnalysis.recorder = user.arabic_name
            urineAnalysis.save()

            url = reverse('results', args=(patient_id, patient_num))

            return redirect(url)

        else:

            message = 'Please input data !'

            return render(request, 'laboratory/results.html', locals())


@login_required
def edit_csf(request, laboratory_id, patient_id, patient_num):

    csf = CSF.objects.get(id=laboratory_id)
    user = User.objects.get(name=request.session['name'])

    if request.method == "POST":
        color = request.POST.get('color')
        appearance = request.POST.get('appearance')
        rbc = request.POST.get('rbc')
        wbc = request.POST.get('wbc')
        glucose = request.POST.get('glucose')
        protein = request.POST.get('protein')

        if color or appearance or rbc or wbc or glucose or protein:
            if color:
                csf.color = color
            else:
                csf.color = None
            if appearance:
                csf.appearance = appearance
            else:
                csf.appearance = None
            if rbc:
                csf.rbc = rbc
            else:
                csf.rbc = None
            if wbc:
                csf.wbc = wbc
            else:
                csf.wbc = None
            if glucose:
                csf.glucose = glucose
            else:
                csf.glucose = None
            if protein:
                csf.protein = protein
            else:
                csf.protein = None

            csf.recorder = user.arabic_name
            csf.save()

            url = reverse('results', args=(patient_id, patient_num))

            return redirect(url)

        else:
            message = 'Please input data !'

            return render(request, 'laboratory/results.html', locals())


@login_required
def edit_antibiotics(request, laboratory_id, patient_id, patient_num):

    # 当前需要的信息
    antibiotics = Antibiotics.objects.get(id=laboratory_id)
    user = User.objects.get(name=request.session['name'])

    if request.method == "POST":
        cephradine = request.POST.get('cephradine')
        ciprofloxacin = request.POST.get('ciprofloxacin')
        gentamicin = request.POST.get('gentamicin')
        nitrofurantoin = request.POST.get('nitrofurantoin')
        ofloxacin = request.POST.get('ofloxacin')
        cefoxitin = request.POST.get('cefoxitin')
        cefaclor = request.POST.get('cefaclor')
        amikacin = request.POST.get('amikacin')
        ceftriaxone = request.POST.get('ceftriaxone')
        amoxicillin_clavulanic_acid = request.POST.get('amoxicillin_clavulanic_acid')
        cefadroxil = request.POST.get('cefadroxil')
        cefixime = request.POST.get('cefixime')
        cefotaxime = request.POST.get('cefotaxime')
        cefuroxime = request.POST.get('cefuroxime')
        imipenem = request.POST.get('imipenem')
        ampicillin_sulbactam = request.POST.get('ampicillin_sulbactam')
        amoxicillin = request.POST.get('amoxicillin')
        azithromycin = request.POST.get('azithromycin')
        levofloxacin = request.POST.get('levofloxacin')
        neomycin = request.POST.get('neomycin')
        doxycycline = request.POST.get('doxycycline')
        pipemidic_acid = request.POST.get('pipemidic_acid')
        meropenem = request.POST.get('meropenem')
        cloxacillin = request.POST.get('cloxacillin')
        trimethoprim_sulphamethoxazole = request.POST.get('trimethoprim_sulphamethoxazole')
        norfloxacin = request.POST.get('norfloxacin')

        if cephradine or ciprofloxacin or gentamicin or nitrofurantoin or ofloxacin or cefoxitin or \
                cefaclor or amikacin or ceftriaxone or amoxicillin_clavulanic_acid or cefadroxil or \
                cefixime or cefotaxime or cefuroxime or imipenem or ampicillin_sulbactam or amoxicillin or \
                azithromycin or levofloxacin or neomycin or doxycycline or pipemidic_acid or meropenem or \
                cloxacillin or trimethoprim_sulphamethoxazole or norfloxacin:

            if cephradine:
                antibiotics.cephradine = cephradine
            else:
                antibiotics.cephradine = None
            if ciprofloxacin:
                antibiotics.ciprofloxacin = ciprofloxacin
            else:
                antibiotics.ciprofloxacin = None
            if gentamicin:
                antibiotics.gentamicin = gentamicin
            else:
                antibiotics.gentamicin = None
            if nitrofurantoin:
                antibiotics.nitrofurantoin = nitrofurantoin
            else:
                antibiotics.nitrofurantoin = None
            if ofloxacin:
                antibiotics.ofloxacin = ofloxacin
            else:
                antibiotics.ofloxacin = None
            if cefoxitin:
                antibiotics.cefoxitin = cefoxitin
            else:
                antibiotics.cefoxitin = None
            if cefaclor:
                antibiotics.cefaclor = cefaclor
            else:
                antibiotics.cefaclor = None
            if amikacin:
                antibiotics.amikacin = amikacin
            else:
                antibiotics.amikacin = None
            if ceftriaxone:
                antibiotics.ceftriaxone = ceftriaxone
            else:
                antibiotics.ceftriaxone = None
            if amoxicillin_clavulanic_acid:
                antibiotics.amoxicillin_clavulanic_acid = amoxicillin_clavulanic_acid
            else:
                antibiotics.amoxicillin_clavulanic_acid = None
            if cefadroxil:
                antibiotics.cefadroxil = cefadroxil
            else:
                antibiotics.cefadroxil = None
            if cefixime:
                antibiotics.cefixime = cefixime
            else:
                antibiotics.cefixime = None
            if cefotaxime:
                antibiotics.cefotaxime = cefotaxime
            else:
                antibiotics.cefotaxime = None
            if cefuroxime:
                antibiotics.cefuroxime = cefuroxime
            else:
                antibiotics.cefuroxime = None
            if imipenem:
                antibiotics.imipenem = imipenem
            else:
                antibiotics.imipenem = None
            if ampicillin_sulbactam:
                antibiotics.ampicillin_sulbactam = ampicillin_sulbactam
            else:
                antibiotics.ampicillin_sulbactam = None
            if amoxicillin:
                antibiotics.amoxicillin = amoxicillin
            else:
                antibiotics.amoxicillin = None
            if azithromycin:
                antibiotics.azithromycin = azithromycin
            else:
                antibiotics.azithromycin = None
            if levofloxacin:
                antibiotics.levofloxacin = levofloxacin
            else:
                antibiotics.levofloxacin = None
            if neomycin:
                antibiotics.neomycin = neomycin
            else:
                antibiotics.neomycin = None
            if doxycycline:
                antibiotics.doxycycline = doxycycline
            else:
                antibiotics.doxycycline = None
            if pipemidic_acid:
                antibiotics.pipemidic_acid = pipemidic_acid
            else:
                antibiotics.pipemidic_acid = None
            if meropenem:
                antibiotics.meropenem = meropenem
            else:
                antibiotics.meropenem = None
            if cloxacillin:
                antibiotics.cloxacillin = cloxacillin
            else:
                antibiotics.cloxacillin = None
            if trimethoprim_sulphamethoxazole:
                antibiotics.trimethoprim_sulphamethoxazole = trimethoprim_sulphamethoxazole
            else:
                antibiotics.trimethoprim_sulphamethoxazole = None
            if norfloxacin:
                antibiotics.norfloxacin = norfloxacin
            else:
                antibiotics.norfloxacin = None

            antibiotics.recorder = user.arabic_name
            antibiotics.save()

            url = reverse('results', args=(patient_id, patient_num))

            return redirect(url)

        else:

            message = 'Please input data !'

            return render(request, 'laboratory/results.html', locals())


@login_required
def edit_hormones(request, laboratory_id, patient_id, patient_num):

    # 当前需要的信息
    hormones = Hormones.objects.get(id=laboratory_id)
    user = User.objects.get(name=request.session['name'])

    if request.method == "POST":
        hba1c = request.POST.get('hba1c')
        tsh = request.POST.get('tsh')
        ft4 = request.POST.get('ft4')
        t4 = request.POST.get('t4')
        t3 = request.POST.get('t3')
        lh = request.POST.get('lh')
        fsh = request.POST.get('fsh')
        prolactin = request.POST.get('prolactin')
        testosterone = request.POST.get('testosterone')
        cortisol = request.POST.get('cortisol')
        vit_d = request.POST.get('vit_d')
        ferritin = request.POST.get('ferritin')
        d_dimer = request.POST.get('d_dimer')
        b_hcg = request.POST.get('b_hcg')
        troponin_i = request.POST.get('troponin_i')
        troponin_t = request.POST.get('troponin_t')
        amh = request.POST.get('amh')
        psa = request.POST.get('psa')
        cea = request.POST.get('cea')
        afp = request.POST.get('afp')
        toxo_igg_igm = request.POST.get('toxo_igg_igm')

        if hba1c or tsh or ft4 or t4 or t3 or lh or fsh or prolactin or testosterone or cortisol or \
           vit_d or ferritin or d_dimer or b_hcg or troponin_i or troponin_t or amh or psa or \
           cea or afp or toxo_igg_igm:

            if hba1c:
                hormones.hba1c = hba1c
            else:
                hormones.hba1c = None
            if tsh:
                hormones.tsh = tsh
            else:
                hormones.tsh = None
            if ft4:
                hormones.ft4 = ft4
            else:
                hormones.ft4 = None
            if t4:
                hormones.t4 = t4
            else:
                hormones.t4 = None
            if t3:
                hormones.t3 = t3
            else:
                hormones.t3 = None
            if lh:
                hormones.lh = lh
            else:
                hormones.lh = None
            if fsh:
                hormones.fsh = fsh
            else:
                hormones.fsh = None
            if prolactin:
                hormones.prolactin = prolactin
            else:
                hormones.prolactin = None
            if testosterone:
                hormones.testosterone = testosterone
            else:
                hormones.testosterone = None
            if cortisol:
                hormones.cortisol = cortisol
            else:
                hormones.cortisol = None
            if vit_d:
                hormones.vit_d = vit_d
            else:
                hormones.vit_d = None
            if ferritin:
                hormones.ferritin = ferritin
            else:
                hormones.ferritin = None
            if d_dimer:
                hormones.d_dimer = d_dimer
            else:
                hormones.d_dimer = None
            if b_hcg:
                hormones.b_hcg = b_hcg
            else:
                hormones.b_hcg = None
            if troponin_i:
                hormones.troponin_i = troponin_i
            else:
                hormones.troponin_i = None
            if troponin_t:
                hormones.troponin_t = troponin_t
            else:
                hormones.troponin_t = None
            if amh:
                hormones.amh = amh
            else:
                hormones.amh = None
            if psa:
                hormones.psa = psa
            else:
                hormones.psa = None
            if cea:
                hormones.cea = cea
            else:
                hormones.cea = None
            if afp:
                hormones.afp = afp
            else:
                hormones.afp = None
            if toxo_igg_igm:
                hormones.toxo_igg_igm = toxo_igg_igm
            else:
                hormones.toxo_igg_igm = None

            hormones.recorder = user.arabic_name
            hormones.save()

            url = reverse('results', args=(patient_id, patient_num))

            return redirect(url)

        else:

            message = 'Please input data !'

            return render(request, 'laboratory/results.html', locals())


@login_required
def results(request, patient_id, patient_num):

    # 当前需要的信息
    patient = PatientInfo.objects.all().get(id=patient_id)
    user = User.objects.all().get(name=request.session['name'])

    # 病房
    wards = user.authorityWard.filter(status=True)

    bloodTypes = ['', 'A: Neg-', 'A: Pos+', 'B: Neg-', 'B: Pos+',
                  'AB:Neg-', 'AB:Pos+', 'O: Neg-', 'O: Pos+']

    colors = ['', 'Yellow', 'Dp Yellow', 'Lt Yellow', 'Red', 'Black', 'Brown', 'Green']

    cbcObj = CBC.objects.filter(patient_id=patient_id).order_by('-id')
    coagulationObj = Coagulation.objects.filter(patient_id=patient_id).order_by('-id')
    biochemistryObj = Biochemistry.objects.filter(patient_id=patient_id).order_by('-id')
    electrolytesObj = Electrolytes.objects.filter(patient_id=patient_id).order_by('-id')
    abgObj = ABG.objects.filter(patient_id=patient_id).order_by('-id')
    serologyObj = Serology.objects.filter(patient_id=patient_id).order_by('-id')
    urineAnalysisObj = UrineAnalysis.objects.filter(patient_id=patient_id).order_by('-id')
    csfObj = CSF.objects.filter(patient_id=patient_id).order_by('-id')
    antibioticsObj = Antibiotics.objects.filter(patient_id=patient_id).order_by('-id')
    hormonesObj = Hormones.objects.filter(patient_id=patient_id).order_by('-id')

    return render(request, 'laboratory/results.html', locals())


@login_required
def cancelLaboratory(request, patient_id, laboratory_id, types):

    # 当前需要的信息
    patient = PatientInfo.objects.get(id=patient_id)
    if types == 'CBC':
        cbcObj = CBC.objects.get(id=laboratory_id)
        cbcObj.status = False
        cbcObj.save()

    elif types == 'Coagulation':
        coagulationObj = Coagulation.objects.get(id=laboratory_id)
        coagulationObj.status = False
        coagulationObj.save()

    elif types == 'Biochemistry':
        biochemistryObj = Biochemistry.objects.get(id=laboratory_id)
        biochemistryObj.status = False
        biochemistryObj.save()

    elif types == 'Electrolytes':
        electrolytesObj = Electrolytes.objects.get(id=laboratory_id)
        electrolytesObj.status = False
        electrolytesObj.save()

    elif types == 'ABG':
        abgObj = ABG.objects.get(id=laboratory_id)
        abgObj.status = False
        abgObj.save()

    elif types == 'Serology':
        serologyObj = Serology.objects.get(id=laboratory_id)
        serologyObj.status = False
        serologyObj.save()

    elif types == 'UrineAnalysis':
        urineAnalysisObj = UrineAnalysis.objects.get(id=laboratory_id)
        urineAnalysisObj.status = False
        urineAnalysisObj.save()

    elif types == 'CSF':
        csfObj = CSF.objects.get(id=laboratory_id)
        csfObj.status = False
        csfObj.save()

    elif types == 'Antibiotics':
        antibioticsObj = Antibiotics.objects.get(id=laboratory_id)
        antibioticsObj.status = False
        antibioticsObj.save()

    elif types == 'Hormones':
        hormonesObj = Hormones.objects.get(id=laboratory_id)
        hormonesObj.status = False
        hormonesObj.save()

    url = reverse('results', args=(patient_id, patient.patientID))
    return redirect(url)


@login_required
def confirmLaboratory(request, patient_id, laboratory_id, types):

    # 当前需要的信息
    patient = PatientInfo.objects.get(id=patient_id)
    if types == 'CBC':
        cbcObj = CBC.objects.get(id=laboratory_id)
        cbcObj.status = True
        cbcObj.save()

        url = reverse('results', args=(patient_id, patient.patientID))
        return redirect(url)

    elif types == 'Coagulation':
        coagulationObj = Coagulation.objects.get(id=laboratory_id)
        coagulationObj.status = True
        coagulationObj.save()

        url = reverse('results', args=(patient_id, patient.patientID))
        return redirect(url)

    elif types == 'Biochemistry':
        biochemistryObj = Biochemistry.objects.get(id=laboratory_id)
        biochemistryObj.status = True
        biochemistryObj.save()

        url = reverse('results', args=(patient_id, patient.patientID))
        return redirect(url)

    elif types == 'Electrolytes':
        electrolytesObj = Electrolytes.objects.get(id=laboratory_id)
        electrolytesObj.status = True
        electrolytesObj.save()

        url = reverse('results', args=(patient_id, patient.patientID))
        return redirect(url)

    elif types == 'ABG':
        abgObj = ABG.objects.get(id=laboratory_id)
        abgObj.status = True
        abgObj.save()

        url = reverse('results', args=(patient_id, patient.patientID))
        return redirect(url)

    elif types == 'Serology':
        serologyObj = Serology.objects.get(id=laboratory_id)
        serologyObj.status = True
        serologyObj.save()

        url = reverse('results', args=(patient_id, patient.patientID))
        return redirect(url)

    elif types == 'UrineAnalysis':
        urineAnalysisObj = UrineAnalysis.objects.get(id=laboratory_id)
        urineAnalysisObj.status = True
        urineAnalysisObj.save()

        url = reverse('results', args=(patient_id, patient.patientID))
        return redirect(url)

    elif types == 'CSF':
        csfObj = CSF.objects.get(id=laboratory_id)
        csfObj.status = True
        csfObj.save()

        url = reverse('results', args=(patient_id, patient.patientID))
        return redirect(url)

    elif types == 'Antibiotics':
        antibioticsObj = Antibiotics.objects.get(id=laboratory_id)
        antibioticsObj.status = True
        antibioticsObj.save()

    elif types == 'Hormones':
        hormonesObj = Hormones.objects.get(id=laboratory_id)
        hormonesObj.status = True
        hormonesObj.save()

        url = reverse('results', args=(patient_id, patient.patientID))
        return redirect(url)


@login_required
def dateSearchMoneyLaboratory(request):

    # 当前需要的信息
    user = User.objects.all().get(name=request.session['name'])

    # 病房
    wards = user.authorityWard.filter(status=True)

    if request.method == "POST":
        start = request.POST.get('start')
        end = request.POST.get('end')

        date = (start, end)

        patients = PatientInfo.objects.filter(enterDate__range=date, condition=99).order_by('-id')

        return render(request, 'laboratory/moneyLaboratory.html', locals())


@login_required
def moneyLaboratory(request):

    user = User.objects.get(name=request.session['name'])

    genders = ['', 'ذكر', 'أنثى']

    today = datetime.today().date()

    # 统计病房病人
    wards = user.authorityWard.filter(status=True)
    countOfTotal = wards.aggregate(Sum('count'))['count__sum']

    patients = PatientInfo.objects.filter(enterDate__gte=today, condition=99).order_by('-id')

    return render(request, 'laboratory/moneyLaboratory.html', locals())


@login_required
def addMoneyLaboratoryPatient(request):
    """添加病人基本信息"""

    user = User.objects.get(name=request.session['name'])

    if request.method == 'POST':
        name = request.POST.get('name').title()
        age = request.POST.get('age')
        sex = request.POST.get('sex')

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

        numberID = IDCreator()

        basicInfo = BasicInfo.objects.create(name=name, birthday=birthday, sex=sex,
                                             age=tempAge, operator=user.name)

        patient = PatientInfo.objects.create(basicInfo=basicInfo, patientID=numberID,
                                             condition=99, operator=user.name)

        url = reverse('moneyLaboratory')
        return redirect(url)


@login_required
def displayMoneyLaboratoryPrint(request, patient_id, patient_num):

    user = User.objects.get(name=request.session['name'])

    patient = PatientInfo.objects.get(id=patient_id)
    # 统计病房病人
    wards = user.authorityWard.filter(status=True)
    countOfTotal = wards.aggregate(Sum('count'))['count__sum']

    cbcObj = CBC.objects.filter(patient_id=patient_id, status=True).order_by('id')
    for cbc in cbcObj:
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

    coagulationObj = Coagulation.objects.filter(patient_id=patient_id, status=True).order_by('id')
    for coagulation in coagulationObj:
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

    biochemistryObj = Biochemistry.objects.filter(patient_id=patient_id, status=True).order_by('id')
    for biochemistry in biochemistryObj:
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

    electrolytesObj = Electrolytes.objects.filter(patient_id=patient_id, status=True).order_by('id')
    for electrolytes in electrolytesObj:
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

    abgObj = ABG.objects.filter(patient_id=patient_id, status=True).order_by('id')
    for abg in abgObj:
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

    serologyObj = Serology.objects.filter(patient_id=patient_id, status=True).order_by('id')
    for serology in serologyObj:
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

    urineAnalysisObj = UrineAnalysis.objects.filter(patient_id=patient_id, status=True).order_by('id')
    for urineAnalysis in urineAnalysisObj:
        if urineAnalysis.color:
            color = urineAnalysis.color
        if urineAnalysis.spGravity:
            spGravity = urineAnalysis.spGravity
        if urineAnalysis.netrit:
            netrit = urineAnalysis.netrit
        if urineAnalysis.wbc:
            wbc = urineAnalysis.wbc
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

    csfObj = CSF.objects.filter(patient_id=patient_id, status=True).order_by('id')
    for csf in csfObj:
        if csf.color:
            color = csf.color
        if csf.appearance:
            appearance = csf.appearance
        if csf.rbc:
            rbc = csf.rbc
        if csf.wbc:
            wbc = csf.wbc
        if csf.glucose:
            glucose = csf.glucose
        if csf.protein:
            protein = csf.protein

    antibioticObj = Antibiotics.objects.filter(patient_id=patient_id, status=True).order_by('id')
    for antibiotic in antibioticObj:
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

    hormonesObj = Hormones.objects.filter(patient_id=patient_id, status=True).order_by('id')
    for hormones in hormonesObj:
        if hormones.hba1c:
            hba1c = hormones.hba1c
        if hormones.tsh:
            tsh = hormones.tsh
        if hormones.ft4:
            ft4 = hormones.ft4
        if hormones.t4:
            t4 = hormones.t4
        if hormones.t3:
            t3 = hormones.t3
        if hormones.lh:
            lh = hormones.lh
        if hormones.fsh:
            fsh = hormones.fsh
        if hormones.prolactin:
            prolactin = hormones.prolactin
        if hormones.testosterone:
            testosterone = hormones.testosterone
        if hormones.cortisol:
            cortisol = hormones.cortisol
        if hormones.vit_d:
            vit_d = hormones.vit_d
        if hormones.ferritin:
            ferritin = hormones.ferritin
        if hormones.d_dimer:
            d_dimer = hormones.d_dimer
        if hormones.b_hcg:
            b_hcg = hormones.b_hcg
        if hormones.troponin_i:
            troponin_i = hormones.troponin_i
        if hormones.troponin_t:
            troponin_t = hormones.troponin_t
        if hormones.amh:
            amh = hormones.amh
        if hormones.psa:
            psa = hormones.psa
        if hormones.cea:
            cea = hormones.cea
        if hormones.afp:
            afp = hormones.afp
        if hormones.toxo_igg_igm:
            toxo_igg_igm = hormones.toxo_igg_igm

    return render(request, 'laboratory/displayMoneyLaboratoryPrint.html', locals())
