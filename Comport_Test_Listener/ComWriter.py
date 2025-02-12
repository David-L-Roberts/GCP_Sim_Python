from ComPort import ComPort
from datetime import datetime


class ComWriter():
    """Class for writing data to serial port.
    Allows for construction and transmission of a Genisys message.
    """
    def __init__(self, comPort: ComPort) -> None:
        self._comPort = comPort

    def writeSerial(self):
        """Prompt user to specify message for transmission.
        Transmit message to serial
        """
        # generate new message
        dataBytes = b''
        dataStr = ""
        txData: str = input()
        try:
            dataBytes = bytes.fromhex(txData)
            dataStr = dataBytes.hex(' ').upper()
        except:
            print("Invalid input data.")
        else:
            # write message to serial
            self._comPort.write(dataBytes)
            print(f"Tx Data -> {dataStr} ({self._comPort.getMessageType(dataStr)})")