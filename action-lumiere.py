#!/usr/bin/env python2
# coding: utf-8

import pixel
import requests
import tvchannel as tvc
from hermes_python.hermes import Hermes

IP_LIFE_DOMUS = "192.168.1.129"
PORT_LIFE_DOMUS = "8443"

IP_DECODEUR_ORANGE = "192.168.1.24"
PORT_DECODEUR_ORANGE = "8080"

MQTT_IP_ADDR = "localhost"
MQTT_PORT = 1883
MQTT_ADDR = "{}:{}".format(MQTT_IP_ADDR, str(MQTT_PORT))

INTENT_SET_LIGHT = "valf:lightsSetJeedom"
INTENT_TURNON_LIGHT = "valf:lightsSetJeedom"
INTENT_OPEN_BLINDS = "TomTom830:OpenCoverJeedom"
INTENT_CLOSE_BLINDS = "TomTom830:CloseCover"
INTENT_MODE = "TomTom830:ModeScenario"
INTENT_CHANNEL = "valf:TvChannelJeedom"
INTENT_VOLUME_UP = "valf:VolumeUpJeedom"
INTENT_END = "TomTom830:EndDialogue"

ALL_INTENTS = [INTENT_SET_LIGHT, INTENT_TURNON_LIGHT, INTENT_OPEN_BLINDS, INTENT_CLOSE_BLINDS, INTENT_MODE,INTENT_END,
               INTENT_CHANNEL, INTENT_VOLUME_UP]

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
            d_ouv = "0"
        requests.get("https://"+IP_LIFE_DOMUS+":"+PORT_LIFE_DOMUS+"/UniversalListen?var1=VR&var2="+d_ouv+"&var3=BureauR8R9", verify=False)
        hermes.publish_continue_session(intent_message.session_id, u"Autre choses ?", ALL_INTENTS)

def fermeStore(hermes, intent_message):
    pixels.think()
    if intent_message.slots.window_devices[0].slot_value.value.value == "stores":
        if intent_message.slots.closing_percent:
            d_ouv = str(intent_message.slots.closing_percent[0].slot_value.value.value)
        else:
            d_ouv = "100"
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
        d_lum = "100"
    requests.get("https://"+IP_LIFE_DOMUS+":"+PORT_LIFE_DOMUS+"/UniversalListen?var1=Eclairage&var2="+d_lum+"&var3=BureauR8R9", verify=False)
    hermes.publish_continue_session(intent_message.session_id, u"Autre choses ?", ALL_INTENTS)

def eteinsLumiere(hermes, intent_message):
    pixels.think()
    requests.get("https://"+IP_LIFE_DOMUS+":"+PORT_LIFE_DOMUS+"/UniversalListen?var1=Eclairage&var2=0&var3=BureauR8R9",
                 verify=False)
    hermes.publish_continue_session(intent_message.session_id, u"Autre choses ?", ALL_INTENTS)

def changeChaine(hermes, intent_message):
    pixels.think()
    channel = str(intent_message.slots.channel[0].slot_value.value.value)
    channel_int = tvc.convert_channel(channel)
    print("on met chaine {}".format(str(channel_int)))
    requests.get("http://{}:{}/remoteControl/cmd?operation=09&epg_id={}&uui=1".
                 format(IP_DECODEUR_ORANGE, PORT_DECODEUR_ORANGE, channel_int))

def monteSon(hermes, intent_message):
    pixels.think()
    print("Je monte le son")
    requests.get("http://{}:{}/remoteControl/cmd?operation=01&key=115&mode=0".
                 format(IP_DECODEUR_ORANGE, PORT_DECODEUR_ORANGE))

def baisseSon(hermes, intent_message):
    pixels.think()
    print("je baisse le son")
    requests.get("http://{}:{}/remoteControl/cmd?operation=01&key=114&mode=0".
                 format(IP_DECODEUR_ORANGE, PORT_DECODEUR_ORANGE))

def allerReplay(hermes, intent_message):
    pixels.think()
    print("je vais dans le replay")
    requests.get("http://{}:{}/remoteControl/cmd?operation=01&key=393&mode=0".
                 format(IP_DECODEUR_ORANGE, PORT_DECODEUR_ORANGE))

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
        .subscribe_intent("valf:TvChannelJeedom", changeChaine)\
        .subscribe_intent("valf:VolumeUpJeedom", monteSon)\
        .subscribe_intent("valf:VolumeDownJeedom", baisseSon)\
        .subscribe_intent("TomTom830:GoToReplay", allerReplay)\
        .subscribe_session_started(begin_session)\
        .subscribe_session_ended(end_session).start()
