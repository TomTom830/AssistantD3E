#!/usr/bin/env python2
from hermes_python.hermes import Hermes

MQTT_IP_ADDR = "localhost"
MQTT_PORT = 1883
MQTT_ADDR = "{}:{}".format(MQTT_IP_ADDR, str(MQTT_PORT))


def intent_received(hermes, intent_message):
    print()
    print(intent_message.intent.intent_name)
    print()


with Hermes(MQTT_ADDR) as h:
    h.subscribe_intents(intent_received).start()
