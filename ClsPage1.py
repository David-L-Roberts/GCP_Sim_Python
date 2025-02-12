from nicegui import ui
from StyleSettings import *

class Page1MainBody:
    def __init__(self):
        with ui.column().classes(f'{C_MAIN_BODY_2} px-20 py-8 mx-5 my-2 space-y-4'):
            self.__add_controls_decreaseEZ()
            self.__add_controls_increaseEZ()
            self.__add_controls_resetEZ()
            self.__add_controls_manual()
            self.__add_controls_speedConfig()

    
    def __add_controls_decreaseEZ(self):
        with ui.row().classes("items-center"):
            ui.label("Decrease EZ:") \
                .classes("text-bold text-lg")
            ui.button("Start Approach", on_click=lambda: ui.notify('Train Approaching')) \
                .props('icon=switch_right color=green-6')
            ui.button("Pause Approach", on_click=lambda: ui.notify('Approach Paused')) \
                .props('icon=pause color=green-6')
    
    def __add_controls_increaseEZ(self):
        with ui.row().classes("items-center"):
            ui.label("Increase EZ:") \
                .classes("text-bold text-lg")
            ui.button("Start Departure", on_click=lambda: ui.notify('Train Departing')) \
                .props('icon=switch_left color=cyan-6')
            ui.button("Pause Depature", on_click=lambda: ui.notify('Depature Paused')) \
                .props('icon=pause color=cyan-6')
    
    def __add_controls_resetEZ(self):
        with ui.row().classes("items-center"):
            ui.label("Reset EZ:") \
                .classes("text-bold text-lg")
            ui.button("Reset EZ High (100)", on_click=lambda: ui.notify('Set EZ=100')) \
                .props('icon=arrow_upward color=purple-6')
            ui.button("Reset EZ Low (0)", on_click=lambda: ui.notify('Set EZ=0')) \
                .props('icon=arrow_downward color=deep-purple-6')
    
    def __add_controls_manual(self):
        with ui.row().classes("items-center"):
            ui.label("Manual Controls:") \
                .classes("text-bold text-lg")
            ui.label("TBD (Coming Soon)")
    
    def __add_controls_speedConfig(self):
        with ui.row().classes("items-center"):
            ui.label("Switching Speed:") \
                .classes("text-bold text-lg")
            ui.label("TBD (Coming Soon)")
    
