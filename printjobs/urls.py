from django.urls import include, path


from . import views

app_name = 'printjob'

urlpatterns = [
    path('', views.index, name='home'),
    path('print/', views.printer_jobs, name='print-jobs'),
    path('place-order', views.CreateJobView.as_view(), name='place-job-order'),
    path('printjob', views.get_order_job, name='printjob'),
    path('jobevent', views.record_print_job_event, name='jobevent'),
    path('order', views.OrderListView.as_view(), name='order'),
    path('unconf-order/<int:pk>', views.OrderDetailView.as_view(), name='unconf-order-details'),
    path('order/<int:pk>', views.OrderedJobDetailView.as_view(), name='ordered-details'),
    path('checkout', views.OrderedJobListView.as_view(),name='checkout'),
    path('confirm/<int:order_id>', views.confirm_job_order, name='confirm'),
    path('check', views.check_order, name='check'),
    path('delete/<int:id>', views.delete_order, name='delete'),
    path('monthly', views.monthly_job_order_expenses_profit, name='monthly'),
    path('add-print-job/', views.add_print_job_view, name='add_print_job_view'),
    path('add-print-job-to-order/', views.add_print_job_to_order, name='add_print_job_to_order'),
    path('restricted/', views.RestrictedPageView.as_view(), name='restricted_page'),
    path('redirect/', views.RedirectView.as_view(), name='redirect'),
    path('process_orders', views.process_orders_view, name='process_orders'),
    path('payment', views.payment, name='payment'),
    path('receipt', views.generate_receipt, name="receipt"),
]