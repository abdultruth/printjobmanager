# Generated by Django 4.2.3 on 2023-08-05 14:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('printjobs', '0008_rename_user_payment_customer'),
    ]

    operations = [
        migrations.RenameField(
            model_name='orderjob',
            old_name='Customer',
            new_name='customer',
        ),
    ]