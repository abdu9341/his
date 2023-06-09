# Generated by Django 3.2.9 on 2023-01-22 19:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('laboratory', '0010_auto_20230122_1906'),
    ]

    operations = [
        migrations.AddField(
            model_name='urineanalysis',
            name='appearance',
            field=models.CharField(blank=True, max_length=7, null=True),
        ),
        migrations.AddField(
            model_name='urineanalysis',
            name='bacteria',
            field=models.CharField(blank=True, max_length=7, null=True),
        ),
        migrations.AddField(
            model_name='urineanalysis',
            name='casts',
            field=models.CharField(blank=True, max_length=5, null=True),
        ),
        migrations.AddField(
            model_name='urineanalysis',
            name='fungi',
            field=models.CharField(blank=True, max_length=5, null=True),
        ),
        migrations.AddField(
            model_name='urineanalysis',
            name='mucus',
            field=models.CharField(blank=True, max_length=7, null=True),
        ),
        migrations.AddField(
            model_name='urineanalysis',
            name='netrit',
            field=models.CharField(blank=True, max_length=7, null=True),
        ),
        migrations.AddField(
            model_name='urineanalysis',
            name='ox_calcium',
            field=models.CharField(blank=True, max_length=5, null=True),
        ),
        migrations.AddField(
            model_name='urineanalysis',
            name='pus_cell',
            field=models.CharField(blank=True, max_length=5, null=True),
        ),
        migrations.AddField(
            model_name='urineanalysis',
            name='triple_phospate',
            field=models.CharField(blank=True, max_length=5, null=True),
        ),
        migrations.AddField(
            model_name='urineanalysis',
            name='urates',
            field=models.CharField(blank=True, max_length=7, null=True),
        ),
        migrations.AddField(
            model_name='urineanalysis',
            name='uric_acid',
            field=models.CharField(blank=True, max_length=7, null=True),
        ),
        migrations.AddField(
            model_name='urineanalysis',
            name='yeast',
            field=models.CharField(blank=True, max_length=5, null=True),
        ),
    ]
