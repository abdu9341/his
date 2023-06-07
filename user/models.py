from django.db import models
from department.models import *


class Position(models.Model):
    """职位表"""

    name = models.CharField(max_length=20, unique=True)
    arabic_name = models.CharField(max_length=25, default='', null=True, blank=True)  # 姓名

    def __str__(self):
        return self.name


class User(models.Model):
    """用户信息"""

    name = models.CharField(max_length=35)  # 姓名
    arabic_name = models.CharField(max_length=35, default='', null=True, blank=True)  # 姓名
    account = models.SmallIntegerField(unique=True, null=True, blank=True)
    password = models.CharField(max_length=11)  # 密码
    sex = models.CharField(max_length=6)  # 性别
    position = models.ForeignKey(Position, on_delete=models.DO_NOTHING)  # 职位
    template = models.ManyToManyField(Template, blank=True)  # 要登录的模板
    # 能访问的科室或者病房
    authorityDepartment = models.ForeignKey(Department, on_delete=models.DO_NOTHING)
    authorityWard = models.ManyToManyField(Ward, blank=True)  # 能访问的病房
    # authorityMenu = models.ManyToManyField(Menu, blank=True)  # 能用的菜单
    # 状态， FALSE表示未激活，True表示已激活
    status = models.BooleanField(default=True, null=True, blank=True)
    currentTemplateUrl = models.CharField(max_length=20, default='', null=True, blank=True)
    # 语言： 1 表示阿拉伯语， 2 表示英语
    language = models.SmallIntegerField(default=1, null=True, blank=True)

    def __str__(self):
        return self.name


class Account(models.Model):
    """账户"""

    account = models.IntegerField(default=1, null=True, blank=True)
