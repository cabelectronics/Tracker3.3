#Python3.9

import serial
from flask import Flask
from flask_cors import CORS
from decimal import Decimal
import json

#START Flask
app = Flask(__name__)
CORS(app)

#########################################################READ THE CONFIGURATION################################################################################

#READ ave_lat
ave_lat_file = open('configuration/ave_lat.txt')
for line in ave_lat_file:
  ave_lat = int(line)
ave_lat_file.close()

#READ ave_lon
ave_lon_file = open('configuration/ave_lon.txt')
for line in ave_lon_file:
  ave_lon = line
ave_lon_file.close()

#READ port

#READ baudrate

@app.route("/helicopter_1.json")
def hello():
      
  ser = serial.Serial()
  ser.port = 'COM2'
  ser.baudrate = 9600
  ser.open()
  search = ser.readline()
  line = str(search)
  if 'GPRMC' in line:
    line = line.split(',')
    aH1 = Decimal(line[3])
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

    
    aW1 = Decimal(line[3])
    aW2 = aW1 / 100
    aW3 = int(aW2)
    aW4 = aW3 * 100
    aW5 = aW1 - aW4
    aW6 = aW5 / 60
    aW7 = aW3 + aW6

    LONGITUDE_result = aW7

    if ave_lon < 0:
      LONGITUDE_result = aW7 * -1
    else:
      pass
   

    msg = '{"helicopter1_position": {"latitude": '+ str(LATITUDE_result) + ', "longitude": ' + str(LONGITUDE_result) +'}, "message": "success", "timestamp": 1604506611}'
    msg_json = json.loads(str(msg)) 
    
    return msg_json
    
  else:
    pass
  
  
app.run(host='127.0.0.1', port= 5000)


#'{helicopter1_position": {"latitude": '+ str(LATITUDE_result) + ', "longitude": -2.63266}, "message": "success", "timestamp": 1604506611}'