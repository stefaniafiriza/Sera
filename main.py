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

import cv2
import numpy as np
import imutils


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
            chan2 = AnalogIn(ads, ADS.P1)
            value = (chan1.voltage + chan2.voltage) / 2
            value = '{0:.2f}'.format(value)
            dictionary = {
                "sensors": {
                    "sensor": "moisture",
                    "value": value
                    }
                }
            return dictionary, 200
        if id == 3:
            humidity = dht11.humidity
            dictionary = {
                "sensors": {
                     "sensor": "humidity - air",
                     "value": humidity
                    }
                }
            return dictionary, 200
        if id == 4:
            temperature = dht11.temperature
            dictionary = {
                "sensors": {
                    "sensor": "temperature - air",
                    "value": temperature
                    }
                }
            return dictionary, 200
        if id == 5:
            GPIO.output(26,True)
            time.sleep(5)
            GPIO.output(26,False)
            return "the plants was watered"
        if id == 6:
            cam = cv2.VideoCapture(0)
            ok,img = cam.read()
            if ok:
                print("ok")
                img=cv2.resize(img,(480,600))
                hsv=cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
                
                l_b = np.array([22,28,37])
                u_b = np.array([101,248,148])
                
                mask = cv2.inRange(hsv,l_b,u_b)
                res = cv2.bitwise_and(img,img,mask=mask)
                
                median = cv2.medianBlur(mask,5)
                cnts = cv2.findContours(median.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
                cnts = imutils.grab_contours(cnts)
                green_area = 0
                for c in cnts:
                    M = cv2.moments(c)
                    if M["m00"] > 0:
                        cX = int((M["m10"]/M["m00"]))
                        cY = int((M["m01"]/M["m00"]))
                        peri = cv2.arcLength(c, True)
                        approx = cv2.approxPolyDP(c, 0.04 * peri, True)
                        cv2.drawContours(img, [c], -1, (0, 255, 0), 2)
                        area = cv2.contourArea(c)
                        green_area = green_area + area
                full_area = img.shape[0]*img.shape[1]/2
                procent = (green_area * 100) / full_area
                procent = '{0:.2f}'.format(procent)
                cv2.waitKey(0)
                dictionary = {
                    "sensors": {
                        "sensor": "Detect weeds",
                        "value": procent
                        }
                    }
                cam.release()
                cv2.imwrite("result.jpg",img)
                return dictionary, 200
        return "Not found", 404
api.add_resource(DataBase,"/api","/api/<int:id>")
if __name__ == '__main__':
    app.run(debug = True,host='0.0.0.0')
 
