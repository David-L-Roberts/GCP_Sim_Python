from nicegui import ui
from ComPort import ComPort
from MessageLib import ActionCodes, txMessageCodes
from StyleSettings import *
from Utils import SETTINGS
from SystemState import SystemMode, SystemTimes

class Page1MainBody:
    def __init__(self, comPort: ComPort, systemTime: SystemTimes, systemMode: SystemMode):
        self.__comPort: ComPort = comPort
        self.__systemTime: SystemTimes = systemTime
        self.__systemMode: SystemMode = systemMode

        self.switch_t_mult = SETTINGS["SWITCH_T_MULT"]
        self.max_state = SETTINGS["MAX_STATE"]
        self.min_state = 0
        self.approach_t_min_sec = int(SETTINGS["APPROACH_T_MIN_MS"]/1000)
        self.approach_t_max_sec = int(SETTINGS["APPROACH_T_MAX_MS"]/1000)

        with ui.column().classes(f'{C_MAIN_BODY_2} px-8 py-6 mx-2 my-2 space-y-4'):
            self.__add_controls_decreaseEZ()
            self.__add_controls_increaseEZ()
            self.__add_controls_resetEZ()

        with ui.column().classes(f'{C_MAIN_BODY_2} px-8 py-6 mx-2 my-2 space-y-4'):
            self.__add_controls_manual()
            
        with ui.column().classes(f'{C_MAIN_BODY_2} px-8 py-6 mx-2 my-2 space-y-4'):
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
            self.sliderSystemState = ui.slider(min=self.min_state, max=self.max_state, step=1, value=0) \
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
            ui.label("Switching Speed (1):") \
                .classes("text-bold text-lg")
            ui.label("Update the total approach / departure time (in seconds).") \
                .classes("text-lg text-[#ffecb3]")
            ui.label("This is the amount of time it takes for system to go from EZ=100 to EZ=0.") \
                .classes("text-italic text-stone-200")
            
        with ui.row().classes("items-center"):
            self.sliderSwitchTime = ui.slider(
                min=self.approach_t_min_sec, 
                max=self.approach_t_max_sec, 
                step=1, 
                value=SETTINGS["DEFUALT_FULL_TIME_MS"]/1000
                ).classes("w-[34rem]").props('color=amber-8 label')
            ui.label().bind_text_from(self.sliderSwitchTime, 'value')
            ui.label("sec")
            ui.button("Update Speed", on_click=self.__buttonFunc_speedUpdate_1) \
                .props('icon=send color=amber-8')
            self.labelSent_SwitchSpeed_1 = ui.label()
        
        with ui.row().classes("items-center"):
            ui.button("Dec", on_click=self.__buttonFunc_decreaseSwitchTime) \
                .props('icon=keyboard_arrow_left color=amber-9')
            ui.button("Inc", on_click=self.__buttonFunc_increaseSwitchTime) \
                .props('icon=keyboard_arrow_right color=amber-9')

        
        # ===========================================
            
        with ui.row().classes("items-center"):
            ui.label("Switching Speed (2):") \
                .classes("text-bold text-lg")
            ui.label("Control approach time with train Speed and approach Distance") \
                .classes("text-lg text-[#ffecb3]")
            ui.label("A different way of controlling the switching speed.") \
                .classes("text-italic text-stone-200")
            
        with ui.row().classes("items-center"):
            self.inputTrainSpeed = ui.input(label='Train Speed (km/h)', placeholder=f'{SETTINGS["MIN_SPEED"]} - {SETTINGS["MAX_SPEED"]}',
                on_change=self.__calcFullTimeSec_FromDistSpeed,
                validation= {
                    'Speed too Low': lambda value: (int(value)) >= SETTINGS["MIN_SPEED"],
                    'Speed too High': lambda value: (int(value)) <= SETTINGS["MAX_SPEED"],
                }
            ).classes("w-[14rem]")

            self.inputTrainDistance = ui.input(label='Approach Distance (meters)', placeholder=f'{SETTINGS["MIN_DIST"]} - {SETTINGS["MAX_DIST"]}',
                on_change=self.__calcFullTimeSec_FromDistSpeed,
                validation= {
                    'Distance too Low': lambda value: (int(value)) >= SETTINGS["MIN_DIST"],
                    'Distance too High': lambda value: (int(value)) <= SETTINGS["MAX_DIST"],
                }
            ).classes("w-[14rem]")

            self.labelSwitchSpeed_2 = ui.label("***")
            ui.label("sec")
            ui.button("Update Speed", on_click=self.__buttonFunc_speedUpdate_2) \
                .props('icon=send color=amber-8')
            self.labelSent_SwitchSpeed_2 = ui.label()

    # ========================================================================================
    #   BUTTON FUNCTIONS    
    # ========================================================================================
    
    # decreaseEZ
    def __buttonFunc_startApproach(self):
        self.__comPort.writeSerial(txMessageCodes[ActionCodes.DECREASE_EZ])
        self.__systemMode.set_activeMode(ActionCodes.DECREASE_EZ)
        ui.notify('Train Approaching', position="top", type="info")
    
    def __buttonFunc_pauseApproach(self):
        self.__comPort.writeSerial(txMessageCodes[ActionCodes.IDLE])
        self.__systemMode.set_activeMode(ActionCodes.IDLE)
        ui.notify('Approach Paused', position="top", type="info")

    # increaseEZ
    def __buttonFunc_startDeparture(self):
        self.__comPort.writeSerial(txMessageCodes[ActionCodes.INCREASE_EZ])
        self.__systemMode.set_activeMode(ActionCodes.INCREASE_EZ)
        ui.notify('Train Departing', position="top", type="info")
    
    def __buttonFunc_pauseDeparture(self):
        self.__comPort.writeSerial(txMessageCodes[ActionCodes.IDLE])
        self.__systemMode.set_activeMode(ActionCodes.IDLE)
        ui.notify('Depature Paused', position="top", type="info")

    # resetEZ
    def __buttonFunc_resetEZHigh(self):
        self.__comPort.writeSerial(txMessageCodes[ActionCodes.RESET_HIGH_EZ])
        self.__systemMode.set_activeMode(ActionCodes.RESET_HIGH_EZ)
        self.__systemMode.set_stateNum(self.min_state)
        ui.notify('Set EZ=100', position="top", type="info")
    
    def __buttonFunc_resetEZLow(self):
        self.__comPort.writeSerial(txMessageCodes[ActionCodes.RESET_LOW_EZ])
        self.__systemMode.set_activeMode(ActionCodes.RESET_LOW_EZ)
        self.__systemMode.set_stateNum(self.max_state)
        ui.notify('Set EZ=0', position="top", type="info")

    # manual
    def __buttonFunc_setState(self):
        ui.notify(f"System state forced to: #{self.sliderSystemState.value}", position="top", type="info")   # <----------------------------- TODO
        self.__comPort.writeSerial(txMessageCodes[ActionCodes.SET_STATE])
        self.__systemMode.set_activeMode(ActionCodes.MANUAL)
        self.__systemMode.set_stateNum(self.sliderSystemState.value)
        self.__comPort.newSysState = True
        setStateActionCode: bytes = str(self.sliderSystemState.value).encode()
        self.__comPort.writeSerial(setStateActionCode)
        
    
    def __buttonFunc_increaseState(self):
        if self.sliderSystemState.value < self.max_state:
            self.sliderSystemState.value += 1
    
    def __buttonFunc_decreaseState(self):
        if self.sliderSystemState.value > self.min_state:
            self.sliderSystemState.value -= 1
        
    # speedConfig
    def __speedUpdate_main(self):
        ui.notify(f"Approach time updated to: {self.sliderSwitchTime.value} sec", position="top", type="info")

        self.__systemTime.set_speed_fromFullTime_ms(fullTime_ms=self.sliderSwitchTime.value*1_000)
        self.__systemTime.sendNewSwitchingTime()

    def __buttonFunc_speedUpdate_1(self):
        self.__speedUpdate_main()
        self.labelSent_SwitchSpeed_1.set_text("Update Sent")
        self.labelSent_SwitchSpeed_2.set_text("")

    def __buttonFunc_speedUpdate_2(self):
        self.__speedUpdate_main()
        self.labelSent_SwitchSpeed_2.set_text("Update Sent")
        self.labelSent_SwitchSpeed_1.set_text("")

    def __buttonFunc_increaseSwitchTime(self):
        if self.sliderSwitchTime.value < self.approach_t_max_sec:
            self.sliderSwitchTime.value += 1
    
    def __buttonFunc_decreaseSwitchTime(self):
        if self.sliderSwitchTime.value > self.approach_t_min_sec:
            self.sliderSwitchTime.value -= 1

    def __calcFullTimeSec_FromDistSpeed(self, x):
        try:
            distance = int(self.inputTrainDistance.value)
            speed_kmph = int(self.inputTrainSpeed.value)
            speed_mps = speed_kmph / 3.6
            time = int(distance / speed_mps)

            if (self.approach_t_min_sec > time) or (self.approach_t_max_sec < time):
                raise Exception()
        except:
            self.labelSwitchSpeed_2.set_text("???")
        else:
            self.labelSwitchSpeed_2.set_text(f"{time}")
            self.sliderSwitchTime.value = time