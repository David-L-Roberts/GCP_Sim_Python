import tkinter as tk
import csv
from Button import Button
from Settings import *

class NumPad:

    def __init__(self, master, row, col) -> None:
        self.master = master

        # Top Level Frame for NumPad
        self.frame = tk.Frame(
            master=self.master,
            bg=GREY_1
        )
        self.frame.grid(
            row=row,
            column=col,
            padx=20
        )
        
        # Create NumPad buttons from csv data
        self.buttons = {}
        self.instantiate_all_buttons()
        

    def instantiate_all_buttons(self):
        with open("Resources\\NumPad_BtnData.csv", "r") as file:
            reader = csv.DictReader(file)
            table = list(reader)

        for entry in table:
            self.buttons[entry["name"]] = Button(
                name=entry["name"],
                master=self.frame,
                row=entry["row"],
                col=entry["col"],
                img_src=entry["img_src"],
            )
        
        self.buttons["TICK"].button.config(bg=GREEN)
        self.buttons["X"].button.config(bg=RED)

    
