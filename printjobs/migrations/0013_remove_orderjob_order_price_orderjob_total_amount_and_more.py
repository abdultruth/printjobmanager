# Generated by Django 4.2.3 on 2023-08-11 08:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import printjobs.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('printjobs', '0012_payment_confirmed_by'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderjob',
            name='order_price',
        ),
        migrations.AddField(
            model_name='orderjob',
            name='total_amount',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
        migrations.AlterField(
            model_name='order',
            name='discount',
            field=models.FloatField(default=0.0),
        ),
        migrations.AlterField(
            model_name='payment',
            name='confirmed_by',
            field=models.ForeignKey(limit_choices_to={'is_admin': True}, on_delete=models.SET(printjobs.models.set_user_inactive), to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='Expense',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('job_order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='expenses', to='printjobs.orderjob')),
            ],
        ),
    ]