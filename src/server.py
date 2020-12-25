from flask import Flask
from flask_cors import CORS
import json
import serial
import subprocess
from decimal import Decimal
from threading import Thread

#Read ave_lat
file_ave_lat = open('configuration/ave_lat.txt')
for line in file_ave_lat:
    ave_lat = line
file_ave_lat.close()

#Read ave_lon
file_ave_lon = open('configuration/ave_lon.txt')
for line in file_ave_lon:
    ave_lon = line
file_ave_lon.close()

#Read baudrate
file_baudrate = open('configuration/baudrate.txt')
for line in file_baudrate:
    BAUDRATE = line
file_baudrate.close()

#Read PORT 
file_port = open('configuration/port.txt')
for line in file_port:
    PORT = line
file_port.close()

#CONFIGURE and OPEN Serial Port
ser = serial.Serial()
ser.baudrate = BAUDRATE
ser.port = PORT
try:
    ser.open()
except:
    ser.close()
    print('[SERIAL] ERROR opening serial port')

#START flask
app = Flask(__name__)
CORS(app)


#We define the caltulator of the latitude coordinates
def coordinates_operation_latitude(aH1):
    aH2 = aH1 / 100
    aH3 = int(aH2)
    aH4 = aH3 * 100
    aH5 = aH1 - aH4
    aH6 = aH5 / 60
    aH7 = aH3 + aH6
    LATITUDE_result = aH7

    if ave_lat < 0:
        LATITUDE_result = aH7 * -1
    else:
        pass

    return LATITUDE_result


#Function to get the latitude
def get_latitude():
    try:
        search = ser.readline
        my_line = str(search)

        if 'RMC' in my_line:
            line.split(',')
            aH1 = Decimal(line[3])
            helicopter_latitude = coordinates_operation_latitude(aH1)
            return helicopter_latitude
    except:
        print('[Latitude] ERROR getting the latitude')


def get_coordinates(): #func1
    while True:
        try:
            H1LA = get_latitude()
            write_array = '{helicopter1_position": {"latitude":',H1LA ,', "longitude": -2.63266}, "message": "success", "timestamp": 1604506611}'
            file_array = open('ins/array.txt', 'w')
            file_array.write(write_array)
            file_array.close()
        except:
            pass

Thread(target= get_coordinates).start

@app.route("/")
def hello():
    return "Welcome to CAB - MISSION SOFTWARE"

#Read ins/array
file_array = open('ins/array.txt')
for line in file_array:
    my_latitude = line
file_array.close()

helicopter_latitude_json = json.loads(my_latitude)

@app.route("/helicopter_1.json")
def send_data_helicopter():
    try:
        return helicopter_latitude_json
    except:
        return 'aaa'

app.run(host='127.0.0.1', port= 5000)


