from django.db import models
from patient.models import PatientInfo


class Discharge(models.Model):
    """出院"""

    leaveDate = models.DateTimeField(auto_now_add=True, blank=True,)  # 出院时间
    leavingDepartment = models.CharField(max_length=35, blank=True, null=True)  # 出院的科室
    dischargeStatus = models.CharField(max_length=35, blank=True, null=True)  # 出院状况
    patient = models.ForeignKey(PatientInfo, on_delete=models.CASCADE)  # 关联病人信息
    operator = models.CharField(max_length=25, null=True)

