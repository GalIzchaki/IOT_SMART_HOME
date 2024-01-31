from icecream import ic

from backend.devices.device_listener import DeviceListener
from backend.devices.DeviceMqttAdapter import DeviceMqttAdapter
from backend.devices.DeviceSwitch import DeviceSwitch
from backend.devices.temprature_simulator import TempretureSimulator
from backend.event import post_event
from backend.service_event_handeler import ServiceEventHandler
from backend.service_listener import ServiceListener


class Service:
    _self = None

    def __new__(cls):
        if cls._self is None:
            cls._self = super().__new__(cls)
        return cls._self

    def __init__(self):
        self.device_adapter = DeviceMqttAdapter()
        self.service_listener = ServiceListener(self)
        self.service_handeler = ServiceEventHandler(self)
        self.simulator = TempretureSimulator(self.device_adapter)
        self.simulator.start_simulation()
        self.Device_switch_id = self.get_switch_from_devices()
        self.is_changed = False

    def get_switch_from_devices(self):
        devices = self.device_adapter.devices
        for device in devices:
            if (type(device) is DeviceSwitch):
                return device.id

    def start_simulation(self):
        self.simulator.start_simulation

    def feach_devices(self):
        return self.device_adapter.devices
    
    def turn_on_switch(self):
        devices = self.device_adapter.devices
        post_event("turn_on_device", self.Device_switch_id)

    def turn_off_switch(self):
        post_event("turn_off_device", self.Device_switch_id)

    def set_is_changed(self):
        self.is_changed = True

    def set_tempreture(self, temp):
        self.simulator.tempreture = temp


    def run(self):
        self.service_listener.run()

    def shutdown(self):
        self.simulator.stop_simulation()
        self.service_listener.is_running = False

    def __del__(self):
        ic(f"service : distractor invoked disconnect all devices")
        self.device_adapter.disconnect_all_devices()





