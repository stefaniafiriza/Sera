from flask import Flask
from flask_restful import Api, Resource, reqparse
from gpiozero import DigitalInputDevice
import RPi.GPIO as GPIO
import adafruit_dht
from board import *
import time

GPIO.setup(26,GPIO.OUT)
SENSOR_PIN = D22

dht11 = adafruit_dht.DHT11(SENSOR_PIN, use_pulseio=False)

app = Flask(__name__)
api = Api(app)

class DataBase(Resource):
    def get(self,id = 0):
        if id == 0:
            return "Request invalid", 404
        if id == 1:
            d0_input = DigitalInputDevice(17)
            if not d0_input.value:
                return 'threshold reached -> s1', 200
            else:
                return 'put water -> s1', 200
        if id == 2:
            d1_input = DigitalInputDevice(27)
            if not d1_input.value:
                return 'threshold reached -> s2', 200
            else:
                return 'put water -> s2', 200
        if id == 3:
            humidity = dht11.humidity
            return humidity, 200
        if id == 4:
            temperature = dht11.temperature
            return temperature, 200
        if id == 5:
            GPIO.output(26,True)
            time.sleep(5)
            GPIO.output(26,False)
            return "the plants was watered"
        return "Not found", 404
api.add_resource(DataBase,"/api","/api/<int:id>")
if __name__ == '__main__':
    app.run(debug = True)
