from w1thermsensor import W1ThermSensor
import RPi.GPIO as GPIO
from datetime import datetime
import time
import sqlite3

GPIO.setmode(GPIO.BCM)
blue_led = 16
orange_led = 20
red_led = 21
GPIO.setup(blue_led,GPIO.OUT)
GPIO.setup(orange_led,GPIO.OUT)
GPIO.setup(red_led,GPIO.OUT)

def light_reset():
    GPIO.output(blue_led,GPIO.LOW)
    GPIO.output(orange_led,GPIO.LOW)
    GPIO.output(red_led,GPIO.LOW)
    
def blink_light(chosen_light):
    GPIO.output(chosen_light,GPIO.HIGH)
    time.sleep(0.25)
    GPIO.output(chosen_light,GPIO.LOW)
    time.sleep(0.25)
    GPIO.output(chosen_light,GPIO.HIGH)
    time.sleep(0.25)
    GPIO.output(chosen_light,GPIO.LOW)
    time.sleep(0.25)
    GPIO.output(chosen_light,GPIO.HIGH)
    time.sleep(0.25)
    GPIO.output(chosen_light,GPIO.LOW)
    time.sleep(0.25)
    GPIO.output(chosen_light,GPIO.HIGH)
    time.sleep(0.25)
    GPIO.output(chosen_light,GPIO.LOW)
    time.sleep(0.25)
    GPIO.output(chosen_light,GPIO.HIGH)
    time.sleep(0.25)
    GPIO.output(chosen_light,GPIO.LOW)
    time.sleep(0.25)
    GPIO.output(chosen_light,GPIO.HIGH)
    time.sleep(0.25)
    GPIO.output(chosen_light,GPIO.LOW)
    time.sleep(0.25)
    GPIO.output(chosen_light,GPIO.HIGH)
    time.sleep(0.25)
    GPIO.output(chosen_light,GPIO.LOW)
    time.sleep(0.25)
    GPIO.output(chosen_light,GPIO.HIGH)
    
def main():
    db_filename = 'temp.db'
    connection = sqlite3.connect(db_filename)
    cursor = connection.cursor()
    cursor.execute('''CREATE TABLE if not exists stephs (
                        time date primary key,
                        temp float)''')
                        
    sensor = W1ThermSensor()
 
    while True:
        try:
            temp = sensor.get_temperature(W1ThermSensor.DEGREES_F)
            print("writing  " + str(temp))
            if temp < 70.0:
                chosen_light = blue_led
            elif temp >= 70.0 and temp <= 75.0:
                chosen_light = orange_led
            elif temp > 75.0:
                chosen_light = red_led
            else:
                light_reset()
                GPIO.output(blue_led,GPIO.HIGH)
                GPIO.output(orange_led,GPIO.HIGH)
                GPIO.output(red_led,GPIO.HIGH)
                
            light_reset()
            GPIO.output(chosen_light,GPIO.HIGH)
            cursor.execute("INSERT INTO stephs (time, temp) VALUES (?, ?)", (datetime.now(),temp))
            connection.commit()

            time.sleep(2)
            blink_light(chosen_light)
        except KeyboardInterrupt:
            connection.close()
            GPIO.cleanup()

if __name__ == "__main__":main()
