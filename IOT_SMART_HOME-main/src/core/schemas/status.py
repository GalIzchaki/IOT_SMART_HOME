from typing import Optional

from pydantic import BaseModel, Field

from core.enums.status import ConnectionStatusEnum, StatusEnum


class Status(BaseModel):
    status: StatusEnum = Field(StatusEnum.OFF)
    message: Optional[str]

class ConnectionStatus(BaseModel):
    connectin_status: ConnectionStatusEnum = Field(ConnectionStatusEnum.DISCONNECTED)
    message: Optional[str]