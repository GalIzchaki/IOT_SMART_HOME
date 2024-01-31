from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4

from pydantic import BaseModel, Field

from core.enums.status import StatusEnum
from core.schemas.device import Device


class TempSensor(Device):
    status: StatusEnum = Field(default=StatusEnum.ON)
    temperature: Optional[float]
    last_update: Optional[datetime]
