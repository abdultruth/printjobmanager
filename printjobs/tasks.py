# tasks.py
from celery import shared_task
from .printer_event_listener import PrintEventListener

@shared_task
def run_print_listener():
    print_listener = PrintEventListener()
    print_listener.run()
