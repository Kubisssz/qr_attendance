# Generated by Django 5.1.2 on 2024-10-17 01:31

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("attendance", "0002_alter_employee_email"),
    ]

    operations = [
        migrations.AddField(
            model_name="attendance",
            name="check_out_time",
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
