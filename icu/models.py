from django.db import models
from patient.models import PatientInfo


class DatesInICU(models.Model):
    """ICU"""

    objects = models.Manager()
    date = models.DateTimeField(auto_now_add=True, blank=True, null=True)  # 转入ICU日期
    icuPatient = models.ForeignKey(PatientInfo, on_delete=models.CASCADE)  # 关联病人信息


class VitalSigns(models.Model):
    """生命体征"""

    objects = models.Manager()
    pulse = models.IntegerField(blank=True, null=True)  # 脉搏
    bloodPressureMax = models.IntegerField(blank=True, null=True)  # 最高血压  SYS
    bloodPressureMin = models.IntegerField(blank=True, null=True)  # 最低血压 DYS
    bloodPressureAverage = models.IntegerField(blank=True, null=True)  # 平均血压  MAP
    spo2 = models.IntegerField(blank=True, null=True)  # 氧气饱和度
    temperature = models.FloatField(blank=True, null=True)  # 体温
    breathingRate = models.IntegerField(blank=True, null=True)  # 呼吸频率
    urineOutput = models.FloatField(blank=True, null=True)  # 尿液输出量
    oxygen = models.CharField(default='', max_length=7, blank=True, null=True)  # 氧气量
    glucose = models.FloatField(blank=True, null=True)  # 葡萄糖
    frequency = models.IntegerField(blank=True, null=True)  #
    mode = models.CharField(max_length=20, default='', null=True)  #
    vt = models.IntegerField(blank=True, null=True)  #
    fio2 = models.IntegerField(blank=True, null=True)  #
    psv = models.IntegerField(blank=True, null=True)  #
    peep = models.IntegerField(blank=True, null=True)  #
    recorder = models.CharField(max_length=35)  # 记录人
    date = models.DateTimeField(blank=True, null=True)  # 记录日期
    patient = models.ForeignKey(PatientInfo, on_delete=models.CASCADE)  # 关联病人信息
