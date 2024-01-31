from icecream import ic

from backend.devices.DeviceReader import DeviceReader
from backend.devices.DeviceRelay import DeviceRelay
from backend.devices.DeviceSwitch import DeviceSwitch


class DeviceEventHandler:
    def __init__(self, device_adapter ) -> None:
        self.device_adapter = device_adapter

    def on_device_message_received(self, device):
        if device.last_message_received == "switch_on":
            ic("switch_on")
            
        elif device.last_message_received == "switch_off":
            ic("switch_off")
            
        elif device.last_message_received == "relay_on":
            self.turn_device_relay_on(device)

        elif device.last_message_received == "relay_off":
            self.turn_device_relay_off(device)

        ic()

    def on_device_tempreture_changed(self, device):
        msg = f"Temperature: {device.last_temp_reading}"
        self.device_adapter.send_message(device, msg)
        ic()


    def turn_device_relay_on(self,device):
        device.relay_on()
        ic()

    def turn_device_relay_off(self,device):
        device.relay_off()
        ic()
         