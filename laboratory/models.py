from django.db import models
from patient.models import PatientInfo


class CBC(models.Model):

    bloodGroup = models.CharField(max_length=7, default='', blank=True, null=True)
    wbc = models.FloatField(blank=True, null=True)
    lym = models.FloatField(blank=True, null=True)
    mid = models.FloatField(blank=True, null=True)
    gran = models.FloatField(blank=True, null=True)
    rbc = models.FloatField(blank=True, null=True)
    hemoglobin = models.FloatField(blank=True, null=True)
    hematocrite = models.FloatField(blank=True, null=True)
    plt = models.FloatField(blank=True, null=True)
    mcv = models.FloatField(blank=True, null=True)
    mch = models.FloatField(blank=True, null=True)
    mchc = models.FloatField(blank=True, null=True)
    rdw = models.FloatField(blank=True, null=True)
    esrH1 = models.FloatField(blank=True, null=True)
    esrH2 = models.FloatField(blank=True, null=True)
    recorder = models.CharField(max_length=25)  # 记录人
    date = models.DateTimeField(auto_now_add=True)  # 记录日期
    patient = models.ForeignKey(PatientInfo, on_delete=models.CASCADE)  # 关联病人信息
    status = models.BooleanField(default=True, blank=True)  # True表示已确认， False表示已取消


class Coagulation(models.Model):
    """血常规"""

    pt = models.FloatField(blank=True, null=True)
    inr = models.FloatField(blank=True, null=True)
    aptt = models.FloatField(blank=True, null=True)
    bleedTime = models.FloatField(blank=True, null=True)
    clotTime = models.FloatField(blank=True, null=True)
    act = models.FloatField(blank=True, null=True)
    recorder = models.CharField(max_length=25)  # 记录人
    date = models.DateTimeField(auto_now_add=True)  # 记录日期
    patient = models.ForeignKey(PatientInfo, on_delete=models.CASCADE)  # 关联病人信息
    status = models.BooleanField(default=True, blank=True)  # True表示已确认， False表示已取消


class Biochemistry(models.Model):
    """生化"""

    glucose = models.FloatField(blank=True, null=True)
    urea = models.FloatField(blank=True, null=True)
    creatine = models.FloatField(blank=True, null=True)
    sgpt = models.FloatField(blank=True, null=True)
    sgot = models.FloatField(blank=True, null=True)
    biliTotal = models.FloatField(blank=True, null=True)
    biliDirect = models.FloatField(blank=True, null=True)
    biliIndirect = models.FloatField(blank=True, null=True)
    alp = models.FloatField(blank=True, null=True)  # alkPhosphatase
    amylase = models.FloatField(blank=True, null=True)
    ldh = models.FloatField(blank=True, null=True)
    albumin = models.FloatField(blank=True, null=True)
    totalProtein = models.FloatField(blank=True, null=True)
    ck = models.FloatField(blank=True, null=True)
    ck_mb = models.FloatField(blank=True, null=True)
    lipase = models.FloatField(blank=True, null=True)
    uric_acid = models.FloatField(blank=True, null=True)
    triglycerid = models.FloatField(blank=True, null=True)
    cholesterol = models.FloatField(blank=True, null=True)
    crp = models.FloatField(blank=True, null=True)
    aslo = models.FloatField(blank=True, null=True)
    rf = models.FloatField(blank=True, null=True)
    recorder = models.CharField(max_length=25)  # 记录人
    date = models.DateTimeField(auto_now_add=True)  # 记录日期
    patient = models.ForeignKey(PatientInfo, on_delete=models.CASCADE)  # 关联病人信息
    status = models.BooleanField(default=True, blank=True)  # True表示已确认， False表示已取消


class Electrolytes(models.Model):
    """电解质"""

    na = models.FloatField(blank=True, null=True)
    k = models.FloatField(blank=True, null=True)
    cl = models.FloatField(blank=True, null=True)
    tca = models.FloatField(blank=True, null=True)
    nca = models.FloatField(blank=True, null=True)
    ica = models.FloatField(blank=True, null=True)
    iron = models.FloatField(blank=True, null=True)
    mg = models.FloatField(blank=True, null=True)
    phosphorus = models.FloatField(blank=True, null=True)
    recorder = models.CharField(max_length=25)  # 记录人
    date = models.DateTimeField(auto_now_add=True)  # 记录日期
    patient = models.ForeignKey(PatientInfo, on_delete=models.CASCADE)  # 关联病人信息
    status = models.BooleanField(default=True, blank=True)  # True表示已确认， False表示已取消


class ABG(models.Model):
    """动脉血气"""

    ph = models.FloatField(blank=True, null=True)
    pc02 = models.FloatField(blank=True, null=True)
    p02 = models.FloatField(blank=True, null=True)
    na = models.FloatField(blank=True, null=True)
    k = models.FloatField(blank=True, null=True)
    ca1 = models.FloatField(blank=True, null=True)
    glucose = models.FloatField(blank=True, null=True)
    lac = models.FloatField(blank=True, null=True)
    hc03 = models.FloatField(blank=True, null=True)
    beecf = models.FloatField(blank=True, null=True)
    s02c = models.FloatField(blank=True, null=True)
    fi02 = models.FloatField(blank=True, null=True)
    recorder = models.CharField(max_length=25)  # 记录人
    date = models.DateTimeField(auto_now_add=True)  # 记录日期
    patient = models.ForeignKey(PatientInfo, on_delete=models.CASCADE)  # 关联病人信息
    status = models.BooleanField(default=True, blank=True)  # True表示已确认， False表示已取消


class Serology(models.Model):
    """血清学"""

    hbs_Ag = models.CharField(max_length=7, blank=True, null=True)
    hiv = models.CharField(max_length=7, blank=True, null=True)
    hcv = models.CharField(max_length=7, blank=True, null=True)
    hcg = models.CharField(max_length=7, blank=True, null=True)
    fob = models.FloatField(blank=True, null=True)
    widal_o = models.CharField(max_length=7, blank=True, null=True)
    widal_h = models.CharField(max_length=7, blank=True, null=True)
    wrigh_a = models.CharField(max_length=7, blank=True, null=True)
    wrigh_b = models.CharField(max_length=7, blank=True, null=True)
    recorder = models.CharField(max_length=25)  # 记录人
    date = models.DateTimeField(auto_now_add=True)  # 记录日期
    patient = models.ForeignKey(PatientInfo, on_delete=models.CASCADE)  # 关联病人信息
    status = models.BooleanField(default=True, blank=True)  # True表示已确认， False表示已取消


class UrineAnalysis(models.Model):
    """尿常规"""

    color = models.CharField(max_length=10, blank=True, null=True)
    spGravity = models.FloatField(blank=True, null=True)
    netrit = models.CharField(max_length=7, blank=True, null=True)
    wbc = models.CharField(max_length=7, blank=True, null=True)
    urates = models.CharField(max_length=7, blank=True, null=True)
    uric_acid = models.CharField(max_length=7, blank=True, null=True)
    appearance = models.CharField(max_length=7, blank=True, null=True)
    glucose = models.CharField(max_length=5, blank=True, null=True)
    keton = models.CharField(max_length=5, blank=True, null=True)
    rbc = models.CharField(max_length=7, blank=True, null=True)
    bacteria = models.CharField(max_length=7, blank=True, null=True)
    mucus = models.CharField(max_length=7, blank=True, null=True)
    ph = models.FloatField(blank=True, null=True)
    blood = models.CharField(max_length=5, blank=True, null=True)
    protein = models.CharField(max_length=5, blank=True, null=True)
    epCells = models.CharField(max_length=5, blank=True, null=True)
    ox_calcium = models.CharField(max_length=5, blank=True, null=True)
    casts = models.CharField(max_length=5, blank=True, null=True)
    fungi = models.CharField(max_length=5, blank=True, null=True)
    yeast = models.CharField(max_length=5, blank=True, null=True)
    pus_cell = models.CharField(max_length=5, blank=True, null=True)
    triple_phospate = models.CharField(max_length=5, blank=True, null=True)
    recorder = models.CharField(max_length=25)  # 记录人
    date = models.DateTimeField(auto_now_add=True)  # 记录日期
    patient = models.ForeignKey(PatientInfo, on_delete=models.CASCADE)  # 关联病人信息
    status = models.BooleanField(default=True, blank=True)  # True表示已确认， False表示已取消


class CSF(models.Model):
    """脑椎液"""

    color = models.CharField(max_length=7, blank=True, null=True)
    appearance = models.CharField(max_length=7, blank=True, null=True)
    rbc = models.FloatField(blank=True, null=True)
    wbc = models.CharField(max_length=7, blank=True, null=True)
    glucose = models.FloatField(blank=True, null=True)
    protein = models.FloatField(blank=True, null=True)
    recorder = models.CharField(max_length=25)  # 记录人
    date = models.DateTimeField(auto_now_add=True)  # 记录日期
    patient = models.ForeignKey(PatientInfo, on_delete=models.CASCADE)  # 关联病人信息
    status = models.BooleanField(default=True, blank=True)  # True表示已确认， False表示已取消


class Antibiotics(models.Model):
    """抗生素"""

    cephradine = models.FloatField(blank=True, null=True)
    ciprofloxacin = models.FloatField(blank=True, null=True)
    gentamicin = models.FloatField(blank=True, null=True)
    nitrofurantoin = models.FloatField(blank=True, null=True)
    ofloxacin = models.FloatField(blank=True, null=True)
    cefoxitin = models.FloatField(blank=True, null=True)
    cefaclor = models.FloatField(blank=True, null=True)
    amikacin = models.FloatField(blank=True, null=True)
    ceftriaxone = models.FloatField(blank=True, null=True)
    amoxicillin_clavulanic_acid = models.FloatField(blank=True, null=True)
    cefadroxil = models.FloatField(blank=True, null=True)
    cefixime = models.FloatField(blank=True, null=True)
    cefotaxime = models.FloatField(blank=True, null=True)
    cefuroxime = models.FloatField(blank=True, null=True)
    imipenem = models.FloatField(blank=True, null=True)
    ampicillin_sulbactam = models.FloatField(blank=True, null=True)  # 13 -- 18
    amoxicillin = models.FloatField(blank=True, null=True)
    azithromycin = models.FloatField(blank=True, null=True)
    levofloxacin = models.FloatField(blank=True, null=True)
    neomycin = models.FloatField(blank=True, null=True)
    doxycycline = models.FloatField(blank=True, null=True)
    pipemidic_acid = models.FloatField(blank=True, null=True)
    meropenem = models.FloatField(blank=True, null=True) # 12 -- 17
    cloxacillin = models.FloatField(blank=True, null=True)
    trimethoprim_sulphamethoxazole = models.FloatField(blank=True, null=True)  # 12 -- 16
    norfloxacin = models.FloatField(blank=True, null=True)  # 12 -- 16
    recorder = models.CharField(max_length=25)  # 记录人
    date = models.DateTimeField(auto_now_add=True)  # 记录日期
    patient = models.ForeignKey(PatientInfo, on_delete=models.CASCADE)  # 关联病人信息
    status = models.BooleanField(default=True, blank=True)  # True表示已确认， False表示已取消


class Hormones(models.Model):
    """激素"""

    hba1c = models.FloatField(blank=True, null=True)
    tsh = models.FloatField(blank=True, null=True)
    ft4 = models.FloatField(blank=True, null=True)
    t4 = models.FloatField(blank=True, null=True)
    t3 = models.FloatField(blank=True, null=True)
    lh = models.FloatField(blank=True, null=True)
    fsh = models.FloatField(blank=True, null=True)
    prolactin = models.FloatField(blank=True, null=True)
    testosterone = models.FloatField(blank=True, null=True)
    cortisol = models.FloatField(blank=True, null=True)
    vit_d = models.FloatField(blank=True, null=True)
    ferritin = models.FloatField(blank=True, null=True)
    d_dimer = models.FloatField(blank=True, null=True)
    b_hcg = models.FloatField(blank=True, null=True)
    troponin_i = models.FloatField(blank=True, null=True)
    troponin_t = models.FloatField(blank=True, null=True)  # 13 -- 18
    amh = models.FloatField(blank=True, null=True)
    psa = models.FloatField(blank=True, null=True)
    cea = models.FloatField(blank=True, null=True)
    afp = models.FloatField(blank=True, null=True)
    toxo_igg_igm = models.FloatField(blank=True, null=True)
    recorder = models.CharField(max_length=25)  # 记录人
    date = models.DateTimeField(auto_now_add=True)  # 记录日期
    patient = models.ForeignKey(PatientInfo, on_delete=models.CASCADE)  # 关联病人信息
    status = models.BooleanField(default=True, blank=True)  # True表示已确认， False表示已取消
