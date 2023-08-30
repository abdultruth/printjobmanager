

import asyncio
from typing import Any
from django.db.models.query import QuerySet

from django.forms.models import BaseModelForm
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect
from django.db.models import Sum
from django.http import JsonResponse 
from django.contrib.auth.mixins import (
                                        LoginRequiredMixin,
                                        PermissionRequiredMixin
                                        )
from django.contrib.auth.decorators import login_required, permission_required
from django.core.exceptions import PermissionDenied
from django.utils.decorators import method_decorator
from django.views import View
from django.contrib import messages



import win32print
import win32evtlog


from django.shortcuts import get_object_or_404, render
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, DeleteView
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.urls import reverse, reverse_lazy



from .models import Order, JobOrder, JobType, Print, Expense, Payment
from .forms import OrderForm


def index(request):
    return render(request, 'base.html')
    
    
    

def printer_jobs(request):
    print(win32print.EnumJobs(win32print.OpenPrinter(win32print.GetDefaultPrinter()), 0, -1, 1 ))
    jobs = []

    printer_name = win32print.GetDefaultPrinter()
    handle = win32print.OpenPrinter(printer_name)
    job_info = win32print.EnumJobs(handle, 0, -1, 2)

    for job in job_info:
        job_id, _, _, status = job
        jobs.append({
            'job_id': job_id,
            'status': status,
        })
        
    win32print.ClosePrinter(handle)

    return render(request, 'printjobs/print_jobs.html', {'jobs': jobs, 'printer_name': printer_name})



class CreateJobView(LoginRequiredMixin, CreateView):
    model = Order
    template_name = 'order/create_order.html'
    form_class = OrderForm
    success_url = reverse_lazy('printjob:order')
    
    
    def get_form(self):
        form = super(CreateJobView, self).get_form()
        return form
        
    def form_valid(self, form):
        form.instance.staff = self.request.user
        form.instance.status = 'New'
        form.save()
        return super(CreateJobView, self).form_valid(form)
    
    
class RedirectView(View):
    def get(self, request, *args, **kwargs):
        messages.error(request, "You don't have permission to access this page.")
        return redirect('account:login')
    
    
class RestrictedPageView(View):
    @method_decorator(permission_required('printjobs.access_place_order_page', raise_exception=True))
    def get(self, request, *args, **kwargs):
        return render(request, 'restricted_page.html')
    
    
class RedirectView(View):
    def get(self, request, *args, **kwargs):
        messages.error(request, "You don't have permission to access this page.")
        return redirect('login')
            
    
    
class OrderDetailView(DetailView):
    model = Order
    template_name = 'order/order_details.html'
    
    def get_queryset(self):
        return super().get_queryset()

    
class OrderedJobDetailView(DetailView):
    model = JobOrder
    template_name = 'order/orderjob_details.html'  
    

    
    
class OrderListView(ListView):
    model = Order
    template_name = 'order/order_list.html'
    

class OrderedJobListView(ListView):
    model = JobOrder
    template_name = 'order/joborder_list.html'
    queryset = JobOrder.objects.filter(paid=False)

 

def record_print_job_event(request):
    hand = win32evtlog.OpenEventLog('localhost', 'System')
    flags = win32evtlog.EVENTLOG_BACKWARDS_READ | win32evtlog.EVENTLOG_SEQUENTIAL_READ

    events = win32evtlog.ReadEventLog(hand, flags, 0)
    
    for event in events:
            if event.EventID == 307:
                print(event)
            else:
                print('none')
                # Event ID 307 corresponds to print job events
    #             print_data = event.StringInserts[1]  # Extract print job information
    #             # Process and record print_data in the database
    #             print(print_data)

    events = win32evtlog.ReadEventLog(hand, flags, 0)

    win32evtlog.CloseEventLog(hand)
    
    # context = {
    #     'events':events,
    #     'hand': hand,
    #     'flags':flags
    # }
    # {'context':context}
    
    return render(request, 'printjobs/records.html')
    
    
# Step 3: Run the Monitoring Script
# Run the monitoring script as a background service or in a separate process to continuously monitor the Windows Event Log for print events.

# Note: Running scripts that access the Windows Event Log API typically requires administrative privileges. Ensure that the script is executed with the necessary permissions.

# Please note that directly interacting with the Windows Event Log API requires knowledge of the Event Log structure and IDs to filter the relevant print job events. You may need to customize the script based on your specific use case and the information logged in the Windows Event Log for print events.

# Additionally, consider using external tools or third-party solutions that specialize in monitoring print activities on Windows systems to ensure more comprehensive monitoring and easier management. These tools often offer more robust features and can simplify the process of capturing print events.

def check_order(request):
    if request.method == 'GET':
      if 'q' in request.GET:
        query = request.GET['q']
        jobs = Order.objects.filter(id__icontains=query)
        return render(request, 'order/check_job.html', {'jobs':jobs})
    
    return render(request, 'order/check_job.html')

@permission_required('printjobs.can_delete_placed_order')
def delete_order(request, id):
    order = get_object_or_404(Order, pk=id)
    order.delete()
    return redirect('printjob:order')
    
# @permission_required('printjobs.can_confirm_order')
def confirm_job_order(request, order_id):
  if request.method == 'POST':
    order = get_object_or_404(Order, pk=order_id)
    order.status = 'confirmed'
    order.save()
        
    job_order = JobOrder(
        order = order,
        job_type = order.job_type,
        quantity = order.quantity,
        customer = order.customer,
        total_amount = order.price,
        staff = request.user
        )

    job_order.ordered = True
    job_order.save()
        
    return redirect('printjob:checkout')



def process_orders_view(request):
    if request.method == 'POST':
      # Get the all id the selected ordered job    
      selected_joborders_ids = request.POST.getlist('selected_orders')
      # Filter them out Fetch order data from database    
      selected_orders = JobOrder.objects.filter(id__in=selected_joborders_ids) 
      # sum the total_amount  
      total_price = sum(joborder.total_amount for joborder in selected_orders)
      
        
    # Process selected_orders as needed (e.g., update the orders, send emails, etc.)
    #   return HttpResponse('Selected orders processed successfully.')
    
      return render(request, 'order/payment_order_list.html', {'orders': selected_orders, 'total':total_price})

    


@csrf_exempt
def get_order_job(request): 
    if request.method == 'POST': 
        job_id = request.POST.get('job_id')
        try:
            order_job =  JobOrder.objects.get(pk=job_id) 
            # order_job is ordered, allow printing 
            return JsonResponse({'job_id': order_job.id,
                                 'ordered': order_job.ordered, 
                                #  'customer':order_job.customer, 
                                #  'staff':order_job.staff,
                                 'created_at': order_job.created_at}) 
    
        except JobOrder.DoesNotExist:
            # order_job is not ordered, deny printing 
            return JsonResponse({'job_id':job_id, 'ordered': False})


def print(request):
    if request.method == 'POST':
        job_id = request.POST.get('job_id')
        ordered_job = get_object_or_404(JobOrder, pk=job_id)
        job_to_print == Print.objects.create()
        
        
        
def yearly_job_order_expenses_profit(request):
    pass
        
        
        
def  monthly_job_order_expenses_profit(request):
    # get year
    # curent_year = request.GET.get('year', 2023)
    # get month
    # curent_month = request.GET.get('month', 8)
    # calculate the start and end dates of the month
    current_year = 2023
    current_month = 8
    start_date = f'{current_year}-{current_month:02d}-01'
    end_date = f'{current_year}-{current_month:02d}-31'
    # get the total jo order amount
    total_job_order_amount = JobOrder.objects.filter(
                                                      created_at__range=[
                                                                         start_date, 
                                                                         end_date
                                                                        ]
                                                    ).aggregate(total_amount=Sum('total_amount'))['total_amount'] or 0
    
    # Get the total expenses for the month
    total_expenses = Expense.objects.filter(
                                            created__range=[
                                                         start_date,
                                                         end_date]
    ).aggregate(total_amount=Sum('amount'))['total_amount'] or 0
    
    # Calculate the profit for the month
    profit = total_job_order_amount - total_expenses
    
    context = {
                'year': current_year,
                'month': current_month,
                'total_job_order_amount': total_job_order_amount,
                'total_expenses': total_expenses,
                'profit':profit
            }
    
    return render(request, 'printjobs/monthly_report.html', context)


def weekly_job_order_expenses_profit(request):
    pass




def add_print_job_view(request):
    orders = Order.objects.all()
    return render(request, 'add_print_job.html', {'orders': orders})



def add_print_job_to_order(request):
    if request.method == 'POST':
        order_id = request.POST.get('order')
        job_type = request.POST.get('job_name')
        quantity = request.POST.get('quantity')
        
        order = Order.objects.get(pk=order_id)
        print_job = JobOrder(order=order, job_type=job_type, quantity=quantity)
        print_job.save()
        
    return render(request, 'print_job_added.html')


def payment(request):
    return render(request, 'order/payment.html')


def generate_receipt(request):
    return render(request, 'order/print.html')
    
    
    
        


