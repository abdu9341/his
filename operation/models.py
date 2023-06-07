from django.db import models
from patient.models import PatientInfo


class Operation(models.Model):

    patient = models.ForeignKey(PatientInfo, on_delete=models.DO_NOTHING)
    name = models.CharField(max_length=35)  # 手术名称
    doctor = models.CharField(max_length=35)  # 医生名称
    assistant = models.CharField(max_length=35)  # 助手
    surgicalNurse = models.CharField(max_length=20)  # 手术护士
    anesthetist = models.CharField(max_length=35)  # 麻醉师名称
    typesNarcosis = models.CharField(max_length=15)  # 麻醉类型
    typesOperation = models.CharField(max_length=10)  # 手术类型
    roomNo = models.CharField(max_length=20)  # 房号
    begin = models.DateTimeField()  # 手术开始时间
    timeOfOperation = models.SmallIntegerField()  # 手术时间
    recordDate = models.DateTimeField(auto_now_add=True)  # 记录时间
    operator = models.CharField(max_length=35, default='')  # 操作员


class TimeTable(models.Model):
    """医生时间表"""

    doctor = models.CharField(max_length=35)  # 医生名称
    date = models.DateField()  # 手术开始时间


class BookingOperation(models.Model):
    """手术预约"""

    timeTable = models.ForeignKey(TimeTable, on_delete=models.DO_NOTHING)
    patient = models.ForeignKey(PatientInfo, on_delete=models.DO_NOTHING)
    name = models.CharField(max_length=35)  # 手术名称
    # doctor = models.CharField(max_length=35)  # 医生名称
    date = models.DateField()  # 手术开始时间
    timeOfOperation = models.SmallIntegerField(default=1)  # 手术时间, 1表示一个小时
    operator = models.CharField(max_length=35, default='')  # 操作员
    order = models.SmallIntegerField(default=1)  # 手术预定顺序


class OperationDictionary(models.Model):
    """手术名称表"""

    name = models.CharField(max_length=35)  # 手术名称
