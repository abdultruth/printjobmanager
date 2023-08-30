# printer_event_listener.py
import win32evtlog
import win32evtlogutil
import time

class PrintEventListener:
    def __init__(self):
        self.events_flags = win32evtlog.EVENTLOG_BACKWARDS_READ | win32evtlog.EVENTLOG_SEQUENTIAL_READ
        self.events_handle = win32evtlog.OpenEventLog(None, 'System')

    def run(self):
        while True:
            events = win32evtlog.ReadEventLog(self.events_handle, self.events_flags, 0)
            for event in events:
                if event.EventID == 307:  # Print job submitted event ID (you can verify the actual event ID for print jobs)
                    print(f"Print job submitted: {event.StringInserts}")
            time.sleep(5)  # Sleep for a few seconds before checking for new events again

    def stop(self):
        win32evtlog.CloseEventLog(self.events_handle)
