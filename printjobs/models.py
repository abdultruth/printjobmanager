from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib.auth.models import Permission



def set_user_inactive():
    get_user_model.objects.is_active = True
    get_user_model.save()

# Create your models here.
class Order(models.Model):
    STATUS = [('New','New'),
              ('Confirmed','Confirmed'),
              ('Completed', 'Completed'),
              ('Cancelled', 'Cancelled'),
            ]
             
    length = models.FloatField()
    width = models.FloatField()
    quantity = models.PositiveIntegerField()
    job_type = models.ForeignKey('JobType', on_delete=models.CASCADE)
    staff = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET(set_user_inactive), limit_choices_to={'is_admin': True})
    price = models.FloatField(db_index=True)
    status = models.CharField(max_length=10, choices=STATUS, default='New', db_index=True)
    customer = models.ForeignKey('Customer', on_delete=models.CASCADE)
    discount = models.FloatField(default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    ip = models.CharField(max_length=20)
    
    
    def __str__(self):
        return f'{self.job_type}/{self.length}/{self.width}/{self.created_at}'
    
    def get_absolute_url(self):
        return reverse('printjob:unconf-order-details', kwargs={"pk": self.pk})
    
    
class Customer(models.Model):
    Name = models.CharField(max_length=120, db_index=True)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f'{self.Name}'
     
    
class JobType(models.Model):
    name = models.CharField(max_length=100)
    rate = rate = models.FloatField(default=1.0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f'{self.name}'
    
    
class Payment(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    payment_id = models.CharField(max_length=100)
    payment_method = models.CharField(max_length=100)
    amount_paid = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_created=True)
    tax = models.FloatField()
    ip = models.CharField(max_length=20)
    confirmed_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET(set_user_inactive), limit_choices_to={'is_admin': True})
    
    def __str__(self):
        return f'{self.payment_method}|{self.payment_method}|{self.amount_paid}'
    
    # class Meta:
    #     Permissions = [
    #         ("Can_change_job_order_status_to_paid","Can change job order status to paid")
    #     ]
    
    
class JobOrder(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE, null=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    job_type = models.ForeignKey(JobType, on_delete=models.CASCADE)
    staff = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET(set_user_inactive), limit_choices_to={'is_admin': True})
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    ordered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False)
    
    def __str__(self):
        return f'{self.order}'
    
    
    def get_absolute_url(self):
        return reverse('printjob:ordered-details', kwargs={"pk": self.pk})
    

class Expense(models.Model):
    title = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    job_order = models.ForeignKey(JobOrder, on_delete=models.CASCADE, related_name='expenses')
    created = models.DateTimeField(auto_now_add=True)
    
    

class Print(models.Model):
    STATUS = [
              ('In_progress', 'In_progress'),
              ('Completed', 'Completed'),
              ('Print_error', 'Print_error'),
            ]
    length = models.FloatField()
    width = models.FloatField()
    order_job = models.OneToOneField(JobOrder, on_delete=models.CASCADE)
    status = models.CharField(max_length=11, choices=STATUS, default='In_progress', db_index=True)
    collected = models.BooleanField(default=False)
    printed_by = models.ForeignKey(settings.AUTH_USER_MODEL, models.SET(set_user_inactive), limit_choices_to={'is_admin': True})
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(auto_now=True)
    
    
class GroupPermissions(models.Model):
    class Meta:
        permissions = [
            ("access_place_order_page", "Can access the place order page"),
            ("can_place_order", "Can placed order"),
            ("can_delete_placed_order", "Can delete placed order"),
            ("can_confirm_order","can confirm order"),
        ]   