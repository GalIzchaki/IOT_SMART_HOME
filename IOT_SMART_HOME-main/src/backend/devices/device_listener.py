from backend.devices.device_event_handler import DeviceEventHandler
from backend.devices.DeviceBase import DeviceBase
from backend.event import subscribe


class DeviceListener:
    def __init__(self, device_adapter):
        self.handler = DeviceEventHandler(device_adapter)
        self.setup_device_event_handlers()


    def handel_on_device_message_received_event(self, device):
        self.handler.on_device_message_received(device)

    def handel_on_device_tempreture_event(self, device):
        self.handler.on_device_tempreture_changed(device)

    def setup_device_event_handlers(self):
        subscribe("on_device_message_received", self.handel_on_device_message_received_event)
        subscribe("device_tempreture_changed", self.handel_on_device_tempreture_event)
        
        
