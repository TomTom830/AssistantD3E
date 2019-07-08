#!/usr/bin/env python2
# coding: utf-8

import pixel
import requests
from hermes_python.hermes import Hermes

IP_LIFE_DOMUS = "192.168.1.129"
PORT_LIFE_DOMUS = "8443"

MQTT_IP_ADDR = "localhost"
MQTT_PORT = 1883
MQTT_ADDR = "{}:{}".format(MQTT_IP_ADDR, str(MQTT_PORT))

INTENT_SET_LIGHT = "valf:lightsSetJeedom"
INTENT_TURNON_LIGHT = "valf:lightsSetJeedom"
INTENT_OPEN_BLINDS = "TomTom830:OpenCoverJeedom"
INTENT_CLOSE_BLINDS = "TomTom830:CloseCover"
INTENT_MODE = "TomTom830:ModeScenario"
INTENT_END = "TomTom830:EndDialogue"

ALL_INTENTS = [INTENT_SET_LIGHT, INTENT_TURNON_LIGHT, INTENT_OPEN_BLINDS, INTENT_CLOSE_BLINDS, INTENT_MODE,INTENT_END]

pixels = pixel.Pixels()

def begin_session(hermes,param):
    pixels.listen()
    print('WAKEWORD DETECTED')

def end_session(hermes,param):
    pixels.off();
    print('END OF THE SESSION')

def ouvreStore(hermes, intent_message):
    pixels.think()
    if intent_message.slots.window_devices[0].slot_value.value.value == "stores":
        if intent_message.slots.percentage:
            d_ouv = str(intent_message.slots.percentage[0].slot_value.value.value)
        else:
            d_ouv = 0
        requests.get("https://"+IP_LIFE_DOMUS+":"+PORT_LIFE_DOMUS+"/UniversalListen?var1=VR&var2="+d_ouv+"&var3=BureauR8R9", verify=False)
        hermes.publish_continue_session(intent_message.session_id, u"Autre choses ?", ALL_INTENTS)

def fermeStore(hermes, intent_message):
    pixels.think()
    if intent_message.slots.window_devices[0].slot_value.value.value == "stores":
        if intent_message.slots.closing_percent:
            d_ouv = str(intent_message.slots.closing_percent[0].slot_value.value.value)
        else:
            d_ouv = 100
        print(d_ouv)
        requests.get("https://"+IP_LIFE_DOMUS+":"+PORT_LIFE_DOMUS+"/UniversalListen?var1=VR&var2=" + d_ouv + "&var3=BureauR8R9", verify=False)
        hermes.publish_continue_session(intent_message.session_id, u"Autre choses ?", ALL_INTENTS)

def finDialogue(hermes, intent_message):
    pixels.think()
    hermes.publish_end_session(intent_message.session_id, u"Au revoir")

def mettreLumiere(hermes, intent_message):
    pixels.think()
    if(intent_message.slots.intensity_percent):
        d_lum = str(intent_message.slots.intensity_percent[0].slot_value.value.value)
        print(d_lum)
    else:
        d_lum = 100
    requests.get("https://"+IP_LIFE_DOMUS+":"+PORT_LIFE_DOMUS+"/UniversalListen?var1=Eclairage&var2="+d_lum+"&var3=BureauR8R9", verify=False)
    hermes.publish_continue_session(intent_message.session_id, u"Autre choses ?", ALL_INTENTS)

def eteinsLumiere(hermes, intent_message):
    pixels.think()
    requests.get("https://"+IP_LIFE_DOMUS+":"+PORT_LIFE_DOMUS+"/UniversalListen?var1=Eclairage&var2=0&var3=BureauR8R9",
                 verify=False)
    hermes.publish_continue_session(intent_message.session_id, u"Autre choses ?", ALL_INTENTS)

def modeScenario(hermes, intent_message):
    pixels.think()
    print(intent_message.slots.Mode[0].slot_value.value.value)
    mode = intent_message.slots.Mode[0].slot_value.value.value
    requests.get("https://"+IP_LIFE_DOMUS+":"+PORT_LIFE_DOMUS+"/UniversalListen?var1=Scenario&var2="+mode+"&var3=BureauE11",verify=False)
    hermes.publish_continue_session(intent_message.session_id, u"Autre choses ?", ALL_INTENTS)

with Hermes(MQTT_ADDR) as h:
    h.subscribe_intent("valf:lightsSetJeedom", mettreLumiere)\
        .subscribe_intent("TomTom830:EndDialogue", finDialogue)\
        .subscribe_intent("TomTom830:CloseCover", fermeStore)\
        .subscribe_intent("TomTom830:OpenCoverJeedom", ouvreStore)\
        .subscribe_intent("valf:lightsTurnOffJeedom", eteinsLumiere)\
        .subscribe_intent("TomTom830:ModeScenario", modeScenario)\
        .subscribe_session_started(begin_session)\
        .subscribe_session_ended(end_session).start()
