import time
import sqlite3

from backend.devices.DeviceBase import DeviceBase

conn = sqlite3.connect('src\\backend\\data\\smart_home.db', check_same_thread=False)
c = conn.cursor()

class DataManager:
    def __init__(self):
        self.init_broker_msg_table()
    
    def insert_device_to_db(self, device: DeviceBase):
        with conn:
            c.execute("INSERT INTO devices VALUES (:DeviceId, :DeviceType, :DeviceName, :DeviceGroup,"
                      " :DeviceLocation, :DeviceTopicSub, :DeviceTopicPub)",
                      {"DeviceId": device.id.__str__(),
                       "DeviceType": device.type.__str__(),
                       "DeviceName": device.name,
                       "DeviceGroup": device.group,
                       "DeviceLocation": device.location,
                       "DeviceTopicSub": device.topic_sub,
                       "DeviceTopicPub": device.topic_pub})

    def remove_all_devices_from_db(self):
        with conn:
            c.execute("DELETE FROM devices;")

    def insert_all_devices(self):
        self.remove_all_devices_from_db()
        devices = self.service.get_all_devices_from_adapter()
        for device in devices:
            self.insert_device_to_db(device)

    def fetch_all_devices(self) -> list:
        c.execute("SELECT * FROM devices")
        return c.fetchall()
    
    def init_broker_msg_table(self):
        with conn:
            c.execute("""CREATE TABLE IF NOT EXISTS BrokerMessages(
            TimeStamp text,
            BrokerClientID text,
            DeviceName text,
            TopicSUB text,
            TopicPub text,
            TransactionType text,
            Message text
            )""")

    def insert_msg_to_table(self, client_id, device_name, topic_sub, topic_pub, trans_type, msg ):
        if not conn.in_transaction:
            with conn:
                c.execute("INSERT INTO BrokerMessages VALUES(:TimeStamp, :BrokerClientID, :DeviceName," 
                        ":TopicSUB, :TopicPub, :TransactionType, :Message)",
                        {
                            "TimeStamp": time.asctime(time.localtime()),
                            "BrokerClientID":client_id.__str__(),
                            "DeviceName": device_name,
                            "TopicSUB": topic_sub,
                            "TopicPub": topic_pub,
                            "TransactionType": trans_type,
                            "Message": msg  
                        }
                        )
            
            