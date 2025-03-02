from nicegui import ui
from ComPort import ComPort
from MessageLib import ActionCodes, txMessageCodes
from StyleSettings import *
from Utils import SETTINGS
from DynamicSwitch import DynamicSwitch


class Page1MainBody:
    def __init__(self, comPort: ComPort):
        self.__comPort: ComPort = comPort
        self.__dynamSwitch: DynamicSwitch = DynamicSwitch()

        self.switch_t_mult = SETTINGS["SWITCH_T_MULT"]
        self.max_state = SETTINGS["MAX_STATE"]
        self.approach_t_min_sec = int(SETTINGS["APPROACH_T_MIN_MS"]/1000)
        self.approach_t_max_sec = int(SETTINGS["APPROACH_T_MAX_MS"]/1000)

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
            ui.label("Set system state.") \
                .classes("text-lg text-[#f48fb1]")
            ui.label("Manualy jump system to a specific state.") \
                .classes("text-italic text-stone-200")
            
        with ui.row().classes("items-center"):
            self.sliderSystemState = ui.slider(min=0, max=self.max_state, step=1, value=0) \
                .classes("w-[34rem]").props('color=pink-8 label')
            ui.label().bind_text_from(self.sliderSystemState, 'value')
            ui.label(f"/ {self.max_state}")
            ui.button("Update State", on_click=self.__buttonFunc_setState) \
                .props('icon=send color=pink-8')
            
        with ui.row().classes("items-center"):
            ui.button("Dec", on_click=self.__buttonFunc_decreaseState) \
                .props('icon=keyboard_arrow_left color=pink-9')
            ui.button("Inc", on_click=self.__buttonFunc_increaseState) \
                .props('icon=keyboard_arrow_right color=pink-9')
            
    
    def __add_controls_speedConfig(self):
        with ui.row().classes("items-center"):
            ui.label("Switching Speed:") \
                .classes("text-bold text-lg")
            ui.label("Update the total approach / departure time (in seconds).") \
                .classes("text-lg text-[#ffecb3]")
            ui.label("This is the amount of time it takes for system to go from EZ=100 to EZ=0.") \
                .classes("text-italic text-stone-200")
            
        with ui.row().classes("items-center"):
            self.sliderSwitchTime = ui.slider(min=self.approach_t_min_sec, max=self.approach_t_max_sec, step=1, value=120) \
                .classes("w-[34rem]").props('color=amber-8 label')
            ui.label().bind_text_from(self.sliderSwitchTime, 'value')
            ui.label("sec")
            ui.button("Update Speed", on_click=self.__buttonFunc_speedUpdate) \
                .props('icon=send color=amber-8')
        
        with ui.row().classes("items-center"):
            ui.button("Dec", on_click=self.__buttonFunc_decreaseSwitchTime) \
                .props('icon=keyboard_arrow_left color=amber-9')
            ui.button("Inc", on_click=self.__buttonFunc_increaseSwitchTime) \
                .props('icon=keyboard_arrow_right color=amber-9')

    
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
    def __buttonFunc_setState(self):
        ui.notify(f"System state forced to: #{self.sliderSystemState.value}")
        self.__comPort.writeSerial(txMessageCodes[ActionCodes.SET_STATE])
        self.__comPort.newSysState = True
        setStateActionCode: bytes = str(self.sliderSystemState.value).encode()
        self.__comPort.writeSerial(setStateActionCode)
    
    def __buttonFunc_increaseState(self):
        if self.sliderSystemState.value < self.max_state:
            self.sliderSystemState.value += 1
    
    def __buttonFunc_decreaseState(self):
        if self.sliderSystemState.value > 0:
            self.sliderSystemState.value -= 1
        
    # speedConfig
    def __buttonFunc_speedUpdate(self):
        ui.notify(f"Approach time updated to: {self.sliderSwitchTime.value} sec")

        baseStepPeriodMs: int = self.__dynamSwitch.calcBaseStepTime(fullTime=self.sliderSwitchTime.value*1_000)
        print(baseStepPeriodMs)

        self.__comPort.writeSerial(txMessageCodes[ActionCodes.CHANGE_SWITCH_T])
        self.__comPort.newSwitchTime = True
        switchTActionCode: bytes = str(int(baseStepPeriodMs / self.switch_t_mult)).encode()
        self.__comPort.writeSerial(switchTActionCode)

    def __buttonFunc_increaseSwitchTime(self):
        if self.sliderSwitchTime.value < self.approach_t_max_sec:
            self.sliderSwitchTime.value += 1
    
    def __buttonFunc_decreaseSwitchTime(self):
        if self.sliderSwitchTime.value > self.approach_t_min_sec:
            self.sliderSwitchTime.value -= 1