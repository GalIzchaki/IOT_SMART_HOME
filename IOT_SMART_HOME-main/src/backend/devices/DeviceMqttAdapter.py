import copy
import time
import uuid

from icecream import ic

from backend.ApplicationSettings import AppSettings
from backend.data.DataManager import DataManager
from backend.devices.device_event_handler import DeviceEventHandler
from backend.devices.device_listener import DeviceListener
from backend.devices.DeviceBase import DeviceBase, DeviceType
from backend.devices.DeviceFactory import DeviceFactory
from backend.devices.temprature_simulator import TempretureSimulator
from backend.event import post_event
from backend.proxies.MqttClient import MqttClient


class DeviceMqttAdapter:
    _self = None

    def __new__(cls):
        if cls._self is None:
            cls._self = super().__new__(cls)
        return cls._self
    def __init__(self):
        self.data_manager = DataManager()
        self.devices_clients_dict = dict()
        self.devices_ids_dict = dict()
        self.devices = list()
        self.mqtt_client = MqttClient()
        self.appsettings = AppSettings()
        self.mqtt_client.broker = self.appsettings.broker_url
        self.mqtt_client.port = self.appsettings.broker_port
        self.mqtt_client.username = self.appsettings.broker_username
        self.mqtt_client.password = self.appsettings.broker_password
        self.mqtt_client.topic = self.appsettings.broker_root_topic
        self.fetch_devices()
        self.device_event_handler = DeviceEventHandler(self)
        self.device_listener = DeviceListener(self)
        self.tempreture_simulator = TempretureSimulator(self)


    def fetch_devices(self):
        db_devices = self.data_manager.fetch_all_devices()
        ic(f"featch_devices : the amountr of devices is {len(db_devices)}")
        if len(db_devices) != 0:
            
            for device in db_devices:
                self.create_new_device(device[0], device[1], device[2], device[3], device[4],
                                       device[5], device[6])
                

    def assign_mqtt_client_to_device(self, device):
        mqtt_client_copy = copy.deepcopy(self.mqtt_client)
        mqtt_client_copy.client_name = f"{device.id}+{time.time_ns()}"
        mqtt_client_copy.subscribe_topic = device.topic_sub
        mqtt_client_copy.publish_topic = device.topic_pub
        self.devices_ids_dict[device.id] = device
        self.devices_clients_dict[device.id] = mqtt_client_copy


    def create_new_device(self, device_id, device_type, name, group, location, topic_sub, topic_pub):
        device_factory = DeviceFactory()
        if type(device_type) is str:
            if device_type == "DeviceType.DEFAULT":
                device_type = DeviceType.DEFAULT
            elif device_type == "DeviceType.INPUT":
                device_type = DeviceType.INPUT
            elif device_type == "DeviceType.OUTPUT":
                device_type = DeviceType.OUTPUT
            elif device_type == "DeviceType.READER":
                device_type = DeviceType.READER
        device = device_factory.create_device(device_type)
        if type(device_id) is str:
            device_id = uuid.UUID(device_id)
        if device_id is None:
            device.id = uuid.uuid4()
        else:
            device.id = device_id


        if name is not None:
            if len(name) > 1:
                device.name = name

        if group is not None:
            if len(group) > 1:
                device.group = group

        if location is not None:
            if len(location) > 1:
                device.location = location


        if topic_pub is not None:
            if len(topic_pub) > 1:
                device.topic_pub = topic_pub

        self.devices.append(device)
        self.assign_mqtt_client_to_device(device)
        self.connect(device)

    def device_connection_handler(self, client, device):
        try:
            client.on_message = self.on_message_recived
            client.connect_to()
            client.start_listening()
            while not client.connected:
                ic("Waiting for connection")
            if client.connected:
                device.is_connected = True
                client.on_on_message = self.on_message_recived
                client.subscribe_to(f"{client.topic}{device.topic_sub}")
                post_event("on_device_connect", device)
        except ConnectionError as e:
            ic("Bad connection Returned code=", e)

    def dict_return_key_by_value(self, dictionary, val):
        return_key = None
        for key, value in dictionary.items():
            if value == val:
                return_key = key
        return return_key

    def dict_return_key_by_value_client(selfself, dictionary, val):
        return_key = None
        for key, value in dictionary.items():
            if value.client == val:
                return_key = key
        return return_key

    def on_message_recived(self, client, userdata, msg):
        topic = msg.topic
        m_decode = str(msg.payload.decode("utf-8", "ignore"))
        ic("message from:" + topic, m_decode)
        device_id = self.dict_return_key_by_value_client(self.devices_clients_dict, client)
        device = self.devices_ids_dict[device_id]
        device.last_message_received = m_decode
        self.data_manager.insert_msg_to_table(client_id=device.id, device_name=device.name,
                                              topic_sub= device.topic_sub, 
                                              topic_pub= device.topic_pub,
                                              trans_type= "Message received",
                                              msg=m_decode)
        
        post_event("on_device_message_received", device)

    def connect(self, device):
        client = self.devices_clients_dict[device.id]
        self.device_connection_handler(client, device)

    def disconnect(self, device):
        client = self.devices_clients_dict[device.id]
        client.disconnect_from()
        while client.connected:
            ic("Disconnecting")
        if not client.connected:
            device.is_connected = False
            post_event("on_device_disconnect", device)


    def send_message(self, device, msg):
        client = self.devices_clients_dict[device.id]
        device.message_to_send = msg
        if device.is_connected:
            if device.topic_pub is not None:
                if len(device.topic_pub) > 5:
                    client.publish_to(device.topic_pub, device.message_to_send)
                    self.data_manager.insert_msg_to_table(client_id=device.id, device_name=device.name,
                                        topic_sub= device.topic_sub, 
                                        topic_pub= device.topic_pub,
                                        trans_type= "Sending message",
                                        msg=msg)
                    post_event("on_device_send_message", self)

    def disconnect_all_devices(self):
        for device in self.devices:
            self.disconnect(device)

    
        

