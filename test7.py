import time 

#this test changes the temp, humidity, ldr and ammnia data in run time

def changeReadData(readData):
    while True:
        time.sleep(1)
        readData[0] += 1
        readData[1] += 1
        readData[2] += 1
        readData[3] += 1

