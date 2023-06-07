from django.http import JsonResponse
from django.db.models import Sum, Q
from django.shortcuts import render, redirect
from patient.models import PatientInfo
from department.models import *
from user.models import *


def login_required(view_func):
    """登录判断装饰器"""

    def wrapper(request, *view_args, **view_kwargs):

        if request.session.has_key('islogin'):
            # 用户已登录，调用对应视图
            return view_func(request, *view_args, **view_kwargs)
        else:
            # 用户未登录，跳转到登录页
            return redirect('/login')

    return wrapper


def login(request):
    """登录"""

    return render(request, 'user/login.html', locals())


def loginCheck(request):
    """登录校验"""

    if request.method == 'POST':
        account = request.POST.get('account')
        password = request.POST.get('password')
        message = ''

        # 进行效验，返回json数据
        try:
            user = User.objects.get(account=account)

            # 验证用户是否未激活
            if user.status:
                pass

            else:
                message = 'Your account has not been activated !'
                return render(request, 'user/login.html', locals())

        except:
            message = 'Your account is wrong !'
            return render(request, 'user/login.html', locals())

        else:
            if user.password == password:

                name = user.name
                # 记住用户登录状态，只有session中有islogin，就认为用户已登录
                response = redirect('/index')
                request.session['islogin'] = True
                request.session['name'] = name

                return redirect('/' + user.currentTemplateUrl + '/')

            else:
                message = 'Your password is wrong !'
                return render(request, 'user/login.html', locals())


def logout(request):
    request.session.clear()

    return redirect('/login')


@login_required
def changePwdAction(request):
    """修改密码处理"""

    user = User.objects.get(name=request.session['name'])

    # 1. 获取新密码
    if request.method == 'POST':
        pwd = request.POST.get('pwd')
        # 2.更新数据库
        # username = request.COOKIES['username']
        name = request.session['name']
        user = User.objects.get(name=name)
        user.password = pwd
        user.save()

        return redirect('/userProfile/')


@login_required
def userProfile(request):
    """用户资料"""

    user = User.objects.get(name=request.session['name'])

    if user.currentTemplateUrl == 'index':

        # 统计病房病人
        wards = user.authorityWard.filter(status=True)
        countOfTotal = wards.aggregate(Sum('count'))['count__sum']

        # 该用户能访问的病人
        patientsDoctor = PatientInfo.objects.filter(condition=1, department=user.authorityDepartment)
        patientsNurse = PatientInfo.objects.filter(condition=1, sickroom__in=user.authorityWard.all())

        return render(request, 'user/profileHospitalized.html', locals())

    elif user.currentTemplateUrl == 'indexPolyclinic':

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

        # 统计科室的病人
        departments = Department.objects.filter(Q(status=True, types=2) | Q(status=True, types=3))
        countOfTotal = departments.aggregate(Sum('count'))['count__sum']

        return render(request, 'user/profilePolyclinic.html', locals())

    elif user.currentTemplateUrl == 'indexEmergency':

        # 急诊科病人
        emergencyMalePatients = PatientInfo.objects.filter(condition=2, basicInfo__sex='ذكر')
        emergencyFemalePatients = PatientInfo.objects.filter(condition=2, basicInfo__sex='انثى')

        # 急诊科病人数量
        countOfMale = emergencyMalePatients.count()
        countOfFemale = emergencyFemalePatients.count()

        return render(request, 'user/profileEmergency.html', locals())

    elif user.currentTemplateUrl == 'indexLaboratory':

        # 统计病房病人
        wards = user.authorityWard.filter(status=True)
        countOfTotal = wards.aggregate(Sum('count'))['count__sum']

        return render(request, 'user/profileLaboratory.html', locals())

    elif user.currentTemplateUrl == 'indexOperation':

        # 统计病房病人
        wards = user.authorityWard.filter(status=True)
        countOfTotal = wards.aggregate(Sum('count'))['count__sum']

        return render(request, 'user/profileOperation.html', locals())

    elif user.currentTemplateUrl == 'indexBooking':

        # 科室
        departments = Department.objects.filter(Q(status=True, types=2) | Q(status=True, types=3))

        return render(request, 'user/profileOperationBooking.html', locals())

    elif user.currentTemplateUrl == 'indexAdmin':

        return render(request, 'user/profileAdmin.html', locals())


@login_required
def indexAdmin(request):

    user = User.objects.all().get(name=request.session['name'])

    # 更新当前模板内容
    user.currentTemplateUrl = 'indexAdmin'
    user.save()

    return render(request, 'user/indexAdmin.html', locals())


@login_required
def allUsers(request):
    """所有用户"""

    name = request.session['name']
    user = User.objects.get(name=name)

    users = User.objects.filter(account__gt=0).order_by('account')

    positions = Position.objects.all()

    departments = Department.objects.filter(status=True)

    wards = Ward.objects.filter(status=True)

    templates = Template.objects.all()

    # menuCategories = MenuCategory.objects.all()

    # menus = Menu.objects.all()

    return render(request, 'user/allUsers.html', locals())


@login_required
def addUser(request):

    if request.method == 'POST':
        name = request.POST.get('name')
        arabic_name = request.POST.get('arabic_name')
        gender = request.POST.get('gender')
        password = request.POST.get('password')
        position_id = request.POST.get('position')
        department_id = request.POST.get('department')
        template_ids = request.POST.getlist('templates')
        ward_ids = request.POST.getlist('wards')
        # menu_ids = request.POST.getlist('menus')

        # 账号表
        account = Account.objects.first()

        if account:
            pass
        else:
            account = Account.objects.create()

        # 当前模板地址
        currentTemplateUrl = ''

        # 模板
        template_list = []
        for template_id in template_ids:
            template = Template.objects.get(id=template_id)
            template_list.append(template)
            currentTemplateUrl = template.url_name

        # 病房
        ward_list = []
        for ward_id in ward_ids:
            ward_list.append(Ward.objects.get(id=ward_id))

        # 菜单
        # menu_list = []
        # for menu_id in menu_ids:
        #     menu_list.append(Menu.objects.get(id=menu_id))

        if User.objects.filter(name=name):
            message = 'This Account is already exists !'

            return render(request, 'user/allUsers.html', locals())

        else:

            user = User.objects.create(name=name, arabic_name=arabic_name, account=account.account,
                                       password=password, sex=gender, position_id=position_id,
                                       authorityDepartment_id=department_id,
                                       currentTemplateUrl=currentTemplateUrl)

            # 给这个用户添加能访问的模板，病房，菜单
            user.template.add(*template_list)
            user.authorityWard.add(*ward_list)
            # user.authorityMenu.add(*menu_list)

            # 更新当前模板地址
            for template_id in template_ids:
                template = Template.objects.get(id=template_id)
                user.currentTemplateUrl = template.url_name
            user.save()

            # 更新账户号码
            account.account += 1
            account.save()

            return redirect('/allUsers/')


@login_required
def editUser(request, user_id):

    user = User.objects.get(id=user_id)

    if request.method == 'POST':
        name = request.POST.get('name')
        arabic_name = request.POST.get('arabic_name')
        gender = request.POST.get('gender')
        password = request.POST.get('password')
        position_id = request.POST.get('position')
        department_id = request.POST.get('department')
        template_ids = request.POST.getlist('templates')
        ward_ids = request.POST.getlist('wards')
        # menu_ids = request.POST.getlist('menus')

        # 模板
        template_list = []
        for template_id in template_ids:
            template = Template.objects.get(id=template_id)
            template_list.append(template)
            user.currentTemplateUrl = template.url_name
        user.save()

        # 病房
        ward_list = []
        for ward_id in ward_ids:
            ward_list.append(Ward.objects.get(id=ward_id))

        # 菜单
        # menu_list = []
        # for menu_id in menu_ids:
        #     menu_list.append(Menu.objects.get(id=menu_id))

        if User.objects.filter(name=name) and user.name != name:
            message = 'This Account is already exists !'

            return render(request, 'user/allUsers.html', locals())

        else:

            user.name = name
            user.arabic_name = arabic_name
            user.sex = gender
            user.password = password
            user.position_id = position_id
            user.authorityDepartment_id = department_id
            user.save()

            # 先清除当前用户的所有模板、病房、菜单，
            user.template.clear()
            user.authorityWard.clear()
            # user.authorityMenu.clear()

            # 再给这个用户添加模板、病房、菜单
            user.template.add(*template_list)
            user.authorityWard.add(*ward_list)
            # user.authorityMenu.add(*menu_list)

            return redirect('/allUsers/')


@login_required
def activeUser(request, user_id):

    user = User.objects.get(id=user_id)

    user.status = True
    user.save()

    return redirect('/allUsers/')


@login_required
def inactiveUser(request, user_id):

    user = User.objects.get(id=user_id)

    user.status = False
    user.save()

    return redirect('/allUsers/')


@login_required
def arabic(request):
    """阿拉伯语"""

    user = User.objects.get(name=request.session['name'])

    user.language = 1
    user.save()

    return redirect(user.currentTemplateUrl)


@login_required
def english(request):
    """英语"""

    user = User.objects.get(name=request.session['name'])

    user.language = 2
    user.save()

    return redirect(user.currentTemplateUrl)


