# Generated by Django 4.2.3 on 2023-07-27 14:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('printjobs', '0006_order_ip_alter_order_status_payment_orderjob'),
    ]

    operations = [
        migrations.RenameField(
            model_name='payment',
            old_name='status',
            new_name='created_at',
        ),
    ]
