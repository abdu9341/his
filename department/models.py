from django.db import models


class Department(models.Model):
    """科室信息表"""

    name = models.CharField(max_length=25, unique=True)
    arabic_name = models.CharField(max_length=35, default='', unique=True)
    types = models.SmallIntegerField()  # 类型：1表示临床科室，2表示门诊科室，3表示通用科室，4表示职能科室
    # True表示不显示病房名称，False 表示显示病房名称
    status = models.BooleanField(default=True, null=True, blank=True)
    count = models.SmallIntegerField(default=0, null=True, blank=True)  # 该科室的病人数量

    def __str__(self):
        return self.name


class Ward(models.Model):
    """病房表"""

    name = models.CharField(max_length=25, unique=True)
    arabic_name = models.CharField(max_length=35, default='', unique=True)
    # True表示显示病房名称，False 表示不显示病房名称
    status = models.BooleanField(default=True, null=True, blank=True)
    count = models.SmallIntegerField(default=0, null=True, blank=True)  # 该病房的病人数量

    def __str__(self):
        return self.name


class Template(models.Model):
    """模板类别"""

    name = models.CharField(max_length=20, unique=True)
    arabic_name = models.CharField(max_length=35, default='')
    url_name = models.CharField(max_length=35, default='', unique=True)

    def __str__(self):
        return self.name
