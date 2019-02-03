from flask import Flask, render_template
from flask import request
import random
from commu import *


#code to communication between the shared memory and the server

def getTemperature():








#arduino side code
ports = serial_ports()
print(ports)
Arduino = serial.Serial(ports[0], baudrate=9600, timeout=0.5)
read_from_Arduino_instance = ReadFromArduino(Arduino, verbose=6)
send_to_Arduino_instance = SendtoArduino(Arduino, verbose=6)

heater=str()
fan=str()
light=str()
servo=str()
autostate=str()


# flask code
app = Flask(__name__)

def openORclose(x):
    if x=="0":
        x="OFF"
        return x
    else:
        x="ON"
        return x


@app.route('/index', methods=['GET', 'POST'])
def index():
    # x=read_from_Arduino_instance.getTemperature()
    # y=read_from_Arduino_instance.getHumidity()
    # z=read_from_Arduino_instance.getLDR()
    x=random.randint(50,100)
    y=random.randint(20,45)
    z=random.randint(40,60)
    texts=str(x)+" "+str(y)+" "+str(z)
    return """{}""".format(texts)


@app.route('/heater', methods=['GET','POST'])
def heaters():
    global heater
    if request.method=='POST':
        heater = request.get_data(as_text=True)
        #send_to_Arduino_instance.setHeater(int(heater))
        
    return """{} %""".format(heater)
    

@app.route('/fan', methods=['GET','POST'])
def fans():
    global fan
    if request.method=='POST':
        fan = request.get_data(as_text=True)
        #send_to_Arduino_instance.setFan(int(fan))
        fan=openORclose(fan)

    return """Fan is {}""".format(fan)


@app.route('/light', methods=['GET','POST'])
def lights():
    global light
    if request.method=='POST':
        light = request.get_data(as_text=True)
        send_to_Arduino_instance.setLight(int(light))
        light=openORclose(light)

    return """Light is {}""".format(light)

@app.route('/servo', methods=['GET','POST'])
def servos():
    global servo
    if request.method=='POST':
        servo = request.get_data(as_text=True)
        send_to_Arduino_instance.setServo(int(servo))
        servo=openORclose(servo)


    return """Servo is {}""".format(servo)


@app.route('/auto', methods=['GET','POST'])
def autos():
    global autostate
    if request.method=='POST':
        autoState = request.get_data(as_text=True)

    return"""automatic mode {}""".format(autoState)


def flaskServer():
    app.run(host='192.168.1.7', port=9000)









#testing this module only
if __name__=="__main__":
    #app.run(host='0.0.0.0')
    #app.run(port=5555)
    #app.run(host='192.168.1.69', port=9000)
    app.run(host='192.168.1.7', port=9000)








