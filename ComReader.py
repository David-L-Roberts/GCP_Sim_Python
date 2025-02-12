from threading import Thread, Event
from ComPort import ComPort
import time
from Logging import Log


class ComReader():
    """   
    Starts a thread that will read data from serial.
    Will read for `maxWaitsec` time, then sleep. Will wake when `readSerial` method is called.

    Provides methods to read data from the serial.
    """
    def __init__(self, comPort: ComPort) -> None:
        self._comPort = comPort
        self._rxDataBytes: bytes = b''
        self._rxDataQueue: list[str] = []

        self._event = Event()
        self._readThread = Thread(target=self.__threadLoop, daemon=True)
        self._readThread.start()
    
    def __threadLoop(self):
        while True:
            self.__readSerial()
            time.sleep(0.1)

    def __readSerial(self):
        """Try reading data from serial."""
        self._rxDataBytes = self._comPort.readSerial()
        if self._rxDataBytes == b'':
            return
        self.__processDataBytes()
        
    def __processDataBytes(self):
        rxDataStr = self._comPort.bytesToString(self._rxDataBytes) # convert data bytes to string format
        Log.log(f"Rx Data <- {rxDataStr}", Log.DEBUG)      # log received bytes

        # process individual bytes:
        splitData: list = rxDataStr.split(' ')
        messageTypes = []
        joinFlag = False
        for byteCode in splitData:
            if joinFlag:
                # group distance sensor code with distance sensor data value into a tuple, before adding to queue
                byteCode = (self._rxDataQueue.pop(), byteCode)
                self._rxDataQueue.append(byteCode)
                joinFlag = False
                continue
            elif byteCode == "FD":  # flag special processing for distance sensor code
                joinFlag = True
            # add received bytes to data queue
            self._rxDataQueue.append(byteCode)
            # determine type of code received
            messageTypes.append(self._comPort.getMessageType(byteCode))

        Log.log(f"Rx Message Type: {messageTypes}", Log.DEBUG)

    def popNextMessage(self):
        """returns the oldest unread character code received from serial.
        Removes character code from queue after returning.
        If queue is empty, returns `None`"""
        if self._rxDataQueue == []:
            return None
        else:
            return self._rxDataQueue.pop(0)