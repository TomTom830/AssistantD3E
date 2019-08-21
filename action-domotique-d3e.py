#!/usr/bin/env python3.5
# coding: utf-8

# pixel : contient des animations pour les LEDs de la carte Respeaker 2-mics
# requests : librairie necessaire pour realiser des requetes GET
# tvchannel : contient une fonction qui converti le code des chaines et numeros de chaines
# pour le decodeur Tv orange
# temp_sensor : contient une classe Python utile pour utiliser le capteur de temperature
# hermes_python.hermes : Permet l'utilisation du protocole hermes pour communiquer
# knxip : contient les fonctions permettant de controler les automates avec le protocole knx
# siteid_to_adressknx : contient une fonction qui retourne l'adresse de l'automate selon le lieu
#                       et l'automate renseigne
import pixel
import requests
import tvchannel as tvc
import temp_sensor as temperature
from hermes_python.hermes import Hermes
import knxip
import siteid_to_adressknx


#IP et PORT du module LifeDomus
IP_LIFE_DOMUS = "192.168.1.129"
PORT_LIFE_DOMUS = "8443"

#IP et PORT du decodeur Tv Orange
IP_DECODEUR_ORANGE = "192.168.1.24"
PORT_DECODEUR_ORANGE = "8080"

MQTT_IP_ADDR = "localhost"
MQTT_PORT = 1883
MQTT_ADDR = "{}:{}".format(MQTT_IP_ADDR, str(MQTT_PORT))

#On repertorie tous les intents
INTENT_TURNON_LIGHT = "TomTom830:ThelightsSet"
INTENT_TURNOFF_LIGHT = "TomTom830:TurnOff"
INTENT_OPEN_BLINDS = "TomTom830:OpenCover"
INTENT_CLOSE_BLINDS = "TomTom830:CloseCover"
INTENT_MODE = "TomTom830:ModeScenario"
INTENT_CHANNEL = "TomTom830:ThelightsSet:TvChannel"
INTENT_VOLUME_UP = "TomTom830:ThelightsSet:VolumeUp"
INTENT_VOLUME_DOWN = "TomTom830:ThelightsSet:VolumeDown"
INTENT_REPLAY_ORANGE = "TomTom830:GoToReplay"
INTENT_BACK_ORANGE = "TomTom830:GoBackOrange"
INTENT_MUTE_ORANGE = "TomTom830:ThelightsSet:VolumeMute"


ALL_INTENTS = [INTENT_TURNON_LIGHT, INTENT_OPEN_BLINDS, INTENT_CLOSE_BLINDS, INTENT_MODE,
               INTENT_VOLUME_DOWN, INTENT_REPLAY_ORANGE, INTENT_CHANNEL, INTENT_VOLUME_UP, INTENT_BACK_ORANGE,
               INTENT_MUTE_ORANGE]

# Creation d un objet pixels qui va nous servir a lancer l animation des LEDs
pixels = pixel.Pixels()

# Fonction appelee des que le wakeword est detecte
def begin_session(hermes,param):
    pixels.listen()
    #asyncio.set_event_loop(asyncio.new_event_loop())
    print('WAKEWORD DETECTED')

# Fonction appelee a la fin d une requete vocale
def end_session(hermes,param):
    pixels.off()
    print('END OF THE SESSION')

# Action associee a l intent de demande de la temperature
# Cette fonction se termine par un message vocal qui renseigne la temperature
def donneTemperature(hermes, intent_message):
    sensor = temperature.GroveTemperatureHumiditySensorSHT3x()

    temp, humidity = sensor.read()
    print('Temperature in Celsius is {:.2f} C'.format(temp))
    print('Relative Humidity is {:.2f} %'.format(humidity))

    hermes.publish_end_session(intent_message.session_id, "Il fait {:.1f} degrai".format(temp))

# Action associee a l intent ouvrir le store
# Cette fonction envoyait d'abord une requete http get au module Lifedomus pour executer l'action
# puis avec la nouvelle solution elle envoi directement une requete knx ip sans passer par le
# module Lifedomus grace a la fonction "controle_store" de knxip qui utilise une fonction asynchrone
# la fonction se termine avec un message vocal
def ouvreStore(hermes, intent_message):
    pixels.think()
    if intent_message.slots.window_devices[0].slot_value.value.value == "stores":
        if intent_message.slots.percentage:
            d_ouv = str(intent_message.slots.percentage[0].slot_value.value.value)
        else:
            d_ouv = "0"
    d_ouv = int(d_ouv[:-2])

    # requests.get(
    #    "https://" + IP_LIFE_DOMUS + ":" + PORT_LIFE_DOMUS + "/UniversalListen?var1=VR&var2=" + d_ouv + "&var3=" + intent_message.site_id,
    #    timeout=5, verify=False)

    adr_store = siteid_to_adressknx.convert_siteid_to_adressknx(intent_message.site_id, "store")
    knxip.controle_store(d_ouv, adr_store, intent_message.site_id)
    hermes.publish_end_session(intent_message.session_id, "J'ouvre le store à {} pourcent dans le {}"
                               .format(d_ouv, intent_message.site_id))

# Action associee a l intent fermer le store
# L'algorithme est me même que pour la fonction précédente
def fermeStore(hermes, intent_message):
    pixels.think()
    if intent_message.slots.window_devices[0].slot_value.value.value == "stores":
        if intent_message.slots.closing_percent:
            d_ouv = str(intent_message.slots.closing_percent[0].slot_value.value.value)
        else:
            d_ouv = "100"
        d_ouv = int(d_ouv[:-2])

        # requests.get(
        #    "https://" + IP_LIFE_DOMUS + ":" + PORT_LIFE_DOMUS + "/UniversalListen?var1=VR&var2=" + d_ouv + "&var3=" + intent_message.site_id,
        #    timeout=5, verify=False)

        adr_store = siteid_to_adressknx.convert_siteid_to_adressknx(intent_message.site_id, "store")
        knxip.controle_store(d_ouv, adr_store, intent_message.site_id)
        hermes.publish_end_session(intent_message.session_id, "Je ferme le store à {} pourcent dans le {}"
                                   .format(d_ouv, intent_message.site_id))

# Action associee a l intent allumer la lumiere
# Cette fonction elle aussi implantait la premiere solution (puis mise en commentaire)
# c est a dire l envoi d une requete http au module lifedomus pour controler les automates
# elle envoi desormais elle meme la requete knxip aux automates en renseignant
# l'intensite lumineuse de la lumiere
# l'intensite lumineuse variant de 0 a 255 il faut convertir le pourcentage en
# intensite lumineuse le resultat est stocke dans la variable d_lum
# Elle fini par un message vocal
def mettreLumiere(hermes, intent_message):
    pixels.think()
    print("dans le mettreLumiere")
    if(intent_message.slots.intensity_percent):
        d_lum = str(intent_message.slots.intensity_percent[0].slot_value.value.value)
        print(d_lum)
    else:
        d_lum = "100"
    d_lum = float(d_lum[:-2])
    d_lum = int((255*d_lum)/100)

    #requests.get(
    #    "https://" + IP_LIFE_DOMUS + ":" + PORT_LIFE_DOMUS + "/UniversalListen?var1=Eclairage&var2=" + d_lum + "&var3=" + intent_message.site_id,
    #    timeout=5, verify=False)

    adr_lum = siteid_to_adressknx.convert_siteid_to_adressknx(intent_message.site_id, "lumiere")
    knxip.controle_lumiere(d_lum, adr_lum, intent_message.site_id)
    hermes.publish_end_session(intent_message.session_id, u"J'allume la lumière à {} pourcent dans le {}"
                               .format(d_lum, intent_message.site_id))

# Action associe l intent eteindre la lumiere
# Fonctionnement identique a la fonction precedente avec l intensite a 0
# elle termine par un message vocal
def eteinsLumiere(hermes, intent_message):
    pixels.think()

    #requests.get(
    #    "https://" + IP_LIFE_DOMUS + ":" + PORT_LIFE_DOMUS + "/UniversalListen?var1=Eclairage&var2=0&var3=" + intent_message.site_id,
    #    timeout=5, verify=False)

    adr_lum = siteid_to_adressknx.convert_siteid_to_adressknx(intent_message.site_id, "lumiere")
    knxip.controle_lumiere(0, adr_lum, intent_message.site_id)
    hermes.publish_end_session(intent_message.session_id, u"J'éteins la lumière dans le "+intent_message.site_id)


# Action associee a l intent lancer un scenario
# Cette fonction envoi une requete http au module Lifedomus pour lancer un scenario
def modeScenario(hermes, intent_message):
    pixels.think()
    print(intent_message.slots.Mode[0].slot_value.value.value)
    mode = intent_message.slots.Mode[0].slot_value.value.value
    requests.get("https://"+IP_LIFE_DOMUS+":"+PORT_LIFE_DOMUS+"/UniversalListen?var1=Scenario&var2="+mode+"&var3="+intent_message.site_id,
                 timeout=5, verify=False)
    hermes.publish_end_session(intent_message.session_id, u"Je mets le mode "+mode+u"dans le "+intent_message.site_id)


# Action associee a l intent de changement de chaine
# Cette fonction envoie une requete http au decodeur Tv Orange
# Il y a un code associe a chaque chaine Tv la traduction code numero de chaine est
# effectue par la fonction convert_channel
def changeChaine(hermes, intent_message):
    pixels.think()
    channel = str(intent_message.slots.channel[0].slot_value.value.value)
    channel_int = tvc.convert_channel(channel)
    print("on met chaine {}".format(str(channel_int)))
    requests.get("http://{}:{}/remoteControl/cmd?operation=09&epg_id={}&uui=1".
                 format(IP_DECODEUR_ORANGE, PORT_DECODEUR_ORANGE, channel_int), timeout=5)

# Action associe a l intent augmente le son
# Cette fonction envoi une requete http au decodeur Tv Orange et termine par un message vocal
def monteSon(hermes, intent_message):
    pixels.think()
    print("Je monte le son")
    requests.get("http://{}:{}/remoteControl/cmd?operation=01&key=115&mode=0".
                 format(IP_DECODEUR_ORANGE, PORT_DECODEUR_ORANGE), timeout=5)
    print("valeur du session_id : {}".format(intent_message.site_id))

# Action associe a l intent baisse le son
# Cette fonction envoi une requete http au decodeur Tv Orange et termine par un message vocal
def baisseSon(hermes, intent_message):
    pixels.think()
    print("je baisse le son")
    requests.get("http://{}:{}/remoteControl/cmd?operation=01&key=114&mode=0".
                 format(IP_DECODEUR_ORANGE, PORT_DECODEUR_ORANGE), timeout=5)
    print("valeur du session_id : {}".format(intent_message.site_id))

# Action associe a l intent coupe le son
# Cette fonction envoi une requete http au decodeur Tv Orange et termine par un message vocal
def coupeSon(hermes, intent_message):
    pixels.think()
    print("Je coupe le son test")
    print("valeur du session_id : {}".format(intent_message.site_id))
    requests.get("http://{}:{}/remoteControl/cmd?operation=01&key=113&mode=0".
                 format(IP_DECODEUR_ORANGE, PORT_DECODEUR_ORANGE), timeout=5)

# Action associee a l intent aller dans le replay du decodeur Orange Tv
def allerReplay(hermes, intent_message):
    pixels.think()
    print("je vais dans le replay")
    requests.get("http://{}:{}/remoteControl/cmd?operation=01&key=393&mode=0".
                 format(IP_DECODEUR_ORANGE, PORT_DECODEUR_ORANGE), timeout=5)

# Action associee a l intent retour (bouton back sur la telecommande orange Tv)
def revenirOrange(hermes, intent_message):
    pixels.think()
    print("Je reviens avant")
    requests.get("http://{}:{}/remoteControl/cmd?operation=01&key=158&mode=0".
                 format(IP_DECODEUR_ORANGE, PORT_DECODEUR_ORANGE), timeout=5)


# Ici on associe a chaque intent une fonction qui sera chargera de traiter cet
# intent
# On associe egalement une fonction qui est appelee a chaque debut de session "begin_session" c est
# a dire une fonction qui s execute lorsque le wakeword est entendu
# On associe egalement une fonction appelee a chaque fin de session "end_session"
with Hermes(MQTT_ADDR) as h:
    h.subscribe_intent("TomTom830:TheLightsSet", mettreLumiere)\
        .subscribe_intent("TomTom830:CloseCover", fermeStore)\
        .subscribe_intent("TomTom830:OpenCover", ouvreStore)\
        .subscribe_intent("TomTom830:TurnOff", eteinsLumiere)\
        .subscribe_intent("TomTom830:ModeScenario", modeScenario)\
        .subscribe_intent("TomTom830:TvChannel", changeChaine)\
        .subscribe_intent("TomTom830:VolumeUp", monteSon)\
        .subscribe_intent("TomTom830:VolumeDown", baisseSon)\
        .subscribe_intent("TomTom830:GoToReplay", allerReplay)\
        .subscribe_intent("TomTom830:GoBackOrange", revenirOrange)\
        .subscribe_intent("TomTom830:VolumeMute", coupeSon)\
        .subscribe_intent("TomTom830:EntityStateValue", donneTemperature)\
        .subscribe_session_started(begin_session)\
        .subscribe_session_ended(end_session).start()
