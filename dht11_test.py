import adafruit_dht
from board import *
import time
# GPIO17
SENSOR_PIN = D17

dht11 = adafruit_dht.DHT11(SENSOR_PIN, use_pulseio=False)
while True:
	temperature = dht11.temperature
	humidity = dht11.humidity
	print(f"Humidity= {humidity:.2f}")
	print(f"Temperature= {temperature:.2f}°C")
	time.sleep(10)