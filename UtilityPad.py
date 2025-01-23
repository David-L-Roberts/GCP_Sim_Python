import tkinter as tk
import csv
from Button import Button, PowerButton
from BlankButton import Blank
from Settings import *


class UtilityPad:

    def __init__(self, master, row, col) -> None:
        self.master = master

        # Top Level Frame for Utility pad
        self.frame = tk.Frame(
            master=self.master,
            bg=GREY_1
        )
        self.frame.grid(
            row=row,
            column=col,
            padx=5
        )
        
        # Create Utility Pad buttons from csv data
        self.buttons = {}
        self.instantiate_all_buttons()
        

    def instantiate_all_buttons(self):
        with open("Resources\\UtilityPad_BtnData.csv", "r") as file:
            reader = csv.DictReader(file)
            table = list(reader)

        for entry in table[:2]:
            self.buttons[entry["name"]] = Button(
                name=entry["name"],
                master=self.frame,
                row=entry["row"],
                col=entry["col"],
                img_src=entry["img_src"],
                active_bg=ORANGE,
            )
        
        for entry in table[2:]:
            self.buttons[entry["name"]] = PowerButton(
                name=entry["name"],
                master=self.frame,
                row=entry["row"],
                col=entry["col"],
                img_src=entry["img_src"],
                active_bg=ORANGE,
            )
        
        for i in [2, 3]:
            self.buttons[f"blank_{i}"] = Blank(
                master=self.frame,
                row=i,
                col=0,
            )
