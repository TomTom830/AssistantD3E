import paho.mqtt.client as mqtt
import pixel


HOST = 'localhost'
PORT = 1883
pix = pixel.Pixels()

def on_connect(client, userdata, flags, rc):
    print("Connected to {0} with result code {1}".format(HOST, rc))
    # Subscribe to the hotword detected topic
    client.subscribe("hermes/hotword/default/detected")

def on_message(client, userdata, msg):
    if msg.topic == 'hermes/hotword/default/detected':
        pix.wakeup()
        print("Wakeword detected!")

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(HOST, PORT, 60)
client.loop_forever()