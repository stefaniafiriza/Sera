from flask import Flask
from flask_restful import Api, Resource, reqparse
from gpiozero import DigitalInputDevice
import RPi.GPIO as GPIO
import adafruit_dht
from board import *
import busio
import board
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
import time

GPIO.setup(26,GPIO.OUT)
SENSOR_PIN = D22

dht11 = adafruit_dht.DHT11(SENSOR_PIN, use_pulseio=False)
i2c = busio.I2C(board.SCL,board.SDA)
ads = ADS.ADS1115(i2c)

app = Flask(__name__)
api = Api(app)

class DataBase(Resource):
    def get(self,id = 0):
        print('"sensor": [\n{')
        if id == 0:
            return "Request invalid", 404
        if id == 1:
            chan1 = AnalogIn(ads, ADS.P0)
            dictionary = {
                "sensors": {
                    "sensor": "moisture 1",
                    "value": chan1.voltage
                    }
                }
            return dictionary, 200
        if id == 2:
            chan2 = AnalogIn(ads, ADS.P1 )
            dictionary = {
                "sensors": {
                    "sensor": "moisture 2",
                    "value": chan2.voltage
                    }
                }
            return dictionary, 200
        if id == 3:
            humidity = dht11.humidity
            dictionary = {
                "sensors": {
                     "sensor": "humidity - aer",
                     "value": humidity
                    }
                }
            return dictionary, 200
        if id == 4:
            temperature = dht11.temperature
            dictionary = {
                "sensors": {
                    "sensor": "temperature - aer",
                    "value": temperature
                    }
                }
            return dictionary, 200
        if id == 5:
            GPIO.output(26,True)
            time.sleep(5)
            GPIO.output(26,False)
            return "the plants was watered"
        return "Not found", 404
api.add_resource(DataBase,"/api","/api/<int:id>")
if __name__ == '__main__':
    app.run(debug = True,host='0.0.0.0')
