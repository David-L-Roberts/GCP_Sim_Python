from Utils import SETTINGS
from Logging import Log
from DynamicSwitch import DynamicSwitch
from ComPort import ComPort
from MessageLib import ActionCodes, txMessageCodes


class SystemMode:
    '''
    Class for managing system's mode of switching.
    '''
    def __init__(self):
        self.__activeMode: ActionCodes = ActionCodes.IDLE
        self.__stateNum: int = 0

        self.__subscribersActiveMode: list = []
        self.__subscribersStateNum: list = []

    def set_activeMode(self, newMode: ActionCodes):
        self.__activeMode = newMode
        self.__updateSubscribers_activeMode()
    
    def get_activeMode(self):
        return self.__activeMode
    
    def set_stateNum(self, newStateNum: int):
        self.__stateNum = newStateNum
        self.__updateSubscribers_stateNum()

    def get_stateNum(self):
        return self.__stateNum
    
    # ===========================================

    def subscribeTo_activeModeChange(self, callFunc: callable):
        self.__subscribersActiveMode.append(callFunc)
    
    def __updateSubscribers_activeMode(self):
        callFunc: callable = None
        for callFunc in self.__subscribersActiveMode:
            callFunc()

    def subscribeTo_stateNumChange(self, callFunc: callable):
        self.__subscribersStateNum.append(callFunc)
    
    def __updateSubscribers_stateNum(self):
        callFunc: callable = None
        for callFunc in self.__subscribersStateNum:
            callFunc()
    

# ========================================================================================

class SystemTimes:
    '''
    Class for managing time data related to relay switching periods.
    Provides and sets info about:
        - base-step-period
        - total approach time
        - progress of system towards total approach time
    '''
    def __init__(self, comPort: ComPort, dynamicSwitch: DynamicSwitch):
        self.__comPort: ComPort = comPort
        self.__dynamSwitch: DynamicSwitch = dynamicSwitch

        self.__subscribersFullTime: list = []
        self.__subscribersProgTime: list = []

        self.__approachProgTime_ms: int = None  # progress of total approach time
        self.__approachFullTime_ms: int = None  # total approach time for run
        self.__baseStepPeriod_ms: int = None
        self.__speed_kph: int = None
        self.__distance_m: int = None

        self.switch_t_mult = SETTINGS["SWITCH_T_MULT"]
        self.approach_t_min_sec = int(SETTINGS["APPROACH_T_MIN_MS"]/1000)
        self.approach_t_max_sec = int(SETTINGS["APPROACH_T_MAX_MS"]/1000)

    
    def set_defaults(self):
        self.set_speed_fromFullTime_ms(SETTINGS["DEFUALT_FULL_TIME_MS"])
        self.set_approachProgTime(0)

    # ===========================================

    def set_speed_fromFullTime_ms(self, fullTime_ms: int):
        self.__approachFullTime_ms = fullTime_ms
        self.__baseStepPeriod_ms = self.__dynamSwitch.calcBaseStepTimeMs(fullTime_ms=self.__approachFullTime_ms)

        self.__updateSubscribers_fullTime()

        Log.log(f"New switching speed set. Full approach time (ms) set to: {self.__approachFullTime_ms }", Log.INFO)
        Log.log_file(f"base step period (ms) set to: {self.__baseStepPeriod_ms }", Log.DEBUG)

    def set_speed_fromDistanceAndKPH(self, distance_m: int, speed_kph: int):
        self.__speed_kph = int(speed_kph)
        self.__distance_m = int(distance_m)

        fullTime_sec = self.__calcFullTime_Sec_FromDistSpeed(self.__distance_m, self.__speed_kph)
        self.__approachFullTime_ms = fullTime_sec * 1000

        self.set_speed_fromFullTime_ms(fullTime_ms=self.__approachFullTime_ms)

    def set_approachProgTime(self, stateNum: int):
        self.__approachProgTime_ms = self.__dynamSwitch.getProgressTimeMs(stateNum=stateNum)
        self.__updateSubscribers_progTime()

    # ===========================================

    def get_approachFullTime_ms(self):
        return self.__approachFullTime_ms
    
    def get_approachFullTime_sec(self):
        return int(self.__approachFullTime_ms / 1000)
    
    def get_baseStepPeriod_ms(self):
        return self.__baseStepPeriod_ms
    
    def get_approachProgTime_ms(self):
        return self.__approachProgTime_ms
    
    # ===========================================

    def sendNewSwitchingTime(self):
        self.__comPort.writeSerial(txMessageCodes[ActionCodes.CHANGE_SWITCH_T])
        self.__comPort.newSwitchTime = True
        switchTActionCode: bytes = str(int(self.__baseStepPeriod_ms / self.switch_t_mult)).encode()
        self.__comPort.writeSerial(switchTActionCode)


    # ===========================================

    def __calcFullTime_Sec_FromDistSpeed(self, distance_m: int, speed_kph: int):
        speed_mps = speed_kph / 3.6
        fullTime_sec = int(distance_m / speed_mps)

        if (self.approach_t_min_sec > fullTime_sec):
            Log.log(f"invalid speed and distance combination, resulting in bad approach time: {fullTime_sec}. \
                    Setting default time of {self.approach_t_min_sec}", Log.ERROR)
        elif (self.approach_t_max_sec < fullTime_sec):
            Log.log(f"invalid speed and distance combination, resulting in bad approach time: {fullTime_sec}. \
                    Setting default time of {self.approach_t_max_sec}", Log.ERROR)
        
        return fullTime_sec

    # ===========================================

    def subscribeTo_fullTimeChange(self, callFunc: callable):
        self.__subscribersFullTime.append(callFunc)
    
    def __updateSubscribers_fullTime(self):
        callFunc: callable = None
        for callFunc in self.__subscribersFullTime:
            callFunc()

    def subscribeTo_progTimeChange(self, callFunc: callable):
        self.__subscribersProgTime.append(callFunc)

    def __updateSubscribers_progTime(self):
        callFunc: callable = None
        for callFunc in self.__subscribersProgTime:
            callFunc()
