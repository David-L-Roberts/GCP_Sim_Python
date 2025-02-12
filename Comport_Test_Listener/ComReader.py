from threading import Thread, Event
import time
from ComPort import ComPort
import Logging as Log 


class ComReader():
    """   
    Starts a thread that will read data from serial.
    Will read for `maxWaitsec` time, then sleep. Will wake when `readSerial` method is called.

    Provides methods to read data from the serial.
    """
    def __init__(self, comPort: ComPort, filter: bool=True, maxWaitSec: float=3) -> None:
        self._comPort = comPort
        self._filter = filter
        self._currentMessage = ""
        self.maxWaitSec = maxWaitSec

        self._event = Event()
        self._readThread = Thread(target=self.__threadLoop, daemon=True)
        self._readThread.start()

    def readSerial(self):
        """Start thread to read data from serial."""
        self._event.set()
    
    def __threadLoop(self):
        while True:
            self.__readSerial()
            time.sleep(0.3)

    def __readSerial(self):
        """Try reading data from serial."""
        inputBytes = self.__readRaw() 
        if inputBytes == b'':
            return
        inputStr = inputBytes.hex(' ').upper()
        # print(inputStr, f"({self._comPort.getMessageType(inputStr)})")
        print(f"Rx data <- {inputBytes.decode()}")


    def __readRaw(self):
        """Read raw serial data. For debugging purposes."""
        inputBytes = b''
        while(self._comPort.in_waiting > 0):
            inputBytes += self._comPort.read(10)
        return inputBytes

