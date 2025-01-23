import tkinter as tk
from Settings import *

class Blank:
    """Creates a Blank Button, used for spacing."""
    def __init__(self, master: tk.Frame, row: int, col: int):

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
            bg=GREY_1,
            highlightthickness=0,
        )
        self.canvas.create_text(0, 0, text="")
        self.canvas.grid(row=0, column=0)

