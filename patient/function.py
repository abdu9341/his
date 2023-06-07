from patient.models import Counter
from datetime import datetime
from patient.models import *


def IDCreator():
    """ 住院号"""

    if Counter.objects.all().exists():
        counter = Counter.objects.all().first()
        number = ''
        zero = '0'
        year = str(datetime.now().year)
        if datetime.now().month < 10:
            month = zero + str(datetime.now().month)
        else:
            month = str(datetime.now().month)

        if datetime.now().day < 10:
            day = zero + str(datetime.now().day)
        else:
            day = str(datetime.now().day)
        number = year + month + day

        if datetime.now().day == counter.day:
            number = number + str(counter.count)
            counter.count += 1
            counter.save()
        else:
            counter.count = 1
            number = number + str(counter.count)
            counter.day = datetime.now().day
            counter.count += 1
            counter.save()

        return number

    else:
        counter = Counter.objects.create(day=1, count=1)
        number = ''
        zero = '0'
        year = str(datetime.now().year)
        if datetime.now().month < 10:
            month = zero + str(datetime.now().month)
        else:
            month = str(datetime.now().month)

        if datetime.now().day < 10:
            day = zero + str(datetime.now().day)
        else:
            day = str(datetime.now().day)
        number = year + month + day

        if datetime.now().day == counter.day:
            number = number + str(counter.count)
            counter.count += 1
            counter.save()
        else:
            counter.count = 1
            number = number + str(counter.count)
            counter.day = datetime.now().day
            counter.count += 1
            counter.save()

        return number


def universal():

    # ICU 病人
    patientICU = PatientInfo.objects.filter(sickroom__name='ICU Ward', condition=1)
    patientHDUMen = PatientInfo.objects.filter(sickroom__name='HDU-Men', condition=1)
    patientHDUFemale = PatientInfo.objects.filter(sickroom__name='HDU-Female', condition=1)

    # 统计病人
    countOfICU = PatientInfo.objects.filter(sickroom__name='ICU Ward', condition=1).count()
    countOfHDU_Men = PatientInfo.objects.filter(sickroom__name='HDU-Men', condition=1).count()
    countOfHDU_Female = PatientInfo.objects.filter(sickroom__name='HDU-Female', condition=1).count()
    countOfMen = PatientInfo.objects.filter(sickroom__name='Men\'s Ward', condition=1).count()
    countOfFemal = PatientInfo.objects.filter(sickroom__name='Female Ward', condition=1).count()
    countOfCCUMen = PatientInfo.objects.filter(sickroom__name='CCU-Men', condition=1).count()
    countOfCCUFemale = PatientInfo.objects.filter(sickroom__name='CCU-Female', condition=1).count()
    countOfCovid_19 = PatientInfo.objects.filter(sickroom__name='Covid-19', condition=1).count()
    countOfTotal = PatientInfo.objects.filter(condition=1).count()

    result = (patientICU, patientHDUMen, patientHDUFemale, countOfICU,
              countOfHDU_Men, countOfHDU_Female, countOfMen, countOfFemal,
              countOfCCUMen, countOfCCUFemale, countOfCovid_19, countOfTotal)

    return result


# def countAge(birthday):
#     """计算年龄"""
#
#     # 出生年月日
#     birthYear = birthday.year
#     birthMonth = birthday.month
#     birthDay = birthday.day
#
#     # 当前年月日
#     year = datetime.now().year
#     month = datetime.now().month
#     day = datetime.now().day
#
#     # 计算年龄
#     age = 0
#     if year > birthYear:
#         age = year - birthYear - 1
#         if month - birthMonth:
#             age = age + 1
#         elif month == birthMonth and day >= birthDay:
#             age = age + 1
#
#     return age
