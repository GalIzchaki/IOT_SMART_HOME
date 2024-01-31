import uuid
from enum import Enum

from icecream import ic

from backend.ApplicationSettings import AppSettings
from backend.event import post_event


class DeviceType(Enum):
    DEFAULT = 0
    INPUT = 1
    OUTPUT = 2
    READER = 4


class DeviceBase:
    def __init__(self):
        self.id = uuid.uuid4()
        self.device_type = DeviceType.DEFAULT
        self.name = None
        self.group = None
        self.location = None
        self.topic_pub = None
        self.is_connected = False
        self.last_message_received = None
        self.message_to_send = None
      

    @property
    def topic_sub(self):
        return f"/{self.group}/{self.location}/{self.name}"

    @topic_sub.setter
    def topic_sub(self):
        self.topic_sub = f"/{self.group}/{self.location}/{self.name}"
