import tkinter as tk
import csv
from Button import Button
from BlankButton import Blank
from Settings import *

class FunctionPad:

    def __init__(self, master, row, col) -> None:
        self.master = master

        # Top Level Frame for Function pad
        self.frame = tk.Frame(
            master=self.master,
            bg=GREY_1
        )
        self.frame.grid(
            row=row,
            column=col,
            padx=5
        )
        
        # Create Function Pad buttons from csv data
        self.buttons = {}
        self.instantiate_all_buttons()
        

    def instantiate_all_buttons(self):
        with open("Resources\\FuncBtns_BtnData.csv", "r") as file:
            reader = csv.DictReader(file)
            table = list(reader)

        for entry in table:
            self.buttons[entry["name"]] = Button(
                name=entry["name"],
                master=self.frame,
                row=entry["row"],
                col=entry["col"],
                img_src=entry["img_src"],
                active_bg=BLUE_D,
            )
        
        self.buttons["blank"] = Blank(
            master=self.frame,
            row=len(table),
            col=0,
        )
