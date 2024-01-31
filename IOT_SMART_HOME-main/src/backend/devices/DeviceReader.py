import threading
import time

from icecream import ic

from backend.devices.DeviceBase import DeviceBase, DeviceType
from backend.event import post_event
from core.enums.status import StatusEnum


class DeviceReader(DeviceBase):
    def __init__(self):
        DeviceBase.__init__(self)
        self.type = DeviceType.READER
        self.is_status_ON = True
        self.last_temp_reading = 28