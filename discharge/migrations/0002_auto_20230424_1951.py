# Generated by Django 3.2.9 on 2023-04-24 19:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('discharge', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='discharge',
            name='laboratory',
        ),
        migrations.RemoveField(
            model_name='discharge',
            name='medicine',
        ),
        migrations.RemoveField(
            model_name='discharge',
            name='pathology',
        ),
        migrations.RemoveField(
            model_name='discharge',
            name='radiological',
        ),
        migrations.RemoveField(
            model_name='discharge',
            name='recommendations',
        ),
        migrations.RemoveField(
            model_name='discharge',
            name='surgical',
        ),
        migrations.AlterField(
            model_name='discharge',
            name='leavingDepartment',
            field=models.CharField(blank=True, max_length=35, null=True),
        ),
        migrations.AlterField(
            model_name='discharge',
            name='operator',
            field=models.CharField(max_length=25, null=True),
        ),
    ]