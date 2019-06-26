#!/usr/bin/env python2
# coding: utf-8
"""
LED light pattern like Google Home
"""
import apa102
import time
import threading
import requests

try:
    import queue as Queue
except ImportError:
    import Queue as Queue

from hermes_python.hermes import Hermes

MQTT_IP_ADDR = "localhost"
MQTT_PORT = 1883
MQTT_ADDR = "{}:{}".format(MQTT_IP_ADDR, str(MQTT_PORT))


class Pixels:
    PIXELS_N = 3

    def __init__(self):
        self.basis = [0] * 3 * self.PIXELS_N
        self.basis[0] = 2
        self.basis[3] = 1
        self.basis[4] = 1
        self.basis[7] = 2

        self.colors = [0] * 3 * self.PIXELS_N
        self.dev = apa102.APA102(num_led=self.PIXELS_N)

        self.next = threading.Event()
        self.queue = Queue.Queue()
        self.thread = threading.Thread(target=self._run)
        self.thread.daemon = True
        self.thread.start()

    def wakeup(self, direction=0):
        def f():
            self._wakeup(direction)

        self.next.set()
        self.queue.put(f)

    def listen(self):
        self.next.set()
        self.queue.put(self._listen)

    def think(self):
        self.next.set()
        self.queue.put(self._think)

    def speak(self):
        self.next.set()
        self.queue.put(self._speak)

    def off(self):
        self.next.set()
        self.queue.put(self._off)

    def _run(self):
        while True:
            func = self.queue.get()
            func()

    def _wakeup(self, direction=0):
        for i in range(1, 25):
            colors = [i * v for v in self.basis]
            self.write(colors)
            time.sleep(0.01)

        self.colors = colors

    def _listen(self):
        for i in range(1, 25):
            colors = [i * v for v in self.basis]
            self.write(colors)
            time.sleep(0.01)

        self.colors = colors

    def _think(self):
        colors = self.colors

        self.next.clear()
        while not self.next.is_set():
            colors = colors[3:] + colors[:3]
            self.write(colors)
            time.sleep(0.2)

        t = 0.1
        for i in range(0, 5):
            colors = colors[3:] + colors[:3]
            self.write([(v * (4 - i) / 4) for v in colors])
            time.sleep(t)
            t /= 2

        # time.sleep(0.5)

        self.colors = colors

    def _speak(self):
        colors = self.colors
        gradient = -1
        position = 24

        self.next.clear()
        while not self.next.is_set():
            position += gradient
            self.write([(v * position / 24) for v in colors])

            if position == 24 or position == 4:
                gradient = -gradient
                time.sleep(0.2)
            else:
                time.sleep(0.01)

        while position > 0:
            position -= 1
            self.write([(v * position / 24) for v in colors])
            time.sleep(0.01)

        # self._off()

    def _off(self):
        self.write([0] * 3 * self.PIXELS_N)

    def write(self, colors):
        for i in range(self.PIXELS_N):
            self.dev.set_pixel(i, int(colors[3 * i]), int(colors[3 * i + 1]), int(colors[3 * i + 2]))

        self.dev.show()


def intent_received(hermes, intent_message):
    pixels = Pixels()
    print()
    print(intent_message.intent.intent_name)
    print(intent_message.slots.window_devices[0].slot_value.value.value)
    if intent_message.slots.state:
        d_ouv=(intent_message.slots.state[0].slot_value.value.value).encode('utf-8')

    if intent_message.intent.intent_name == "valf:OpenCoverJeedom":
        if intent_message.slots.window_devices[0].slot_value.value.value == "stores":
            if intent_message.slots.state:
                if d_ouv == u"à moitié":
                    requests.get("https://192.168.1.129:8443/UniversalListen?var1=VR&var2=Moitie&var3=BureauE11")
                if d_ouv == u"trois quart":
                    requests.get("https://192.168.1.129:8443/UniservalListen?var1=VR&var2=Trois_quart&var3=BureauE11")
            else:
                requests.get("https://192.168.1.129:8443/UniversalListen?var1=VR&var2=Haut&var3=BureauE11")

    if intent_message.intent.intent_name == "TomTom830:lightsSet":
        hermes.publish_end_session(intent_message.session_id, u"J'allume la lumière")
        pixels.wakeup()
    if intent_message.intent.intent_name == "bluevert:lightsTurnOff":
        hermes.publish_end_session(intent_message.session_id, u"J'éteind la lumière")
        pixels.off()
    if intent_message.intent.intent_name == "TomTom830:sendRequest":
        r = requests.get("http://linuxfr.org/")
        print(r.status_code)
        hermes.publish_end_session(intent_message.session_id, u"J'envois une requête get")
    print()



with Hermes(MQTT_ADDR) as h:
    h.subscribe_intents(intent_received).start()
