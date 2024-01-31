import time

from backend.service import Service
from backend.devices.DeviceBase import DeviceType
from backend.devices.DeviceMqttAdapter import DeviceMqttAdapter

def test_two_devices_connection():
    service = Service()
    device_adapter = service.device_adapter

    device_adapter.create_new_device(None, DeviceType.OUTPUT, "AC1", "Home", "Living Room",
                                     "318419298_327213906_smart_heater/Home/bedroom/TS1", None)
    
    device_adapter.create_new_device(None, DeviceType.READER, "TS1", "Home", "Living Room",
                                     "318419298_327213906_smart_heater/Home/bedroom/AC_SW",
                                     '318419298_327213906_smart_heater/Home/bedroom/AC1')
    
    device_adapter.create_new_device(None, DeviceType.INPUT, "AC_SW", "Home", "Living Room",
                                     "318419298_327213906_smart_heater/Home/bedroom/AC_SW",
                                     '318419298_327213906_smart_heater/Home/bedroom/TS1')
    
    device_1 = device_adapter.devices[0]
    device_2 = device_adapter.devices[1]
    device_3 = device_adapter.devices[2]

    time.sleep(10)

    device_3.send_message("Switch ON")
    time.sleep(3)
    print(f"Device_1 received message: {device_1.last_message_received}")

    time.sleep(5)

    device_1.disconnect()
    device_2.disconnect()
    device_3.disconnect()

    assert device_3.message_to_send == "Switch ON"
    assert device_1.last_message_received == "Switch ON"

    service.__del__()





    

