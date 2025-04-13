from nicegui import ui
from MessageLib import ActionCodes
from SystemState import SystemMode, SystemTimes
from ClsTimeProgressThread import TimeProgressThread

class clsFooter:
    def __init__(self, systemTime: SystemTimes, systemMode: SystemMode, timeProgressThread: TimeProgressThread):
        self.__systemTime = systemTime 
        self.__systemMode = systemMode
        self.timeProgressThread = timeProgressThread
        
        self.totalTime_sec: int = 0
        self.progressTime_sec: int = 0

        self.__add_footer()

        self.__systemTime.subscribeTo_fullTimeChange(self.updateTotalApproachTime)
        self.__systemTime.subscribeTo_progTimeChange(self.updatePogressApproachTime)
        self.__systemMode.subscribeTo_activeModeChange(self.update_activeMode)

    def __add_footer(self):
        with ui.row().classes("gap-[5px] ml-[20px]"):
            ui.label("Active Mode: ").classes("font-bold")
            self.label_activeMode = ui.label(ActionCodes.IDLE)
        
        with ui.row().classes("gap-[5px]"):
            minTime = 25
            currentTime = 35
            totalTime = 120

            percentProgress = currentTime / totalTime

            ui.label("Approach Time progress: ").classes("font-bold")
            self.label_progressTime_sec = ui.label(currentTime)

            self.label_totalTime_sec = ui.label(f"/ {totalTime} sec")
            self.progressBar_approach = ui.linear_progress(value=0, show_value=False, color="indigo-300")

        with ui.row().classes("gap-[5px] mr-[20px]"):
            ui.label("Current Sys State:").classes("font-bold")
            ui.label("00")
            ui.label("/ 299")
    
    # ===========================================

    def updateTotalApproachTime(self):
        self.totalTime_sec = self.__systemTime.get_approachFullTime_sec()
        self.label_totalTime_sec.set_text(f"/ {self.totalTime_sec} sec")
        # self.__updateProgressBar()
    
    def updatePogressApproachTime(self):
        print("prog time subscriber activated!")
        self.progressTime_sec = self.__systemTime.get_approachProgTime_ms()
        self.label_progressTime_sec.set_text(self.progressTime_sec)
        self.__updateProgressBar()

    def __updateProgressBar(self):
        percentProgress = self.progressTime_sec / self.totalTime_sec
        self.progressBar_approach.set_value(percentProgress)
    
    def update_activeMode(self):
        self.label_activeMode.set_text(self.__systemMode.get_activeMode())