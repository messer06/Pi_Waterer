# External module imp
import RPi.GPIO as GPIO
import datetime
import time
import boto3
import pandas as pd

session = boto3.Session()
credentials = pd.read_csv('/home/pi/Documents/accessKeys.csv')
client = session.client('sns',
                        region_name="us-east-1",
                        aws_access_key_id=credentials.loc[0,'Access key ID'],
                        aws_secret_access_key=credentials.loc[0,'Secret access key'])
f = open("/home/pi/Documents/PhoneNumber.txt")
TextNumber = f.read()
f.close()

init = False

GPIO.setmode(GPIO.BOARD) # Broadcom pin-numbering scheme


def get_last_watered():
    try:
        f = open("/home/pi/Documents/Water/last_watered.txt", "r")
        return f.readline()
    except:
        return "NEVER!"
      
def get_status(pin = 8):
    GPIO.setup(pin, GPIO.IN,pull_up_down=GPIO.PUD_DOWN) 
    GPIO.setup(10,GPIO.OUT)
    GPIO.output(10,GPIO.HIGH)
    time.sleep(3)
    status = 0
    for i in range(0,9):
        status = status + GPIO.input(pin)
        time.sleep(.05)
    status = status /10 > .5    
    GPIO.setup(10,GPIO.OUT)
    GPIO.output(10,GPIO.LOW)
    return status

def init_output(pin):
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)
    GPIO.output(pin, GPIO.HIGH)
    
def auto_water(delay = 5*60, pump_pin = 7, water_sensor_pin = 8):
    consecutive_water_count = 0
    init_output(pump_pin)
    print("Here we go! Press CTRL+C to exit")
    try:
        while 1 and consecutive_water_count < 5:
            wet = get_status(pin = water_sensor_pin)
            if not wet:
                if consecutive_water_count < 4:
                    pump_on(pump_pin, 1*60)
                consecutive_water_count += 1
            else:
                consecutive_water_count = 0
            time.sleep(delay)
        client.publish(PhoneNumber=TextNumber,Message = "Check Your Plants!")
        GPIO.cleanup()
    except KeyboardInterrupt: # If CTRL+C is pressed, exit cleanly:
        GPIO.cleanup() # cleanup all GPI

def pump_on(pump_pin = 7, delay = 1):
    try:
       delay = int(delay)
    except: 
       delay = 1
    init_output(pump_pin)

    #read watering history from file
    #with open("/home/pi/Documents/Water/last_watered.txt", "r") as last_watered:
    #	content = [next(last_watered) for x in range(98)]
    try: water_history = pd.read_csv("/home/pi/Documents/Water/last_watered.txt", nrows=100)
    except: water_history =pd.dataframe()
    #write new line on top of top 100 last waters
    with open("/home/pi/Documents/Water/last_watered.txt", "w") as last_watered:
        last_watered.write("Last watered {}".format(datetime.datetime.now()) + ' for ' + str(delay) + ' seconds' + '\n')
        water_history.to_csv(last_watered, index = False)
    GPIO.output(pump_pin, GPIO.LOW)
    time.sleep(delay)
    GPIO.output(pump_pin, GPIO.HIGH)
    
