# Generated by Django 3.2.9 on 2023-01-22 19:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('laboratory', '0006_auto_20230122_1902'),
    ]

    operations = [
        migrations.AddField(
            model_name='electrolytes',
            name='phosphorus',
            field=models.FloatField(blank=True, null=True),
        ),
    ]