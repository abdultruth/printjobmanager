# Generated by Django 4.2.3 on 2023-08-14 20:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('printjobs', '0014_rename_orderjob_joborder'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='order',
            options={'permissions': [('access_place_order_page', 'Can access the place order page')]},
        ),
        migrations.AlterField(
            model_name='joborder',
            name='total_amount',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
        migrations.AlterField(
            model_name='print',
            name='order_job',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='printjobs.joborder'),
        ),
    ]
