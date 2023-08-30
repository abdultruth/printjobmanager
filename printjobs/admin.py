from django.contrib import admin

from .models import Order, JobType, Customer, Payment, JobOrder, Print, Expense
# Register your models here.

class JobTypeInline(admin.TabularInline):
    model = JobType
    extra = 1
    

class OrderAdmin(admin.ModelAdmin):
    list_display = ('job_type','customer', 'width', 'length', 'price', 'status','quantity','staff')
    
    list_display_links = ('job_type','price','status','customer','staff')
    fieldsets = ()
    readonly_fields=('job_type','status','customer', 'price','quantity','length','width','discount','staff')



class JobtypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'rate')  
    
    

admin.site.register(Order, OrderAdmin)
admin.site.register(JobType)
admin.site.register(Customer)
admin.site.register(Payment)
admin.site.register(JobOrder)
admin.site.register(Print)
admin.site.register(Expense)
