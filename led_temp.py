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
            cursor.execute("INSERT INTO stephs (time, temp) VALUES (?, ?)", (datetime.now(),temp))
            connection.commit()
            light_reset()
            if temp < 70.0:
                GPIO.output(blue_led,GPIO.HIGH)
            elif temp >= 70.0 and temp <= 75.0:
                GPIO.output(orange_led,GPIO.HIGH)
            elif temp > 75.0:
                GPIO.output(red_led,GPIO.HIGH)
            else:
                GPIO.output(blue_led,GPIO.HIGH)
                GPIO.output(orange_led,GPIO.HIGH)
                GPIO.output(red_led,GPIO.HIGH)
            time.sleep(30)
        except KeyboardInterrupt:
            connection.close()
            GPIO.cleanup()

if __name__ == "__main__":main()
