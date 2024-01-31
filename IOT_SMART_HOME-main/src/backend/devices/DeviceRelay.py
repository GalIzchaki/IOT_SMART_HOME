from icecream import ic

from backend.devices.DeviceBase import DeviceBase, DeviceType
from backend.event import post_event
from core.enums.status import StatusEnum


class DeviceRelay(DeviceBase):
    def __init__(self):
        DeviceBase.__init__(self)
        self.type = DeviceType.OUTPUT
        self.is_status_ON = False

    def relay_on(self):
        self.is_status_ON = True
        post_event("device_status_changed",self)
        ic()

    def relay_off(self):
        self.is_status_ON = False
        post_event("device_status_changed",self)
        ic()

