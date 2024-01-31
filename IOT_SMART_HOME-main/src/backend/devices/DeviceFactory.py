from backend.devices.DeviceBase import DeviceType
from backend.devices.DeviceReader import DeviceReader
from backend.devices.DeviceRelay import DeviceRelay
from backend.devices.DeviceSwitch import DeviceSwitch


class DeviceFactory:
    def create_device(self, device_type):
        requested_device = None
        if device_type == DeviceType.INPUT:
            requested_device = DeviceSwitch()
        elif device_type == DeviceType.OUTPUT:
            requested_device = DeviceRelay()
        elif device_type == DeviceType.READER:
            requested_device = DeviceReader()
        return requested_device



