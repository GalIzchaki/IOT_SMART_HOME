from uuid import UUID, uuid4

from pydantic import BaseModel, Field

from core.enums.status import StatusEnum
from core.schemas.status import ConnectionStatus, Status


class Device(Status):
    id: UUID = Field(default_factory=uuid4)
    name: str
    location: str
    connection_status: ConnectionStatus
    status: Status = Field(default_factory=Status)

    def turn_on(self):
        if self.status == StatusEnum.ON:
            raise ValueError("Device is already on")

        if self.status == StatusEnum.OFF:
            self.status = StatusEnum.ON
        else:
            raise ValueError("Device is in unknown state")

    def turn_off(self):
        if self.status == StatusEnum.OFF:
            raise ValueError("Device is already off")

        if self.status == StatusEnum.ON:
            self.status = StatusEnum.OFF
        else:
            raise ValueError("Device is in unknown state")
