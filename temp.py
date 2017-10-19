import serial
from datetime import datetime
import time
import sqlite3

def serial_data():
    ser = serial.Serial(port='/dev/serialyourserial', baudrate=9600)
    
    while True:
        yield ser.readline()
    ser.close()
    
def main():
    db_filename = 'temp.db'
    connection = sqlite3.connect(db_filename)
    cursor = connection.cursor()
    cursor.execute('''CREATE TABLE if not exists office (
                        time date primary key,
                        temp float)''')
 
    while True:
        try:
            print("writing  " + next(serial_data()).decode("utf-8"))
            cursor.execute("INSERT INTO office (time, temp) VALUES (?, ?)", (datetime.now(),float(next(serial_data()).decode("utf-8"))))
            connection.commit()
            time.sleep(30)
        except KeyboardInterrupt:
            connection.close()

if __name__ == "__main__":main()
