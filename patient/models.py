from django.db import models
from department.models import Department, Ward


class BasicInfo(models.Model):

    name = models.CharField(max_length=30)  # 姓名
    birthday = models.DateField(default=None, blank=True, null=True)  # 出生日期
    age = models.FloatField(default=0, blank=True, null=True)  # 年龄
    sex = models.CharField(max_length=10)  # 性别
    bloodGroup = models.CharField(max_length=8, default='', blank=True, null=True)
    marriage = models.CharField(max_length=20, default='', null=True)  # 婚姻状况
    address = models.CharField(max_length=80, default='',  blank=True, null=True)  # 现地址
    phone = models.CharField(max_length=20, default='', blank=True, null=True)  # 病人家属电话
    ses = models.BooleanField(default=False, null=True)
    date = models.DateTimeField(auto_now_add=True, blank=True, null=True)  # 记录时间
    operator = models.CharField(default='', max_length=25, blank=True, null=True)  #

    def __str__(self):
        return self.name


class PatientInfo(models.Model):
    """病人住院信息表"""

    basicInfo = models.ForeignKey(BasicInfo, on_delete=models.CASCADE)  # 病人基本信息
    department = models.ManyToManyField(Department, blank=True)  # 所属科室
    diagnosis = models.CharField(max_length=250, default='', blank=True, null=True)  # 诊断
    # polyclinicDepartment = models.CharField(max_length=27, blank=True, null=True)  # 门诊挂号的科室
    patientID = models.CharField(max_length=11, default='')  # 住院号
    sickroom = models.ForeignKey(Ward, on_delete=models.DO_NOTHING, null=True, blank=True)  # 病房
    enterDate = models.DateTimeField(auto_now_add=True, blank=True, null=True)  # 住院时间
    # 0表示住院病人出院，1表示住院病人，2表示急诊病人，3表示急诊病人出院，5表示门诊等待就诊， 6表示门诊已就诊，7表示门诊缺席，8表示门诊病人出院，
    condition = models.SmallIntegerField(null=True, blank=True)
    #  TRUE 表示该病人的姓名的音频文件已成功生成， FALSE 表示 该病人的姓名的音频文件没有成功生成
    haveSes = models.BooleanField(default=True, null=True, blank=True)
    transferDate = models.DateTimeField(auto_now_add=True, blank=True, null=True)  # 转病房日期
    haveLaboratoryTest = models.SmallIntegerField(default=0)  # 0表示没有检验单，1表示有检验单, 2表示已完成化验单
    haveXRayTest = models.SmallIntegerField(default=0)  # 0表示没有检查单，1表示有检查单, 2表示已完成检查单
    arrive = models.BooleanField(default=False, null=True)  # False表示未到达，True表示已到达
    arriveDate = models.DateTimeField(blank=True, null=True)  # 到达日期
    typeOfEmergency = models.SmallIntegerField(default=0, null=True)  # 1表示green，2表示yellow, 3表示red, 4表示black
    operator = models.CharField(default='', max_length=25, blank=True, null=True)  #

    def __str__(self):
        return self.basicInfo.name


class Counter(models.Model):
    """计数，记日"""

    day = models.SmallIntegerField(default=1, null=True)
    count = models.SmallIntegerField(default=1, null=True)


class MedicalInfo(models.Model):
    """病历信息表"""
    complaint = models.TextField(blank=True)  # 病人病情描述
    medicalHistory = models.TextField(blank=True)  # 病史
    surgeryHistory = models.TextField(blank=True)  # 手术史
    medicineHistory = models.TextField(blank=True)  # 用药史
    allergyHistory = models.TextField(blank=True)  # 过敏史
    familyHistory = models.TextField(blank=True)  # 家族史
    habit = models.TextField(blank=True)  # 个人生活史
    clinicalExamination = models.TextField(blank=True)  # 临床检查
    test = models.TextField(blank=True)  # 检验
    diagnosis = models.TextField(blank=True)  # 诊断
    remind = models.TextField(blank=True)  # 提醒
    doctor = models.CharField(max_length=20, default='')  # 记录病例的医生
    patient = models.OneToOneField(PatientInfo, on_delete=models.CASCADE)  # 关联病人信息

