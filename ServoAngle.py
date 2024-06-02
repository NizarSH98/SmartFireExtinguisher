import RPi.GPIO as GPIO
import time
import serial
import numpy as np
import matplotlib.pyplot as plt
from detect import predict_fire_status

# Open the serial port
ser = serial.Serial('/dev/serial0', 115200, timeout=0.1)
# Constants
HORIZONTAL_FOV = 62
VERTICAL_FOV = 48
IMG_WIDTH = 640
IMG_HEIGHT = 480

HANDSHAKE_PIN = 21  #pin for handshake
RELAY_PIN = 18
is_initialized = False
previous_x_servo_angle = 0
previous_angle=0
global right
right = None

ForestTree = True
SERIAL_PORT = '/dev/serial0'
BAUDRATE = 115200

def read_data_from_nodemcu():
    try:
        line = ser.readline()
        line = line.decode('utf-8', errors='ignore').strip()  # Decode with error handling
        if line:
            if line.startswith("P:"):
                end_index = line.find("#")
                if end_index != -1:
                    data = line[2:end_index]  # Extract data between 'P:' and '#'
                    all_values = data.split(',')
                    pixel_values = [float(val) for val in all_values[:-1]]  # All values except the last one
                    sensor_value = float(all_values[-1])  # The last value
                    return pixel_values, sensor_value  # Return the pixel values and sensor value
                else:
                    print("Invalid pixel data format: '#' not found")
        return None, None  # Return None if no valid data is received
    except Exception as e:
        print(f"Error reading from serial port: {e}")
        return None, None

        
        

def xyToAngles(coordinates,previous_x_servo_angle):
    global is_initialized
    is_initialized = True
    if not is_initialized:
        # Initial position setup
        initial_x_angle = 90  # Set your desired initial x angle
        initial_y_angle = 140  # Recalibrated initial y angle to align with the camera
        
        move_servo('S1',int(initial_x_angle))
        move_servo('S2',int(initial_y_angle))
        
        
        
        previous_x_servo_angle = initial_x_angle

        print(f"Initial setup: x_angle={initial_x_angle}, y_angle={initial_y_angle}")

        # Mark as initialized
        is_initialized = True
        
    x_center = coordinates[0] + (coordinates[2] / 2)
    y_center = coordinates[1] + (coordinates[3] / 2)

    x_angle_offset = (x_center - IMG_WIDTH / 2) * (HORIZONTAL_FOV / IMG_WIDTH)
    y_angle = (( IMG_HEIGHT / 2 ) -y_center) * (VERTICAL_FOV / IMG_HEIGHT) + 140
    
    x_servo_angle = previous_x_servo_angle + x_angle_offset
    
    print("offset x_angle:", x_angle_offset)
    # Apply clamping
    x_servo_angle = max(15, min(150, x_servo_angle))
    y_angle = max(120, min(160, y_angle))

    print("Target x_angle:", x_servo_angle)
    print("Target y_angle:", y_angle)
    
    move_servo('S1',str(int(x_servo_angle)))
    
    move_servo('S2',str(int(y_angle)))
    time.sleep(1.65)
    # Define the timeout duration in seconds
    timeout_duration = 5.0
    start_time = time.time()
    pixel_values , mq2 = read_data_from_nodemcu()
    while pixel_values is None:
        command = f"sending:{1}\n"
        ser.write(command.encode())
        pixel_values, mq2 = read_data_from_nodemcu()
        time.sleep(0.1)
        
        # Check if the timeout duration has been exceeded
        if time.time() - start_time > timeout_duration:
            print("Timeout: No valid data received within the specified duration")
            break
    
    command = f"sending:{0}\n"
    ser.write(command.encode())
    print("Thermal Array:",pixel_values)
    print("Gas sensor:",mq2)

    previous_x_servo_angle = x_servo_angle
    
    time.sleep(0.5)
    if(ForestTree):
        pixel_values = OneToTwoD(pixel_values)
        if (pixel_values != None):
            Relayon = predict_fire_status(1,3900, np.array(pixel_values))
            print(Relayon)
            if Relayon == "FIRE":
                set_relay_pin(5,1)

                time.sleep(5)
                
                set_relay_pin(5,0)
        else:
            set_relay_pin(5,1)

            time.sleep(5)
            
            set_relay_pin(5,0)
    return previous_x_servo_angle


def set_relay_pin(pin, state):
    command = f"D:{state}\n"
    ser.write(command.encode())

def move_servo(servo,angle):
    command=f"{servo}:{angle}\n"
    ser.write(command.encode())

def OneToTwoD(array):
    if array is None:
        print("Input array cannot be None")
        return None
    else:
        a = []
        line = []
        i = 0
        for ele in array:
            line.append(ele)
            i += 1
            if i == 8:
                a.append(line)
                line = []
                i = 0
        return a
    
 
def sweep(previous_angle):
    print("here")
    global right
    if previous_angle<=20:
        right=1
    elif previous_angle>=140:
        right=0
    if right is None:
        right=1
        
    if right==0:
        move_servo('S1',previous_angle-5)
        angle=previous_angle-5
    else:
        move_servo('S1',previous_angle+5)
        angle=previous_angle+5
    return angle
         
         
if __name__ == '__main__':
   xyToAngles([50,50,50,50],100)
