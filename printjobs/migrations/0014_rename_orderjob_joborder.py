# Generated by Django 4.2.3 on 2023-08-11 08:46

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('printjobs', '0013_remove_orderjob_order_price_orderjob_total_amount_and_more'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='OrderJob',
            new_name='JobOrder',
        ),
    ]
