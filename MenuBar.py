import tkinter as tk
from Settings import *
from datetime import datetime

class MenuBar:

    def __init__(self, master, row=0, col=0, columnspan=1) -> None:
        # frame for spacing
        self.frm_spacing = tk.Frame(
            master=master,
            bg=GREY_1,
            height=10
        )
        self.frm_spacing.grid(
            row=row,
            column=col,
            columnspan=columnspan,
            sticky="we"
        )

        # frame to hold the menu bar widgets
        self.frame = tk.Frame(
            master=master,
            bg=GREY_0,
        )
        self.frame.place(
            bordermode=tk.OUTSIDE,
            relwidth=1,
            anchor="nw",
            height=25
        )

        # clock widget
        self.label_clock = tk.Label(
            master=self.frame,
            text="HH:MM:SS",
            bg=GREY_0,
            fg=BLUE_L,
            font=(FONT_NAME, 12),
        )
        self.label_clock.place(
            bordermode=tk.INSIDE,
            anchor="nw",
            relx=0.02,
        )
        self.label_clock.after(ms=1000, func=self.update_time)

        # Serial Com port
        self.label_port = tk.Label(
            master=self.frame,
            text=f"Serial Port: {SERIAL_PORT}",
            bg=GREY_0,
            fg=BLUE_L,
            font=(FONT_NAME, 12),
        )
        self.label_port.place(
            bordermode=tk.INSIDE,
            anchor="n",
            rely=0,
            relx=0.5,
        )

        # Arduino connection status
        self.label_status = tk.Label(
            master=self.frame,
            text="Status: Disconnected".ljust(20),
            bg=GREY_0,
            fg=RED,
            font=(FONT_NAME, 12),
        )
        self.label_status.place(
            bordermode=tk.INSIDE,
            anchor="ne",
            rely=0,
            relx=0.98,
        )

    def update_time(self):
        self.label_clock.config(text=f"{datetime.now().strftime('%I:%M:%S')}")
        self.label_clock.after(ms=1000, func=self.update_time)


