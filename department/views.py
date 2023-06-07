from django.http import HttpResponse
from django.shortcuts import render, redirect
from operation.models import *
from user.views import login_required
from django.db.models import Sum, Q
from department.models import *
from user.models import User
from patient.models import PatientInfo


@login_required
def ward(request, ward_id):

    user = User.objects.get(name=request.session['name'])

    wardObj = Ward.objects.get(id=ward_id)

    # 统计病房病人
    wards = user.authorityWard.filter(status=True)
    countOfTotal = wards.aggregate(Sum('count'))['count__sum']

    # 修正病房病人数量
    for ward in wards:
        patienObjs = PatientInfo.objects.filter(sickroom=ward, condition__range=(1, 2))
        ward.count = patienObjs.count()
        ward.save()

    # 该病房的所有病人
    patients = PatientInfo.objects.filter(sickroom_id=ward_id, condition__range=(1, 2)).order_by('-id')

    return render(request, 'department/ward.html', locals())


@login_required
def allWards(request):

    user = User.objects.get(name=request.session['name'])

    wards = Ward.objects.all().order_by('-id')

    return render(request, 'department/allWards.html', locals())


@login_required
def activeWard(request, ward_id):

    wardObj = Ward.objects.get(id=ward_id)

    wardObj.status = True
    wardObj.save()

    return redirect('/allWards/')


@login_required
def inactiveWard(request, ward_id):

    wardObj = Ward.objects.get(id=ward_id)

    wardObj.status = False
    wardObj.save()

    return redirect('/allWards/')


@login_required
def addWard(request):

    wards = Ward.objects.all()

    if request.method == 'POST':
        name = request.POST.get('name')
        arabic_name = request.POST.get('arabic_name')

        if Ward.objects.filter(Q(name=name) | Q(arabic_name=arabic_name)):

            message = 'هذا الجناح موجود !'

            return render(request, 'department/allWards.html', locals())

        else:

            Ward.objects.create(name=name, arabic_name=arabic_name, status=True, count=0)

            return redirect('/allWards/')


@login_required
def editWard(request, ward_id):

    wards = Ward.objects.all()

    wardObj = Ward.objects.get(id=ward_id)

    if request.method == 'POST':
        name = request.POST.get('name')
        arabic_name = request.POST.get('arabic_name')

        try:
            wardObj.name = name
            wardObj.arabic_name = arabic_name
            wardObj.save()

            return redirect('/allWards/')

        except:

            message = 'هذا الجناح موجود !'

            return render(request, 'department/allWards.html', locals())


@login_required
def departmentPolyclinic(request, department_id):

    user = User.objects.get(name=request.session['name'])

    departmentObj = Department.objects.get(id=department_id)

    url = request.get_full_path()  # /department/2   /departmentPolyclinic/

    url_num = "".join(list(filter(str.isdigit, url)))
    url_str = url[1:21]

    departments = Department.objects.filter(Q(status=True, types=2) | Q(status=True, types=3))

    # 自动更新所有科室的病人数量
    for department in departments:
        department.count = PatientInfo.objects.filter(condition__range=(5, 7), department=department).count()
        department.save()

    # 统计科室的病人
    countOfTotal = departments.aggregate(Sum('count'))['count__sum']

    # 该科室的所有病人
    patientsNotArrive = PatientInfo.objects.filter(department=departmentObj,
                                                   condition__range=(5, 7), arrive=False).order_by('arriveDate')

    patientsArrive = PatientInfo.objects.filter(department=departmentObj,
                                                condition__range=(5, 7), arrive=True).order_by('arriveDate')

    return render(request, 'department/departmentPolyclinic.html', locals())


@login_required
def departmentBookingOperation(request, department_id):

    user = User.objects.get(name=request.session['name'])

    departmentObj = Department.objects.get(id=department_id)

    # 该科室的所有病人
    patients = PatientInfo.objects.filter(department=departmentObj, condition__range=(5, 7))

    # 科室病人
    departments = Department.objects.filter(Q(status=True, types=2) | Q(status=True, types=3))

    doctors = User.objects.filter(position__name='Doctor')

    operationNames = OperationDictionary.objects.all()

    return render(request, 'department/departmentBookingOperation.html', locals())


@login_required
def allDepartments(request):

    types_arabic = ['قسم الجناح', 'قسم العيادات', 'قسم العامة', 'قسم الوظيفية']
    types_english = ['hospitalized', 'Clinical', 'Universal', 'Functional']

    user = User.objects.get(name=request.session['name'])

    departments = Department.objects.all().order_by('-id')

    return render(request, 'department/allDepartments.html', locals())


@login_required
def activeDepartment(request, department_id):

    departmentObj = Department.objects.get(id=department_id)

    departmentObj.status = True
    departmentObj.save()

    return redirect('/allDepartments/')


@login_required
def inactiveDepartment(request, department_id):

    departmentObj = Department.objects.get(id=department_id)

    departmentObj.status = False
    departmentObj.save()

    return redirect('/allDepartments/')


@login_required
def addDepartment(request):

    departments = Department.objects.all()

    if request.method == 'POST':
        name = request.POST.get('name')
        arabic_name = request.POST.get('arabic_name')
        types = request.POST.get('types')

        if Department.objects.filter(Q(name=name) | Q(arabic_name=arabic_name)):

            message = 'القسم موجود !'

            return HttpResponse(message)
            # return render(request, 'department/allDepartments.html', locals())

        else:

            Department.objects.create(name=name, arabic_name=arabic_name, types=types)

            return redirect('/allDepartments/')


@login_required
def editDepartment(request, department_id):

    departments = Department.objects.all()

    departmentObj = Department.objects.get(id=department_id)

    if request.method == 'POST':
        name = request.POST.get('name')
        arabic_name = request.POST.get('arabic_name')
        types = request.POST.get('types')

        try:

            departmentObj.name = name
            departmentObj.arabic_name = arabic_name
            departmentObj.types = types
            departmentObj.save()

            return redirect('/allDepartments/')

        except:

            message = 'القسم موجود !'

            return HttpResponse(message)
            # return render(request, 'department/allDepartments.html', locals())


@login_required
def wardLaboratory(request, ward_id):

    user = User.objects.get(name=request.session['name'])

    wardObj = Ward.objects.get(id=ward_id)

    # 统计病房病人
    wards = user.authorityWard.filter(status=True)
    countOfTotal = wards.aggregate(Sum('count'))['count__sum']

    # 该病房的所有病人
    patients = PatientInfo.objects.filter(sickroom_id=ward_id, condition__range=(1, 2)).order_by('-id')

    return render(request, 'department/wardLaboratory.html', locals())


@login_required
def wardOperation(request, ward_id):

    user = User.objects.get(name=request.session['name'])

    wardObj = Ward.objects.get(id=ward_id)

    # 统计病房病人
    wards = user.authorityWard.filter(status=True)
    countOfTotal = wards.aggregate(Sum('count'))['count__sum']

    patients = PatientInfo.objects.filter(sickroom_id=ward_id, condition__range=(1, 2)).order_by('-id')

    doctors = User.objects.filter(position__name='Doctor')
    nurses = User.objects.filter(position__name='Nurse')

    operationNames = OperationDictionary.objects.all()

    return render(request, 'department/wardOperation.html', locals())
