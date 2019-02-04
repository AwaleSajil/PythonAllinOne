import time
import multiprocessing
from peakCounterV1 import *
from comV1 import *
from flaskServerV1 import *

from test7 import *


if __name__ == "__main__":

	##shared memory variable declarations

	#create a int array of size 2 
    #for peakcount and weight of feed taken in
    soundAnalysis = multiprocessing.Array('d', 2)

    #create an int array of size 4 
    #for sending data to arduino
    sendData = multiprocessing.Array('i', 4)

    #create an int array of size 4
    #for receving data from arduino
    readData = multiprocessing.Array('i', 4)


    # p1 = multiprocessing.Process(target=peakCounter, args=(soundAnalysis,))
    # p2 = multiprocessing.Process(target=com, args=(sendData,readData,))

    p3 = multiprocessing.Process(target=flaskServer, args=(soundAnalysis, sendData, readData, ))

    p4 = multiprocessing.Process(target=changeReadData, args=(readData, ))



    # p1.start()
    # p2.start()
    p3.start()
    p4.start()

    # p1.join()
    # p2.join()
    p3.join()
    p4.join()
