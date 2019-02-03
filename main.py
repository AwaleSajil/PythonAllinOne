import time
import multiprocessing
from peakCounterV1 import *
from comV1 import *

from test2 import *


if __name__ == "__main__":

	#shared memory variable declarations

	#create a int variable and initilize to 0 
    #for peak counter
    pc = multiprocessing.Value('i', 0)


    p1 = multiprocessing.Process(target=peakCounter, args=(pc,))
    # p2 = multiprocessing.Process(target=com, args=())

    p3 = multiprocessing.Process(target=printPeak, args=(pc,))


    p1.start()
    # p2.start()
    p3.start()

    p1.join()
    # p2.join()
    p3.join()
