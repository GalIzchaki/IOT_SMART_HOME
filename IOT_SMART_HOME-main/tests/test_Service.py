import time

from src.backend.service import Service
from src.backend.devices.DeviceBase import DeviceType
from src.backend.devices.DeviceMqttAdapter import DeviceMqttAdapter


def test_add_device():
    service = Service()
    device_adapter = service.device_adapter
    device_adapter.create_new_device(DeviceType.BUTTON, "Test_Button", "Test_group", "Test_location", None)

    for device in device_adapter.devices:
        print(f"The device that added is: {device.name}")

    assert len(device_adapter.devices) == 1


def test_connect_device_to_broker():
    service = Service()
    device_adapter = service.device_adapter
    device_adapter.create_new_device(DeviceType.BUTTON, "Test_Button", "Test_group", "Test_location", None)
    device = device_adapter.devices[0]

    print(f"\nDevice refferance is {device}" )

    device.connect()

    assert device.is_connected

    time.sleep(10)

    device.disconnect()

    assert not device.is_connected

def test_devices_message_publish_and_received():
    service = Service()
    device_adapter = service.device_adapter
    # device_adapter.create_new_device(None, DeviceType.INPUT, "AC_SW", "Home", "Living Room",
    #                                  "318419298_327213906_smart_heater/Home/bedroom/AC_SW",
    #                                  '318419298_327213906_smart_heater/Home/bedroom/TS1')
    # device_adapter.create_new_device(None, DeviceType.OUTPUT, "AC1", "Home", "Living Room",
    #                                  "318419298_327213906_smart_heater/Home/bedroom/TS1", None)
    # device_adapter.create_new_device(None, DeviceType.READER, "TS1", "Home", "Living Room",
    #                                  "318419298_327213906_smart_heater/Home/bedroom/AC_SW",
    #                                  '318419298_327213906_smart_heater/Home/bedroom/AC1')
    device_1 = device_adapter.devices[0]
    device_2 = device_adapter.devices[1]
    device_3 = device_adapter.devices[2]

    print(f"Device refferance is {device_1}")
    print(f"Device refferance is {device_2}")
    print(f"Device refferance is {device_3}")

    time.sleep(10)

    device_2.send_message("please turn on the AC")
    print(f"Device_2 sent message: {device_2.message_to_send}")
    time.sleep(3)
    print(f"Device_1 received message: {device_1.last_message_received}")

    time.sleep(5)

    device_1.disconnect()
    device_2.disconnect()
    device_3.disconnect()

    assert device_2.message_to_send == "please turn on the AC"
    assert device_1.last_message_received == "please turn on the AC"


def test_service_init():
    service = Service()
    db_device_list = service.fetch_all_devices_from_db()
    print("")
    print(f"Devices from DB:{db_device_list}")

    device_adapter_devices_list = service.get_all_devices_from_adapter()

    print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    print("Devices from Device adapter")
    print(device_adapter_devices_list)

    for device in device_adapter_devices_list:
        print(dir(device))

def test_service_new():
    service = Service()
    time.sleep(20)
    devices = service.get_all_devices_from_adapter()
    for device in devices:
        print(device.id)

    service.turn_on_switch()

    time.sleep(20)

    service.turn_off_switch()

    time.sleep(20)

    service.shutdown()



