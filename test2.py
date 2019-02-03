import time


def printPeak(pc):
    for i in range(10000):
        print(i , ": Peack count", pc.value)
        time.sleep(0.01)
