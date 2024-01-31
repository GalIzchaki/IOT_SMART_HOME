from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field, validator

from backend.service import Service
from core.schemas.air_conditioner import AirConditioner
from core.schemas.temperature_sensor import TempSensor


class Controller(BaseModel):
    service: Service = Field(default_factory=Service)
    class Config:
        arbitrary_types_allowed = True
    def __del__(self):
        self.service.shutdwon()