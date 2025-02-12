""" Terminal for reading from a serial port.
"""
from ComPort import ComPort
from ComReader import ComReader
from Utils import load_settings
import time
from ComWriter import ComWriter

class MainApp:
    
    def __init__(self, portNumRx: str, baudrate: int, ReadTimeoutSec: float=3) -> None:
        # comm port setup
        self.comPortRx = ComPort(portNumRx, baudrate)
        # object for reading from comport
        self.comReader = ComReader(comPort=self.comPortRx, maxWaitSec=ReadTimeoutSec, filter=False)
        # object for writing to comport
        self.comWriter = ComWriter(comPort=self.comPortRx)

        self.comReader.readSerial()
        while True:
            self.comWriter.writeSerial()
            time.sleep(0.25)

# ==================================
def main():
    settings = load_settings()

    mainApp = MainApp(
        portNumRx=settings["ComPortRx"], 
        baudrate=settings["Baudrate"],
        ReadTimeoutSec=settings["ReadTimeoutSec"]
    )

if __name__ == "__main__":
    main()