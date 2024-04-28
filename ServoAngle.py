import torch
import RPi.GPIO as GPIO
import time
import math

def xyToAngles(coordinates, img_width=640, img_height=480):
    # Extract center points
    x_center = coordinates[0] + (coordinates[2] / 2)
    y_center = coordinates[1] + (coordinates[3] / 2)

    # Camera FOVs
    horizontal_fov = 62
    vertical_fov = 48

    # Calculate the angles relative to the FOVs
    x_angle = (x_center - (img_width / 2)) * (horizontal_fov / img_width)
    y_angle = (y_center - (img_height / 2)) * (vertical_fov / img_height)

    # Assuming the servos are at the center positions when they are at 90 degrees
    # Adjust the angles based on your servo setup.
    x_servo_angle = 195 - (90 + x_angle)  # Modify this based on your servo calibration
    y_servo_angle = 150 - (90 - y_angle)  # Modify this based on your servo calibration

    # Clamp angles to servo limits if necessary
    x_servo_angle = max(0, min(180, x_servo_angle))
    y_servo_angle = max(0, min(180, y_servo_angle))
    
    set_angle(int(x_servo_angle), 1)
    set_angle(int(y_servo_angle), 2)

	


def set_angle(angle,servo):
	GPIO.setmode(GPIO.BCM)	
	
	GPIO.setup(12,GPIO.OUT)	
	pwm1 = GPIO.PWM(12, 50)
	pwm1.start(0)
	
	GPIO.setup(13,GPIO.OUT)
	pwm2 = GPIO.PWM(13, 50)
	pwm2.start(0)
	
	if servo == 1:
		pwm = pwm1
		pin = 12
	
	elif servo == 2:
		pwm = pwm2
		pin=13
	else:
		return
	
	duty = angle/18+2
	print(duty)
	GPIO.output(pin,True)	
	pwm.ChangeDutyCycle(duty)
	time.sleep(0.5)
	GPIO.output(pin,False)
	pwm.ChangeDutyCycle(0)

	



if __name__ == '__main__':
	
	
	try:
		
		print("hi")
		time.sleep(1)
		set_angle(180,1)
		time.sleep(1)
		set_angle(0,1)
		time.sleep(1)
		set_angle(180,2)
		time.sleep(1)
		set_angle(0,2)
		
		
	
	finally:
		GPIO.cleanup()
    

