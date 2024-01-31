from datetime import datetime

import paho.mqtt.client as mqtt
from icecream import ic

from backend import ApplicationSettings


def time_format():
    return f'{datetime.now()}  Agent|> '


ic.configureOutput(prefix=time_format)
ic.configureOutput(includeContext=False)  # use True for including script file context file


class MqttClient:

    def __init__(self):
        # broker IP address:
        self.broker = ''
        self.topic = ''
        self.port = 1883
        self.client_name = ''
        self.username = ''
        self.password = ''
        self.subscribe_topic = ''
        self.publish_topic = ''
        self.publish_message = ''
        self.on_connected_to_form = ''
        self.connected = False
        self.subscribed = False

    # Setters and getters
    def set_on_connected_to_form(self, on_connected_to_form):
        self.on_connected_to_form = on_connected_to_form

    def get_broker(self):
        return self.broker

    def set_broker(self, value):
        self.broker = value

    def get_port(self):
        return self.port

    def set_port(self, value: int):
        self.port = value

    def get_client_name(self):
        return self.client_name

    def set_client_name(self, value):
        self.client_name = value

    def get_username(self):
        return self.username

    def set_username(self, value):
        self.username = value

    def get_password(self):
        return self.password

    def set_password(self, value):
        self.password = value

    def get_subscribe_topic(self):
        return self.subscribe_topic

    def set_subscribe_topic(self, value):
        self.subscribe_topic = value

    def get_publish_topic(self):
        return self.publish_topic

    def set_publish_topic(self, value):
        self.publish_topic = value

    def get_publish_message(self):
        return self.publish_message

    def set_publish_message(self, value):
        self.publish_message = value

    def on_log(self, client, userdata, level, buf):
        ic("log: " + buf)

    def on_connect(self, client, userdata, flags, rc):

        if rc == 0:
            ic("connected OK")
            self.connected = True
            #self.on_connected_to_form()
        else:
            ic("Bad connection Returned code=", rc)
            raise ConnectionError

    def on_disconnect(self, client, userdata, flags, rc=0):
        self.connected = False
        ic("DisConnected result code " + str(rc))

    def on_message(self, client, userdata, msg):
        topic = msg.topic
        m_decode = str(msg.payload.decode("utf-8", "ignore"))
        ic("message from:" + topic, m_decode)

    def connect_to(self):
        # Init paho mqtt client class
        self.client = mqtt.Client(self.client_name, clean_session=True)  # create new client instance
        self.client.on_connect = self.on_connect  # bind call back function
        self.client.on_disconnect = self.on_disconnect
        self.client.on_log = self.on_log
        self.client.on_message = self.on_message
        self.client.username_pw_set(self.username, self.password)
        ic("Connecting to broker ", self.broker)
        self.client.connect(self.broker, self.port)  # connect to broker

    def disconnect_from(self):
        self.stop_listening()
        self.client.disconnect()


    def start_listening(self):
        self.client.loop_start()

    def stop_listening(self):
        self.client.loop_stop()

    def subscribe_to(self, topic):
        if self.connected:
            self.client.subscribe(topic)
            self.subscribed = True
        else:
            ic("Can't subscribe. Connection should be established first")


    def publish_to(self, topic, message):
        if self.connected:
            self.client.publish(topic, message)
            ic(f"About to publish to topic: {topic} --> message: {message}")
        else:
            ic("Can't publish. Connection should be established first")
