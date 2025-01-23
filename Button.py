from Settings import *

import tkinter as tk
from tkinter import messagebox
import csv

import Logging as Log
from SerialQueue import SerialQueue

class Button:
    """Places a button in a Frame, with a Canvas widget.
    Canvas widget sits behind the button, and controls the size of the button.
    """
    # lookup dictionary for converting button names to action codes for sending to serial comms.
    serial_lookup = {}

    # queue thread object for enqueuing action codes
    thread_queue = None

    def __init__(self, name: str, master: tk.Frame, row: int, col: int, img_src: str, active_bg=PURPLE):
        # name of button
        self.name = name

        # create a frame to hold the button
        self.frame = tk.Frame(
            master=master,
            bg=GREY_2,
        )
        self.frame.grid(
            row=row,
            column=col,
            padx=5,
            pady=5,
        )

        # create a canvas to set the size fo the button
        self.canvas = tk.Canvas(
            master=self.frame,
            width=78,
            height=82,
            bg=PURPLE,
            highlightthickness=0,
        )
        self.canvas.create_text(0, 0, text="")
        self.canvas.grid(row=0, column=0)

        # create photoimage object for button
        self.btn_image = tk.PhotoImage(file=img_src)

        # create button widget
        self.button = tk.Button(
            master=self.frame,
            image=self.btn_image,
            bg=GREY_2,
            activebackground=active_bg,
        )
        self.button.grid(
            row=0,
            column=0,
            sticky="nesw",
        )
        
        # bind a command to the button
        self.bind(self.command)
    

    @classmethod
    def instantiate_serial_lookup(cls):
        with open("Resources\\Serial_Lookup.csv", "r") as file:
            reader = csv.reader(file)
            table = list(reader)
        
        cls.serial_lookup = dict(table)

    @classmethod
    def instantiate_queue_thread(cls, thread_queue: SerialQueue):
        """Pass a queuing thread to the button class."""
        cls.thread_queue = thread_queue
    
    def bind(self, command):
        """Bind the given command to the button.
        Adds the functionality in addition to existing commands bound to the button.

        Args:
            command (Callable): Function to be called on button click
        """
        self.button.bind(
            sequence="<Button-1>",
            func=command,
            add=True
        )
    
    def rebind(self, command):
        """Bind the given command to the button.
        Replaces the existing functionality of the button.

        Args:
            command (Callable): Function to be called on button click
        """
        self.button.bind(
            sequence="<Button-1>",
            func=command,
            add=False
        )

    def command(self, event):
        # log the event of the button being pressed
        Log.log_btnPress(self.name)

        # send action code for button press to serial port
        self._enqueue_action_code()

    
    def _enqueue_action_code(self):
        """enqueues the action code for the button press"""
        # turn button name into an action code
        action_code = "<" + self.serial_lookup[self.name] + ">"
        # enqueue the action code
        Button.thread_queue.enqueue(action_code)

       

class PowerButton(Button):
    def __init__(self, name: str, master: tk.Frame, row: int, col: int, img_src: str, active_bg=PURPLE):
        super().__init__(name, master, row, col, img_src, active_bg)
        
        self.message_result = None  # result of warning message

        if self.name == "POWER ON":
            self.button.configure(command=self.power_on_action)
        elif self.name == "POWER OFF":
            self.button.configure(command=self.power_off_action)
    

    def command(self, event):
        # log the event of the button being pressed
        Log.log_btnPress(self.name)

    # Override default warning window
    def _showwarning(self, title=None, message=None, **options):
        "Show a warning message"
        return messagebox._show(title, message, messagebox.WARNING, messagebox.YESNO, **options)

    def _open_warning_Message(self, title: str, message: str):
        Log.log(message, timeStamp=False, logFlag="")
        self.message_result = self._showwarning(
            title=title,
            message=message
        )
        Log.log(self.message_result, timeStamp=False, logFlag="")

    def power_off_action(self):
        """open a warning message window for power off"""
        message = "Are you sure you wish to turn OFF the ICE Unit?"
        title = "Warning - ICE Power OFF"
        self._open_warning_Message(title, message)
        
        if self.message_result == "yes":
            # send action code for button press to serial port
            self._enqueue_action_code()

    def power_on_action(self):
        """open a warning message window for power on"""
        message = "Are you sure you wish to turn ON the ICE Unit?"
        title = "Warning - ICE Power On"
        self._open_warning_Message(title, message)
        
        if self.message_result == "yes":
            # send action code for button press to serial port
            self._enqueue_action_code()
