from django.apps import AppConfig


# from .permissions import PrintJobPermission

class PrintjobsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'printjobs'

    # def ready(self):
    #    try:
    #        change_permission = PrintJobPermission.objects.get(codename='can_change_job_order_status_to_paid')
    #    except DoesNotExist:
    #        change_permission = None
           
    #    if not change_permission:
    #        PrintJobPermission.objects.create(
    #                                          codename='can_change_job_order_status_to_paid', 
    #                                          name='Can change job order status to paid'
    #                                          )
    #        print("Created 'Can_change_job_order_status_to_paid' Permission ")
           
           