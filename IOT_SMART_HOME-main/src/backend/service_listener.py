from backend.event import subscribe
from backend.devices.DeviceBase import DeviceBase
from backend.event import post_event
from collections import deque


class ServiceListener:
    def __init__(self, service):
        self.service = service
        self.is_running = True
        self.tasks = deque()
        self.setup_service_event_handlers()

    def add_task(self, msg, args):
        def task(): post_event(msg, args)
        self.tasks.append(task)

    def handel_on_turn_on_device_event(self, device_id):
        self.service.service_handeler.handel_on_switch_on(device_id)

    def handel_on_turn_off_device_event(self, device_id):
        self.service.service_handeler.handel_on_switch_off(device_id)

    def handel_on_device_status_changed_event(self, device):
        self.service.service_handeler.handel_on_device_status_changed()

    def setup_service_event_handlers(self):
        subscribe("turn_on_device", self.handel_on_turn_on_device_event)
        subscribe("turn_off_device", self.handel_on_turn_off_device_event)
        subscribe("device_status_changed", self.handel_on_device_status_changed_event)

      
        
    def run(self):
        while self.is_running:
            task = self.tasks.popleft()
            task()
