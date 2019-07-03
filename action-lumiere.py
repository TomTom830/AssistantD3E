#!/usr/bin/env python2
# coding: utf-8
"""
LED light pattern like Google Home
"""
import pixel
import requests

try:
    import queue as Queue
except ImportError:
    import Queue as Queue

from hermes_python.hermes import Hermes

MQTT_IP_ADDR = "localhost"
MQTT_PORT = 1883
MQTT_ADDR = "{}:{}".format(MQTT_IP_ADDR, str(MQTT_PORT))


pixels = pixel.Pixels()

def init_wakeword(hermes,param):
    pixels.listen()
    print('WAKEWORD DETECTED')

def end_session(hermes,param):
    pixels.off();
    print('END OF THE SESSION')

def intent_received(hermes, intent_message):
    pixels.think();
    print()
    print(intent_message.intent.intent_name)
    if intent_message.slots.window_devices:
        print(intent_message.slots.window_devices[0].slot_value.value.value)
    if intent_message.slots.state:
        d_ouv = (intent_message.slots.state[0].slot_value.value.value).encode('utf-8')
        print(d_ouv)
    if intent_message.slots.window_state:
        d_ouv = (intent_message.slots.window_state[0].slot_value.value.value).encode('utf-8')
        print(d_ouv)
    if intent_message.slots.percentage:
        d_ouv = str(intent_message.slots.percentage[0].slot_value.value.value)
        print(d_ouv)
    if intent_message.slots.closing_percent:
        d_ouv = str(intent_message.slots.closing_percent[0].slot_value.value.value)
        print(d_ouv)

    if intent_message.intent.intent_name == "TomTom830:ModeScenario":
        print(intent_message.slots.Mode[0].slot_value.value.value)
        if intent_message.slots.Mode[0].slot_value.value.value == "Projection":
            requests.get("https://192.168.1.129:8443/UniversalListen?var1=Scenario&var2=Projection&var3=BureauE11",verify=False)

    if intent_message.intent.intent_name == "TomTom830:OpenCoverJeedom":
        if intent_message.slots.window_devices[0].slot_value.value.value == "stores":
            if intent_message.slots.percentage:
                requests.get("https://192.168.1.129:8443/UniversalListen?var1=VR&var2="+d_ouv+"&var3=BureauR8R9", verify=False)

            else:
                requests.get("https://192.168.1.129:8443/UniversalListen?var1=VR&var2=0&var3=BureauR8R9", verify=False)

    if intent_message.intent.intent_name == "TomTom830:CloseCover":
        if intent_message.slots.window_devices[0].slot_value.value.value == "stores":
            if intent_message.slots.closing_percent:
                requests.get("https://192.168.1.129:8443/UniversalListen?var1=VR&var2=" + d_ouv + "&var3=BureauR8R9", verify=False)

            else:
                requests.get("https://192.168.1.129:8443/UniversalListen?var1=VR&var2=100&var3=BureauR8R9", verify=False)


    if intent_message.intent.intent_name == "TomTom830:lightsSet":
        hermes.publish_end_session(intent_message.session_id, u"J'allume la lumière")
        requests.get("https://192.168.1.129:8443/UniversalListen?var1=Eclairage&var2=Allumer&var3=BureauE11", verify=False)
        pixels.wakeup()
    if intent_message.intent.intent_name == "bluevert:lightsTurnOff":
        hermes.publish_end_session(intent_message.session_id, u"J'éteind la lumière")
        requests.get("https://192.168.1.129:8443/UniversalListen?var1=Eclairage&var2=Eteindre&var3=BureauE11", verify=False)
        pixels.off()
    print()


    if intent_message.intent.intent_name == "valf:lightSetJeedom":
        d_lum = str(intent_message.slots.intensity_percent[0].slot.value.value)
        print(d_lum)
        requests.get("https://192.168.1.129:8443/UniversalListen?var1=Eclairage&var2="+d_lum+"&var3=BureauR8R9", verify=False)
        hermes.publish_end_session(intent_message.session_id, u"Je mets la lumière à "+d_lum[:2]+u" pourcent")

with Hermes(MQTT_ADDR) as h:
    h.subscribe_intents(intent_received)\
        .subscribe_session_started(init_wakeword)\
        .subscribe_session_ended(end_session).start()
