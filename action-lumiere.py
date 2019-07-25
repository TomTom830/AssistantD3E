#!/usr/bin/env python2
# coding: utf-8

import pixel
import requests
import tvchannel as tvc
import temp_sensor as temperature
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
INTENT_VOLUME_DOWN = "valf:VolumeDownJeedom"
INTENT_REPLAY_ORANGE = "TomTom830:GoToReplay"
INTENT_BACK_ORANGE = "TomTom830:GoBackOrange"
INTENT_MUTE_ORANGE = "valf:VolumeMuteJeedom"
INTENT_END = "TomTom830:EndDialogue"


ALL_INTENTS = [INTENT_SET_LIGHT, INTENT_TURNON_LIGHT, INTENT_OPEN_BLINDS, INTENT_CLOSE_BLINDS, INTENT_MODE,
               INTENT_VOLUME_DOWN, INTENT_REPLAY_ORANGE, INTENT_CHANNEL, INTENT_VOLUME_UP, INTENT_BACK_ORANGE,
               INTENT_MUTE_ORANGE, INTENT_END]

pixels = pixel.Pixels()

def begin_session(hermes,param):
    pixels.listen()
    print('WAKEWORD DETECTED')

def end_session(hermes,param):
    pixels.off();
    print('END OF THE SESSION')

def donneTemperature(hermes, intent_message):
    sensor = temperature.GroveTemperatureHumiditySensorSHT3x()

    temp, humidity = sensor.read()
    print('Temperature in Celsius is {:.2f} C'.format(temp))
    print('Relative Humidity is {:.2f} %'.format(humidity))

    hermes.publish_end_session(intent_message.session_id, u"Il fait " + temp + u" degrés")

def ouvreStore(hermes, intent_message):
    pixels.think()
    if intent_message.slots.window_devices[0].slot_value.value.value == "stores":
        if intent_message.slots.percentage:
            d_ouv = str(intent_message.slots.percentage[0].slot_value.value.value)
        else:
            d_ouv = "0"
        requests.get("https://"+IP_LIFE_DOMUS+":"+PORT_LIFE_DOMUS+"/UniversalListen?var1=VR&var2="+d_ouv+"&var3="+intent_message.site_id,
                     timeout=5, verify=False)
        hermes.publish_end_session(intent_message.session_id, "Je ferme le store dans le " + intent_message.site_id)

def fermeStore(hermes, intent_message):
    pixels.think()
    if intent_message.slots.window_devices[0].slot_value.value.value == "stores":
        if intent_message.slots.closing_percent:
            d_ouv = str(intent_message.slots.closing_percent[0].slot_value.value.value)
        else:
            d_ouv = "100"
        print(d_ouv)
        requests.get("https://"+IP_LIFE_DOMUS+":"+PORT_LIFE_DOMUS+"/UniversalListen?var1=VR&var2="+d_ouv+"&var3="+intent_message.site_id,
                     timeout=5, verify=False)
        hermes.publish_end_session(intent_message.session_id, "Je ferme le store dans le " + intent_message.site_id)

def mettreLumiere(hermes, intent_message):
    pixels.think()
    if(intent_message.slots.intensity_percent):
        d_lum = str(intent_message.slots.intensity_percent[0].slot_value.value.value)
        print(d_lum)
    else:
        d_lum = "100"
    requests.get("https://"+IP_LIFE_DOMUS+":"+PORT_LIFE_DOMUS+"/UniversalListen?var1=Eclairage&var2="+d_lum+"&var3="+intent_message.site_id,
                 timeout=5, verify=False)
    hermes.publish_end_session(intent_message.session_id, u"J'allume la lumière dans le " + intent_message.site_id)

def eteinsLumiere(hermes, intent_message):
    pixels.think()
    requests.get("https://"+IP_LIFE_DOMUS+":"+PORT_LIFE_DOMUS+"/UniversalListen?var1=Eclairage&var2=0&var3="+intent_message.site_id,
                 verify=False, timeout=5)
    hermes.publish_end_session(intent_message.session_id, u"J'éteins la lumière dans le "+intent_message.site_id)


def changeChaine(hermes, intent_message):
    pixels.think()
    channel = str(intent_message.slots.channel[0].slot_value.value.value)
    channel_int = tvc.convert_channel(channel)
    print("on met chaine {}".format(str(channel_int)))
    requests.get("http://{}:{}/remoteControl/cmd?operation=09&epg_id={}&uui=1".
                 format(IP_DECODEUR_ORANGE, PORT_DECODEUR_ORANGE, channel_int), timeout=5)

def monteSon(hermes, intent_message):
    pixels.think()
    print("Je monte le son")
    requests.get("http://{}:{}/remoteControl/cmd?operation=01&key=115&mode=0".
                 format(IP_DECODEUR_ORANGE, PORT_DECODEUR_ORANGE), timeout=5)
    print("valeur du session_id : {}".format(intent_message.site_id))

def baisseSon(hermes, intent_message):
    pixels.think()
    print("je baisse le son")
    requests.get("http://{}:{}/remoteControl/cmd?operation=01&key=114&mode=0".
                 format(IP_DECODEUR_ORANGE, PORT_DECODEUR_ORANGE), timeout=5)
    print("valeur du session_id : {}".format(intent_message.site_id))

def coupeSon(hermes, intent_message):
    pixels.think()
    print("Je coupe le son test")
    print("valeur du session_id : {}".format(intent_message.site_id))
    requests.get("http://{}:{}/remoteControl/cmd?operation=01&key=113&mode=0".
                 format(IP_DECODEUR_ORANGE, PORT_DECODEUR_ORANGE), timeout=5)

def allerReplay(hermes, intent_message):
    pixels.think()
    print("je vais dans le replay")
    requests.get("http://{}:{}/remoteControl/cmd?operation=01&key=393&mode=0".
                 format(IP_DECODEUR_ORANGE, PORT_DECODEUR_ORANGE), timeout=5)

def revenirOrange(hermes, intent_message):
    pixels.think()
    print("Je reviens avant")
    requests.get("http://{}:{}/remoteControl/cmd?operation=01&key=158&mode=0".
                 format(IP_DECODEUR_ORANGE, PORT_DECODEUR_ORANGE), timeout=5)

def modeScenario(hermes, intent_message):
    pixels.think()
    print(intent_message.slots.Mode[0].slot_value.value.value)
    mode = intent_message.slots.Mode[0].slot_value.value.value
    requests.get("https://"+IP_LIFE_DOMUS+":"+PORT_LIFE_DOMUS+"/UniversalListen?var1=Scenario&var2="+mode+"&var3="+intent_message.site_id,
                 timeout=5, verify=False)
    hermes.publish_end_session(intent_message.session_id, u"Je mets le mode "+mode+u"dans le "+intent_message.site_id)

def ErrorIntent(hermes):
    pixels.colors = [255, 0, 0, 255, 0, 0, 255, 0, 0]
    pixels.speak()


with Hermes(MQTT_ADDR) as h:
    h.subscribe_intent("valf:lightsSetJeedom", mettreLumiere)\
        .subscribe_intent("TomTom830:CloseCover", fermeStore)\
        .subscribe_intent("TomTom830:OpenCoverJeedom", ouvreStore)\
        .subscribe_intent("valf:lightsTurnOffJeedom", eteinsLumiere)\
        .subscribe_intent("TomTom830:ModeScenario", modeScenario)\
        .subscribe_intent("valf:TvChannelJeedom", changeChaine)\
        .subscribe_intent("valf:VolumeUpJeedom", monteSon)\
        .subscribe_intent("valf:VolumeDownJeedom", baisseSon)\
        .subscribe_intent("TomTom830:GoToReplay", allerReplay)\
        .subscribe_intent("TomTom830:GoBackOrange", revenirOrange)\
        .subscribe_intent("valf:VolumeMuteJeedom", coupeSon)\
        .subscribe_intent("valf:EntityStateValueJeedom", donneTemperature)\
        .subscribe_intent_not_recognized(ErrorIntent)\
        .subscribe_session_started(begin_session)\
        .subscribe_session_ended(end_session).start()
