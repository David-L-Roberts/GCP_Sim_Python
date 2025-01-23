import tkinter as tk
from Settings import *

class TitleBar:

    def __init__(self, master, text: str, row=0, col=0, columnspan=1) -> None:
        # Title Lable
        self.lbl_title = tk.Label(
            master=master,
            text=text,
            bg=GREY_1,
            fg=BLUE_D,
            font=(FONT_NAME, 30, "bold"),
            # height=2,
        )
        self.lbl_title.grid(
            row=row,
            column=col,
            columnspan=columnspan,
            pady=20,
        )
