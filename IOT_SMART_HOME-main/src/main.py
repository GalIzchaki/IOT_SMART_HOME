import time

import streamlit as st

from backend.devices.DeviceBase import DeviceBase
from controller.control import Controller
from core.enums.status import StatusEnum


@st.cache_resource
def get_controller():
    return Controller()

controller = get_controller()

page_bg_img = """
<style>
[data-testid="stAppViewContainer"]{
background-color: #0c0c1f;
opacity: 0.8;
background-image:  radial-gradient(#ee4b10 0.8500000000000001px, transparent 0.8500000000000001px), radial-gradient(#ee4b10 0.8500000000000001px, #0c0c1f 0.8500000000000001px);
background-size: 34px 34px;
background-position: 0 0,17px 17px;


</style>

"""

st.markdown(page_bg_img,unsafe_allow_html=True)

st.title("Smart Heater For The Winter")

def state_emoji(status):
    if status == True:
        return ":large_green_circle:"
    elif status == False:
        return ":red_circle:"


def status_emoji(status):
    if status:
        return ":large_green_circle:"
    
    return ":black_circle:"

def device_emoji(device_name):
    if device_name == "TS1":
        return ":thermometer:"
    elif device_name == "AC1":
        return ":fire:"
    elif device_name == "AC_SW":
        return "🖲️"

def refresh():
    controller.service.feach_devices()

def on_click_turn_on():
    controller.service.turn_on_switch()

def on_click_turn_off():
    controller.service.turn_off_switch()


for device in controller.service.device_adapter.devices:
    col1, col2, col3 = st.columns([2, 1, 3])
    ##col1.write(f"{device_emoji(device.name)} {device.name} @ {'Bedroom'}")
    ##col1.write(f" Device State {state_emoji(device.is_status_ON)} Connection {status_emoji(device.is_connected)}")
    col1.write(f'<span style="color: white;">{device_emoji(device.name)} {device.name} @ {"BedRoom"}</span>', unsafe_allow_html=True)
    col1.write(f'<span style="color: white;"> Device State {state_emoji(device.is_status_ON)} Connection {status_emoji(device.is_connected)}</span>', unsafe_allow_html=True)


    if device.name == "AC1":
        tempeture = col2.slider("Set temperature heater target ", 22,50,25)
        controller.service.set_tempreture(tempeture)
        
    if device.name == "TS1" and device.is_connected == True:
        col2.metric(label="IFEEL", value=f"{device.last_temp_reading} °C")

    if device.name == "AC_SW":
        if device.is_status_ON == True:
            turn_off_button = col2.button(
                "OFF",
                key=f"turn_off_switch",
                on_click=on_click_turn_off,

            )
        elif device.is_status_ON == False:
            turn_on_button = col2.button(
                "ON",
                key=f"turn_on_switch",
                on_click=on_click_turn_on,

            )


            
while True:
    if controller.service.is_changed:
        controller.service.is_changed = False
        st.experimental_rerun()
    time.sleep(1)





