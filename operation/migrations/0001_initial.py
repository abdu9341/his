# Generated by Django 3.2.9 on 2022-12-23 22:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('patient', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='OperationDictionary',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=35)),
            ],
        ),
        migrations.CreateModel(
            name='TimeTable',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('doctor', models.CharField(max_length=35)),
                ('date', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Operation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=35)),
                ('doctor', models.CharField(max_length=35)),
                ('assistant', models.CharField(max_length=35)),
                ('surgicalNurse', models.CharField(max_length=20)),
                ('anesthetist', models.CharField(max_length=35)),
                ('typesNarcosis', models.CharField(max_length=15)),
                ('typesOperation', models.CharField(max_length=10)),
                ('roomNo', models.CharField(max_length=20)),
                ('begin', models.DateTimeField()),
                ('timeOfOperation', models.SmallIntegerField()),
                ('recordDate', models.DateTimeField(auto_now_add=True)),
                ('operator', models.CharField(default='', max_length=35)),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='patient.patientinfo')),
            ],
        ),
        migrations.CreateModel(
            name='BookingOperation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=35)),
                ('date', models.DateField()),
                ('timeOfOperation', models.SmallIntegerField(default=1)),
                ('operator', models.CharField(default='', max_length=35)),
                ('order', models.SmallIntegerField(default=1)),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='patient.patientinfo')),
                ('timeTable', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='operation.timetable')),
            ],
        ),
    ]