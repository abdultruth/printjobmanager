# Generated by Django 4.2.3 on 2023-08-14 22:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('printjobs', '0019_alter_grouppermissions_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='grouppermissions',
            options={'permissions': [('access_place_order_page', 'Can access the place order page'), ('can_delete_placed_order', 'Can delete placed order'), ('can_confirm_order', 'can confirm order')]},
        ),
    ]