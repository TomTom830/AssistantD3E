#!/usr/bin/env python2
from hermes_python.hermes import Hermes
import apa102

MQTT_IP_ADDR = "localhost"
MQTT_PORT = 1883
MQTT_ADDR = "{}:{}".format(MQTT_IP_ADDR, str(MQTT_PORT))


class Pixels:
    PIXELS_N = 3

    def __init__(self):
        self.colors = [0] * 3 * self.PIXELS_N
        self.dev = apa102.APA102(num_led=self.PIXELS_N)

    def allume(self):
        colors = self.colors
        self.dev.set_pixel(3, int(colors[3 * 3]), int(colors[3 * 3 + 1]), int(colors[3 * 3 + 2]))


pixels = Pixels()


def intent_received(hermes, intent_message):
    print()
    print(intent_message.intent.intent_name)
    pixels.allume()
    print()


with Hermes(MQTT_ADDR) as h:
    h.subscribe_intents(intent_received).start()
