from flask import Flask
from flask_restful import Api, Resource, reqparse
from gpiozero import DigitalInputDevice
import adafruit_dht
from board import *
import time
# GPIO17
SENSOR_PIN = D17

dht11 = adafruit_dht.DHT11(SENSOR_PIN, use_pulseio=False)

app = Flask(__name__)
api = Api(app)

class DataBase(Resource):
    def get(self,id = 'none'):
        if id == 'none':
            return "Request invalid", 404
        if id == 'moisture1':
            d0_input = DigitalInputDevice(17)
	    if not d0_input.value:
		return 'threshold reached -> s1', 200
	    else:
		return 'put water -> s1', 200
        if id == 'moisture2':
            d1_input = DigitalInputDevice(18)
	    if not d1_input.value:
		return 'threshold reached -> s2', 200
	    else:
		return 'put water -> s2', 200
        if id == 'humidityAir':
            humidity = dht11.humidity
            return humidity, 200
        if id == 'temperatureAir':
            temperature = dht11.temperature
            return temperature, 200
        return "Not found", 404

