from gpiozero import DigitalInputDevice
import time

d0_input = DigitalInputDevice(17)

while True:
	print(d0_input.value)
	if not d0_input.value:
		print('threshold reached')
	else:
		print('put water')
	time.sleep(3)