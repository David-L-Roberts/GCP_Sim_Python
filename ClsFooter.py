from nicegui import ui
from MessageLib import ActionCodes
from SystemState import SystemMode, SystemTimes
from ClsTimeProgressThread import TimeProgressThread
from Utils import SETTINGS


class clsFooter:
    def __init__(self, systemTime: SystemTimes, systemMode: SystemMode, timeProgressThread: TimeProgressThread):
        self.__systemTime = systemTime 
        self.__systemMode = systemMode
        self.timeProgressThread = timeProgressThread
        
        self.totalTime_sec: int = 0
        self.progressTime_sec: int = 0

        with ui.row().classes("w-screen flex flex-row justify-between"):
            self.__add_footer()

        self.__systemTime.subscribeTo_fullTimeChange(self.updateTotalApproachTime)
        self.__systemTime.subscribeTo_progTimeChange(self.updatePogressApproachTime)
        self.__systemMode.subscribeTo_activeModeChange(self.update_activeMode)
        self.__systemMode.subscribeTo_stateNumChange(self.update_stateNum)

    def __add_footer(self):
        with ui.row().classes("gap-[5px] ml-[20px] basis-[260px] flex-row justify-start"):
            ui.label("Active Mode: ").classes("font-bold")
            self.label_activeMode = ui.label(ActionCodes.IDLE)
        
        with ui.row().classes("gap-[5px] flex-row basis-[35%] flex-row justify-center"):
            currentTime = 0
            totalTime = 0

            ui.label("Approach Time progress: ").classes("font-bold")
            self.label_progressTime_sec = ui.label(currentTime)

            self.label_totalTime_sec = ui.label(f"/ {totalTime} sec")
            self.progressBar_approach = ui.linear_progress(value=0, show_value=False, color="indigo-300")

        with ui.row().classes("gap-[5px] mr-[20px] basis-[260px] flex-row justify-end"):
            ui.label("Current Sys State:").classes("font-bold")
            self.label_stateNum  = ui.label("0")
            ui.label(f"/ {SETTINGS['MAX_STATE']}")
    
    # ===========================================

    def updateTotalApproachTime(self):
        self.totalTime_sec = self.__systemTime.get_approachFullTime_sec()
        self.label_totalTime_sec.set_text(f"/ {self.totalTime_sec} sec")
        # self.__updateProgressBar()
    
    def updatePogressApproachTime(self):
        self.progressTime_sec = round(self.__systemTime.get_approachProgTime_ms()/1000)
        self.label_progressTime_sec.set_text(self.progressTime_sec)
        self.__updateProgressBar()

    def __updateProgressBar(self):
        if self.totalTime_sec == 0:
            percentProgress = 0
        else:
            percentProgress = self.progressTime_sec / self.totalTime_sec
        
        self.progressBar_approach.set_value(percentProgress)
    
    def update_activeMode(self):
        self.label_activeMode.set_text(self.__systemMode.get_activeMode())
    
    def update_stateNum(self):
        self.label_stateNum.set_text(self.__systemMode.get_stateNum())