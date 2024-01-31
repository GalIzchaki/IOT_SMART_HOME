import threading
import time

from icecream import ic

from backend.devices.DeviceReader import DeviceReader
from backend.devices.DeviceRelay import DeviceRelay
from backend.devices.DeviceSwitch import DeviceSwitch
from backend.event import post_event
from backend.ApplicationSettings import AppSettings

interval = AppSettings().simulator_sampel_interval
INTERVAL = int(interval)


class TempretureSimulator:
    def __init__(self, device_adapter) -> None:
        self.device_adapter = device_adapter
        self.device_ac: DeviceRelay = device_adapter.devices[0]
        self.device_thermometer = device_adapter.devices[1] 
        self.device_switch:DeviceSwitch = device_adapter.devices[2]
        self.is_switch_on = False
        self.is_ac_on = False
        self.is_simulating = False
        self.tempreture = 25
    
    def simulate_temp(self):
        while self.is_simulating:
            self.check_enable_ac()
            if self.is_switch_on:
                if self.device_thermometer.last_temp_reading <= self.tempreture:
                    ic(self.is_ac_on)
                    if self.is_ac_on:
                        self.is_ac_on = False
                        self.turn_ac_off()
                    self.simulate_when_ac_off()

                elif self.device_thermometer.last_temp_reading >= self.tempreture:
                    ic(self.is_ac_on)
                    if not self.is_ac_on:
                        self.is_ac_on = True
                        self.turn_ac_on()
                    self.simulate_when_ac_on()

            elif not self.is_switch_on:
                self.turn_ac_off()
                self.simulate_when_ac_off()
                
            ic(self.device_thermometer.last_temp_reading)

    def turn_ac_off(self):
        self.device_adapter.send_message(self.device_thermometer,"relay_off")

    def turn_ac_on(self):
        self.device_adapter.send_message(self.device_thermometer,"relay_on")


    def simulate_when_ac_on(self):
        time.sleep(INTERVAL)
        self.device_thermometer.last_temp_reading = self.device_thermometer.last_temp_reading - 1
        post_event("device_tempreture_changed", self.device_thermometer)
        post_event("device_status_changed", self)
        ic()
            
            
    def simulate_when_ac_off(self):
        time.sleep(INTERVAL)
        self.device_thermometer.last_temp_reading = self.device_thermometer.last_temp_reading + 1
        post_event("device_tempreture_changed", self.device_thermometer)
        post_event("device_status_changed", self)
        ic()

    def check_enable_ac(self):
        if self.device_thermometer.last_message_received == "switch_on":
            self.is_switch_on = True
            self.turn_ac_on()
        elif self.device_thermometer.last_message_received == "switch_off":
            self.is_switch_on = False
            self.turn_ac_off()
        ic(self.is_switch_on)


            
    def start_simulation(self):
        self.is_simulating = True
        t1 = threading.Thread(target=self.simulate_temp)
        t1.start()
        ic()

    def stop_simulation(self):
        self.is_simulating = False




    