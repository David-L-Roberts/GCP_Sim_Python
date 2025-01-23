from Settings import *

import os
import tkinter as tk
import Logging as Log
import serial

from TitleBar import TitleBar
from MenuBar import MenuBar
from NumPad import NumPad
from FunctionPad import FunctionPad
from UtilityPad import UtilityPad
from Button import Button
from SerialReader import SerialReader
from SerialQueue import SerialQueue


# debug flag
DEBUG = True

class MainApp:
    # ardiuno serial Comms port object
    arduino = serial.Serial()

    def __init__(self, root: tk.Tk):
        # log the start of the application
        Log.log("Application Started.")
        
        # try to connect to arduino
        try:
            MainApp.arduino = serial.Serial(
                port=SERIAL_PORT,
                baudrate=BAUD_RATE,
                timeout=0.1
            )
        except:
            Log.log(f"Failed to connnect to arduino on port {SERIAL_PORT}.", logFlag="|ERROR|")
        else:
            Log.log_file(f"Ardiuno successfully connected on port {SERIAL_PORT}.", logFlag="|Info|")
        

        # configure root window
        self.root = root
        self.configure_root()

        if DEBUG:
            # instantiate thread that reads serial
            self.thread_serialReader = SerialReader(MainApp.arduino)
        # instantiate queuing thread
        self.thread_queue = SerialQueue(
            arduino=MainApp.arduino, 
            maxsize=QUEUE_MAX_SIZE,
            dequeue_interval_seconds=QUEUE_DELAY
        )

        # Instantiate button lookup table for serial action codes
        Button.instantiate_serial_lookup()
        # pass the queuing thread to the button class
        Button.instantiate_queue_thread(self.thread_queue)

        # Add menu bar
        self.MenuBar = MenuBar(
            master=self.root,
            row=0,
            col=0,
        )

        # Add a Title bar to root window
        self.Titlebar = TitleBar(
            master=self.root,
            text="ICE CONTROLS",
            row=1,
            col=0,
        )

        # frame for holding the ICE buttons
        self.ice_buttons = tk.Frame(
            master=self.root,
            bg=GREY_1
        )
        self.ice_buttons.grid(
            row=2,
            column=0,
        )
        self.add_ice_buttons(self.ice_buttons)


    
    def __del__(self):
        # log the end of the application
        Log.log("Application Terminated.")

    def configure_root(self):
        self.root.title("IRAS - ICE REMOTE ACCESS SYSTEM")
        self.root.config(
            padx=40, 
            pady=15,
            bg=GREY_1,
        )
        self.root.minsize(width=560, height=694)
        self.root.resizable(width=True, height=True)

        photo = tk.PhotoImage(file = WINDOW_ICON)
        self.root.wm_iconphoto(True, photo)

    
    def add_ice_buttons(self, master: tk.Frame):
        """Create all the ICE buttons and add them to the given master widget.
        Creates the ICE: function pad; number pad; utility pad
        """
        # add Function pad buttons to root window
        self.functionPad = FunctionPad(
            master=master,
            row=1,
            col=0,
        )

        # Add a Numberpad to the root window
        self.numPad = NumPad(
            master=master,
            row=1,
            col=1,
        )

        # Add utility button pad to root window
        self.utilPad = UtilityPad(
            master=master,
            row=1,
            col=2,
        )



# ---------------------------- Open Web Cam ------------------------------- #
def open_web_cam():
    try:
        os.system('cmd /c "start microsoft.windows.camera:"')
    except:
        Log.log("Webcam App failed to open.", logFlag="|WARNING|")
    else:
        Log.log("Webcam App opened successfully.")


# ---------------------------- MAIN FUNCTION ------------------------------- #

def main():
    # open_web_cam()
    
    root = tk.Tk()
    mainApp = MainApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()