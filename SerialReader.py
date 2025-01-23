from threading import Thread
import time
import serial
import Logging as Log


class SerialReader():
    """Starts a thread that will continually read data from
    the Serial Comm port given, and print the data to the terminal.
    
    Thread started is daemonic (will terminate when main thread terminates).
    """
    def __init__(self, arduino: serial.Serial) -> None:
        self._ardiuno = arduino
        self._thread = Thread(target=self._readSerial, daemon=True)
        self._thread.start()

    def _readSerial(self):
        # reading from serial
        while True:
            input_str = ""
            for i in range(1000):
                try:
                    new_input_bit = str(self._ardiuno.read())[2:-1]
                except:
                    Log.log(
                        text="Ardiuno not connected! Cannot read from serial. Closing 'SerialReader' thread.",
                        logFlag="|ERROR|"
                    )
                    return

                if new_input_bit == "":
                    break
                elif new_input_bit == "\\r":
                    continue
                elif new_input_bit == "\\n":
                    input_str += " "
                    continue
                else:
                    input_str += new_input_bit

            # print data read from serial if string is not empty
            if input_str:
                # print("DEBUG:")
                # print(f"\tFrom Serial: {input_str}", end="")
                message = f"From Serial: {input_str}"
                Log.log(message, logFlag="|Debug|")
            time.sleep(0.25)