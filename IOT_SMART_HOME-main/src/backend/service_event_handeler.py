from icecream import ic

from backend.devices.DeviceMqttAdapter import DeviceMqttAdapter
from backend.devices.DeviceSwitch import DeviceSwitch


class ServiceEventHandler:
        def __init__(self, service) -> None:
            self.service = service

        def handel_on_switch_on(self, device_id):
            device_ids = self.service.device_adapter.devices_ids_dict
            device = device_ids.get(device_id)
            device.switch_on()
            self.service.device_adapter.send_message(device= device , msg="switch_on")
        
        def handel_on_switch_off(self, device_id):
            device_ids = self.service.device_adapter.devices_ids_dict
            device = device_ids.get(device_id)
            device.switch_off()
            self.service.device_adapter.send_message(device= device , msg="switch_off")

        def handel_on_device_status_changed(self):
             self.service.set_is_changed()
        

        