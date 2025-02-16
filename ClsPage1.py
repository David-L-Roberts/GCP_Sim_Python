from nicegui import ui
from ComPort import ComPort
from MessageLib import ActionCodes, txMessageCodes
from StyleSettings import *

SWITCH_T_MULT = 4

class Page1MainBody:
    def __init__(self, comPort: ComPort):
        self.__comPort: ComPort = comPort

        with ui.column().classes(f'{C_MAIN_BODY_2} px-20 py-8 mx-5 my-2 space-y-4'):
            self.__add_controls_decreaseEZ()
            self.__add_controls_increaseEZ()
            self.__add_controls_resetEZ()
            self.__add_controls_manual()
            self.__add_controls_speedConfig()

    # ========================================================================================
    #   ADD UI ELEMENTS    
    # ========================================================================================
    def __add_controls_decreaseEZ(self):
        with ui.row().classes("items-center"):
            ui.label("Decrease EZ:") \
                .classes("text-bold text-lg")
            ui.button("Start Approach", on_click=self.__buttonFunc_startApproach) \
                .props('icon=switch_right color=green-6')
            ui.button("Pause Approach", on_click=self.__buttonFunc_pauseApproach) \
                .props('icon=pause color=green-6')
    
    def __add_controls_increaseEZ(self):
        with ui.row().classes("items-center"):
            ui.label("Increase EZ:") \
                .classes("text-bold text-lg")
            ui.button("Start Departure", on_click=self.__buttonFunc_startDeparture) \
                .props('icon=switch_left color=cyan-6')
            ui.button("Pause Depature", on_click=self.__buttonFunc_pauseDeparture) \
                .props('icon=pause color=cyan-6')
    
    def __add_controls_resetEZ(self):
        with ui.row().classes("items-center"):
            ui.label("Reset EZ:") \
                .classes("text-bold text-lg")
            ui.button("Reset EZ High (100)", on_click=self.__buttonFunc_resetEZHigh) \
                .props('icon=arrow_upward color=purple-6')
            ui.button("Reset EZ Low (0)", on_click=self.__buttonFunc_resetEZLow) \
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
            ui.label("Update Switching Speed (in ms).") \
                .classes("text-lg text-[#ffecb3]")
            ui.label("This is the amount of time before changing to next state (next EZ value).") \
                .classes("text-italic text-stone-200")
            
        with ui.row().classes("items-center"):
            self.sliderSwitchTime = ui.slider(min=200, max=(250*SWITCH_T_MULT), step=10, value=500) \
                .classes("w-96").props('color=amber-8')
            ui.label().bind_text_from(self.sliderSwitchTime, 'value')
            ui.label("ms")

            ui.button("Update Speed", on_click=self.__buttonFunc_speedUpdate) \
                .props('icon=send color=amber-8')

    
    # ========================================================================================
    #   BUTTON FUNCTIONS    
    # ========================================================================================
    
    # decreaseEZ
    def __buttonFunc_startApproach(self):
        self.__comPort.writeSerial(txMessageCodes[ActionCodes.DECREASE_EZ])
        ui.notify('Train Approaching')
    
    def __buttonFunc_pauseApproach(self):
        self.__comPort.writeSerial(txMessageCodes[ActionCodes.IDLE])
        ui.notify('Approach Paused')

    # increaseEZ
    def __buttonFunc_startDeparture(self):
        self.__comPort.writeSerial(txMessageCodes[ActionCodes.INCREASE_EZ])
        ui.notify('Train Departing')
    
    def __buttonFunc_pauseDeparture(self):
        self.__comPort.writeSerial(txMessageCodes[ActionCodes.IDLE])
        ui.notify('Depature Paused')

    # resetEZ
    def __buttonFunc_resetEZHigh(self):
        self.__comPort.writeSerial(txMessageCodes[ActionCodes.RESET_HIGH_EZ])
        ui.notify('Set EZ=100')
    
    def __buttonFunc_resetEZLow(self):
        self.__comPort.writeSerial(txMessageCodes[ActionCodes.RESET_LOW_EZ])
        ui.notify('Set EZ=0')

    # manual
    def __buttonFunc_manual(self):
        pass

    # speedConfig
    def __buttonFunc_speedUpdate(self):
        ui.notify(f"Switching speed updated to: {self.sliderSwitchTime.value} ms")
        self.__comPort.writeSerial(txMessageCodes[ActionCodes.CHANGE_SWITCH_T])
        self.__comPort.newSwitchTime = True
        switchTActionCode: bytes = str(int(self.sliderSwitchTime.value / SWITCH_T_MULT)).encode()
        self.__comPort.writeSerial(switchTActionCode)
