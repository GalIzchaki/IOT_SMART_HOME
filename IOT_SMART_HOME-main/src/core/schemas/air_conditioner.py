from uuid import UUID, uuid4

from pydantic import BaseModel, Field

from core.schemas.device import Device
from core.schemas.status import Status


class AirConditioner(Device):
    ...    