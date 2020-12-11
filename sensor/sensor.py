import json
import time
import random
import paho.mqtt.client as mqtt


class Sensor:
    def __init__(self):
        print("Sensor initialized")
        self.id = 1
        self.timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
        self.temperature = random.randrange(30, 40)
        self.bpm = random.randrange(30, 220)
        self.cpu = random.uniform(0,1)

    def __str__(self):
        return "id_patient: " + str(self.id) + "time: " + str(self.timestamp) + "\n" + "temperature: " + str(self.temperature) + \
               "\n" + "bpm: " + str(self.bpm)

    def get_data(self):
        self.timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
        self.temperature = random.randrange(30, 40)
        self.bpm = random.randrange(30, 220)
        self.cpu = random.uniform(0,1)
        data_set = {"id": self.id, "time": self.timestamp, "temp": self.temperature, "bpm": self.bpm, "cpu": self.cpu}
        json_dump = json.dumps(data_set)

        return json_dump


# MQTT publisher config
broker = "mosquitto"
port = 1883
keep_alive = 60

topic = 'test'

client = mqtt.Client()
client.connect(broker, port, keep_alive)
sensor = Sensor()

# MQTT publishing messages to IoT Broker
while True:
    time.sleep(5)
    client.publish(topic, sensor.get_data())

client.disconnect()
