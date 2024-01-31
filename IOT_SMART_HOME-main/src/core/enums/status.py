from enum import Enum

class StatusEnum(Enum):
    ON = "ON"
    OFF = "OFF"

class ConnectionStatusEnum(Enum):
    CONNECTED = "CONNECTED"
    DISCONNECTED = "DISCONNECTED"
    