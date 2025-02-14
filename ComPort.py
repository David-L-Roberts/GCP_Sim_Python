import serial.tools.list_ports as port_list
import serial
from Logging import Log
from MessageLib import msgTypeLookup


class ComPort(serial.Serial):
    def __init__(self, portNum, baudrate=9600, timeout=0.1) -> None:
        super().__init__(baudrate=baudrate, timeout=timeout)
        self._open_com_port(portNum)
        self.reset_input_buffer()
        self.reset_output_buffer()
    
    def _open_com_port(self, portNum):
        """Open the Serial Com port"""
        try:
            self.port = portNum
            self.open()
        except:
            raise Exception(f"Comm port ({self.portstr}) failed to open!")
        else:
            print(f"Comm port ({self.portstr}) opened successfully.")
    
    @classmethod
    def list_ports(cls):
        """List all available Serial ports on the system."""
        ports = list(port_list.comports())
        if ports:
            print("Com ports available:")
            for i, p in enumerate(ports):
                print(f"\t{i}. {p}")
        else:
            raise Exception("No Com ports Available!")

    def writeSerial(self, messageBytes: bytes):
        """Write given bytes to serial, enclosing within `<` and `>` delimiters."""
        messagePacket: bytes = b'<' + messageBytes + b'>'

        messageStr = messagePacket.decode()
        Log.log(f"Tx Data -> {messageStr} (Type: {self.getMessageType(messageBytes)})", Log.DEBUG)
        self.write(messagePacket)
    
    def readSerial(self):
        """Attempt to read data from comport.
        Returns empty byte string if no data was read.
        """
        inputByteArray: bytes = b''
        bytes_in_waiting = self.in_waiting
        if(bytes_in_waiting > 0):
            Log.log(f"Bytes Received: {bytes_in_waiting}", Log.DEBUG)
        else: 
            return b''    # no data available for reading
        
        while(self.in_waiting > 0):
            inputByteArray += self.read()

        return inputByteArray    # data succesfully read

    def bytesToString(self, byteData: bytes):
        return byteData.hex(" ").upper()

    def getMessageType(self, controlCode: bytes):
        """Return the message type of the last read message."""
        try:
            messageType = msgTypeLookup[controlCode]
        except:
            messageType = controlCode
            Log.log(f"Received invalid Control Code ({controlCode}).", Log.ERROR)

        return messageType

