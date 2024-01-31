from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID
from core.schemas.air_conditioner import AirConditioner
from core.schemas.temperature_sensor import TempSensor
from core.schemas.device import Device

device_list = [
    AirConditioner(name="AC1", location="Bedroom"),
    TempSensor(name="Temperature set", location="Bedroom"),
]


class DeviceManager(BaseModel):
    devices: Optional[list[Device]] = Field(device_list)

    def get_device_by_id(self, device_id: UUID):
        for device in self.devices:
            if device.id == device_id:
                return device
        raise ValueError(f"Device with id {device_id} not found")

    def set_device(self, device: Device):
        for i, d in enumerate(self.devices):
            if d.id == device.id:
                self.devices[i] = device
                return
        self.devices.append(device)

    def turn_on_device(self, device_id: UUID):
        device = self.get_device_by_id(device_id)
        device.turn_on()
        self.set_device(device)

    def turn_off_device(self, device_id: UUID):
        device = self.get_device_by_id(device_id)
        device.turn_off()
        self.set_device(device)
