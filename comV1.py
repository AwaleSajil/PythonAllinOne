from __future__ import print_function
import sys
import serial
import glob
import struct
import time
import numpy as np



def serial_ports():
    """ Lists serial port names

        :raises EnvironmentError:
            On unsupported or unknown platforms
        :returns:
            A list of the serial ports available on the system
    """
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # this excludes your current terminal "/dev/tty"
        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
    else:
        raise EnvironmentError('Unsupported platform')

    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    return result



# def get_time_millis():
#     return(int(round(time.time() * 1000)))


# def get_time_seconds():
#     return(int(round(time.time() * 1000000)))



class ReadFromArduino(object):
    """A class to read the serial messages from Arduino. The code running on Arduino
    can for example be the ArduinoSide_LSM9DS0 sketch."""

    def __init__(self, port, SIZE_STRUCT = 8, verbose=0):
        self.port = port
        # self.millis = get_time_millis()
        self.SIZE_STRUCT = SIZE_STRUCT
        self.verbose = verbose
        self.Data = -1
        # self.t_init = get_time_millis()
        self.t = 0

        self.port.flushInput()

    def read_one_value(self, readData):
        """Wait for next serial message from the Arduino, and read the whole
        message as a structure."""
        read = False

        while not read:
            myByte = self.port.read(1)
            if myByte == b'S':
                packed_data = self.port.read(self.SIZE_STRUCT)
                myByte = self.port.read(1)
                if myByte == b'E':
                    # self.t = (get_time_millis() - self.t_init) / 1000.0

                    # is  a valid message struct
                    unpacked_data = struct.unpack('<hhhh', packed_data)

                    # current_time = get_time_millis()
                    # time_elapsed = current_time - self.millis
                    # self.millis = current_time

                    read = True

                    self.Data = np.array(unpacked_data)

                    #transfer data from internal memory to shared memory
                    readData[0] = self.Data[0]
                    readData[1] = self.Data[1]
                    readData[2] = self.Data[2]
                    readData[3] = self.Data[3]

                    # if self.verbose > 1:
                        # print("Time elapsed since last (ms): " + str(time_elapsed))

                    return(True)

        return(False)

    def print_values(self):
        print("------ ONE MORE MEASUREMENT ------")
        print("Temperature: ", self.Data[0])
        print("Humidity: ", self.Data[1])
        print("LDR: ", self.Data[2])
        print("Ammonia: ", self.Data[3])


    # def getTemperature(self):
    #     self.read_one_value()
    #     return self.Data[0]

    # def getHumidity(self):
    #     self.read_one_value()
    #     return self.Data[1]

    # def getLDR(self):
    #     self.read_one_value()
    #     return self.Data[2]

    # def getAmmonia(self):
    #     self.read_one_value()
    #     return self.Data[3]



class SendtoArduino(object):
    def __init__(self, port, SIZE_STRUCT = 4, verbose=0):
        self.port = port
        self.SIZE_STRUCT = SIZE_STRUCT
        self.verbose = verbose
        self.Data = np.array([4,3,2,1])



    def sendValue(self, sendData):
        #transfer data from shared memory to internal process memory
        self.Data = sendData
        #send the data to the arduino
        self.port.write(b'S')
        packed_data = struct.pack('>BBBB',self.Data[0], self.Data[1], self.Data[2], self.Data[3])
        self.port.write(packed_data)
        self.port.write(b'E')


    # def setHeater(self, Val):
    #     self.Data[0] = Val
    #     self.sendValue()

    # def setFan(self, Val):
    #     self.Data[1] = Val
    #     self.sendValue()

    # def setLight(self, Val):
    #     self.Data[2] = Val
    #     self.sendValue()

    # def setServo(self, Val):
    #     self.Data[3] = Val
    #     self.sendValue()





def com(sendData, readData):
    print("com Started")
    ports = serial_ports()
    print("Ports available: ", ports)
    Arduino = serial.Serial(ports[0], baudrate=9600, timeout=0.5)
    read_from_Arduino_instance = ReadFromArduino(Arduino, verbose=6)
    send_to_Arduino_instance = SendtoArduino(Arduino, verbose=6)

    while True:
        time.sleep(1)
        read_from_Arduino_instance.read_one_value(readData)
        send_to_Arduino_instance.sendValue(sendData)

        #display the values
        # read_from_Arduino_instance.print_values()






if __name__ == "__main__":
    #testing this module only
    com()
