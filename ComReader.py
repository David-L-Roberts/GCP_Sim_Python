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
        self._rxDataQueue: list[bytes] = []

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
        msg_str = self._rxDataBytes.decode()
        # Log.log(f"Processing raw input <- {msg_str}", Log.DEBUG)

        msg_list: list[bytes] = []
        i = 0
        j = 0   # prevent infinite loops
        while True:
            j += 1
            if (i >= len(msg_str)) or (j > 250):
                break
                
            char = msg_str[i]
            if char == "<":
                msg_part1 = msg_str[:i]
                msg_part2 = msg_str[i:]

                msg_list.append(msg_part1.encode())
                msg_str = msg_part2
                i = 1
                continue
            elif char == ">":
                i += 1
                msg_part1 = msg_str[:i]
                msg_part2 = msg_str[i:]

                msg_list.append(msg_part1.encode())
                msg_str = msg_part2
                i=0
                continue

            i += 1

        if msg_str != '':
            msg_list.append(msg_str.encode())

        for msg in msg_list:
            self._rxDataQueue.append(msg)


    def popNextMessage(self):
        """returns the oldest unread character code received from serial.
        Removes character code from queue after returning.
        If queue is empty, returns `None`"""
        if self._rxDataQueue == []:
            return None
        else:
            return self._rxDataQueue.pop(0)