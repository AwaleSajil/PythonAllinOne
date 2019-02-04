from flask import Flask, render_template
from flask import request
import random

from test6 import *

#global reference variables from shared memory
soundData = None 
setData = None
getData = None



#code to communication between the shared memory and the server
#interface

def getPeakCount():
    return soundData[0]

def getPeakFeed():
    return soundData[1]

def getTemperature():
    return getData[0]

def getHumidity():
    return getData[1]

def getLDR():
    return getData[2]

def getgetAmmonia():
    return getData[3]

def setHeater(hValue):
    setData[0] = hValue

def setFan(fValue):
    setData[1] = fValue

def setLight(lValue):
    setData[2] = lValue

def setServo(sValue):
    setData[3] = sValue


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
    # x = getTemperature()
    # y = getHumidity()
    # z = getLDR()
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
        #setHeater(int(heater))
        
    return """{} %""".format(heater)
    

@app.route('/fan', methods=['GET','POST'])
def fans():
    global fan
    if request.method=='POST':
        fan = request.get_data(as_text=True)
        #setFan(int(fan))
        fan=openORclose(fan)

    return """Fan is {}""".format(fan)


@app.route('/light', methods=['GET','POST'])
def lights():
    global light
    if request.method=='POST':
        light = request.get_data(as_text=True)
        setLight(int(light))
        light=openORclose(light)

    return """Light is {}""".format(light)

@app.route('/servo', methods=['GET','POST'])
def servos():
    global servo
    if request.method=='POST':
        servo = request.get_data(as_text=True)
        setServo(int(servo))
        servo=openORclose(servo)


    return """Servo is {}""".format(servo)


@app.route('/auto', methods=['GET','POST'])
def autos():
    global autostate
    if request.method=='POST':
        autoState = request.get_data(as_text=True)

    return"""automatic mode {}""".format(autoState)


def flaskServer(soundAnalysis, sendData, readData):
    global soundData, setData, getData
    soundData = soundAnalysis
    setData = sendData
    getData = readData


    displayreadData(getData)
    
    ##create a server
    #app.run(host='0.0.0.0')
    #app.run(port=5555)
    #app.run(host='192.168.1.69', port=9000)
    # app.run(host='192.168.1.7', port=9000)









#testing this module only
if __name__=="__main__":
    #app.run(host='0.0.0.0')
    #app.run(port=5555)
    #app.run(host='192.168.1.69', port=9000)
    app.run(host='192.168.1.7', port=9000)








