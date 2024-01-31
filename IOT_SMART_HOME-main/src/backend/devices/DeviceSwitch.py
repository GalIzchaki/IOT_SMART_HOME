from icecream import ic

from backend.devices.DeviceBase import DeviceBase, DeviceType
from backend.event import post_event


class DeviceSwitch(DeviceBase):
    def __init__(self):
        DeviceBase.__init__(self)
        self.type = DeviceType.INPUT
        self.is_status_ON = False

    def switch_on(self):
        if not self.is_status_ON:
            ic(f"switch on")
            self.is_status_ON = True
            post_event("device_status_changed",self)

    def switch_off(self):
        if self.is_status_ON:
            ic(f"switch off")
            self.is_status_ON = False
            post_event("device_status_changed",self)


