# Generated by Django 4.2.3 on 2023-08-15 02:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('printjobs', '0025_joborder_job_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='joborder',
            name='job_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='printjobs.jobtype'),
        ),
    ]
