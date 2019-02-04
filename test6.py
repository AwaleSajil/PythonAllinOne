from flaskServerV1 import *
import time

#accesses the read data and display it 
def displayreadData(getData):
    while True:
        time.sleep(1)
        print("T: ", getData[0])
        print("H: ", getData[1])
        print("L: ", getData[2])
        print("A: ", getData[3])
