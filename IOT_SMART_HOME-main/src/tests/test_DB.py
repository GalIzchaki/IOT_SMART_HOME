import time

from backend.service import Service
from backend.devices.DeviceBase import DeviceType
from backend.service import Service
from backend.data.DataManager import DataManager
from backend.devices.DeviceMqttAdapter import DeviceMqttAdapter


def test_devices_message_publish_and_received():
    service = Service()
    device_adapter = service.device_adapter
    device_adapter.create_new_device(None, DeviceType.OUTPUT, "AC1", "Home", "Living Room",
                                     "318419298_327213906_smart_heater/Home/Living Room/TS1", None)
    
    device_adapter.create_new_device(None, DeviceType.READER, "TS1", "Home", "Living Room",
                                     "318419298_327213906_smart_heater/Home/Living Room/AC_SW",
                                     '318419298_327213906_smart_heater/Home/Living Room/AC1')
    
    device_adapter.create_new_device(None, DeviceType.INPUT, "AC_SW", "Home", "Living Room",
                                     "318419298_327213906_smart_heater/Home/Living Room/AC_SW",
                                     '318419298_327213906_smart_heater/Home/Living Room/TS1')



    service.save_all_devices_to_db()

    devices = service.fetch_all_devices_from_db()
    print(devices)
    assert len(devices) == 3

def test_featch_devices():
    dm = DataManager(None)
    devices = dm.fetch_all_devices()
    print(devices)
    assert len(devices) == 3

    

    # device_1 = device_adapter.devices[0]
    # device_2 = device_adapter.devices[1]
    # device_3 = device_adapter.devices[3]
    #
    # print(f"Device refferance is {device_1}")
    # print(f"Device refferance is {device_2}")
    # print(f"Device refferance is {device_3}")
    #
    # device_1.connect()
    # device_2.connect()
    # device_3.connect()
    #
    # time.sleep(10)
    #
    # device_2.send_message("this is a test message")
    # print(f"Device_2 sent message: {device_2.message_to_send}")
    # time.sleep(3)
    # print(f"Device_1 received message: {device_1.last_message_received}")
    #
    # time.sleep(5)
    #
    # device_1.disconnect()
    # device_2.disconnect()
    #
    # assert device_2.message_to_send == "this is a test message"
    # assert device_1.last_message_received == "this is a test message"