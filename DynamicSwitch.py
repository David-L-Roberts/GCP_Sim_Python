import math
from Utils import SETTINGS
import array

class DynamicSwitch:
    def __init__(self):
        self.switch_base_mult = SETTINGS["SWITCH_BASE_MULT"]
        self.max_state = SETTINGS["MAX_STATE"]

        self.__lookup_stateNumToProgTimeMs: array.array = array.array('I', [0]*(self.max_state+1))
        self.__lookup_stateNumToDelayMs: array.array = array.array('I', [0]*(self.max_state+1))
        self.__fullTime_ms: int = 0
        self.__baseTime_ms: int = 0
    
    def calcBaseStepTimeMs(self, fullTime_ms: int) -> int:
        '''
        Returns the base step time for a given full switching time, in milliseconds.
        '''
        dynamicCoeff: float = 0
        for stateNum in range(0, self.max_state+1):
            dynamicCoeff += self.__dynamFuncNormalised(stateNum) * self.switch_base_mult + 1

        baseTime_ms: int = math.ceil(fullTime_ms / dynamicCoeff)
        self.__populateLookupTables(baseTime_ms=baseTime_ms)
        return baseTime_ms

    # ===========================================
    
    def __populateLookupTables(self, baseTime_ms: int):
        self.__baseTime_ms = baseTime_ms
        timeProgress_ms: int = 0
        for stateNum in range(0, self.max_state+1):
            self.__lookup_stateNumToProgTimeMs[stateNum] = timeProgress_ms

            delayTime = self.__calcStateDelayMs(stateNum, baseTime_ms)
            timeProgress_ms += delayTime
            
            self.__lookup_stateNumToDelayMs[stateNum] = delayTime
        
        print("populate Lookup tables")
        print(self.__lookup_stateNumToProgTimeMs[self.max_state])
        print(self.__lookup_stateNumToProgTimeMs[0])
        print(timeProgress_ms)
        self.__fullTime_ms = timeProgress_ms

    def __calcStateDelayMs(self, stateNum: int, baseTime_ms: int) -> int:
        '''
        Returns total time spent in a given state number, including the time adjustment. 
        Time is in ms.

        baseTime is in ms.
        stateNum is system state of microcontroller.
        '''
        
        # int timeAdjust = floor((7*pow(10, -6)*pow(stateNum, 2) - 0.0055*stateNum + 1.02) * (switchTime*SWITCH_BASE_MULT)); // c code from microcontroller
        timeAdjust_ms: int = math.floor(self.__dynamFuncNormalised(stateNum) * (baseTime_ms*self.switch_base_mult))
        timeStepFull_ms: int =  baseTime_ms + timeAdjust_ms
        return timeStepFull_ms


    def __dynamFuncNormalised(self, stateNum: int) -> float:
        '''Normalised dynamic function -> val range: [0, 1]'''
        timeAdjustNorm: float = 7*math.pow(10, -6)*math.pow(stateNum, 2) - 0.0055*stateNum + 1.02
        return timeAdjustNorm

    # ===========================================

    def getStateDelayMs(self, stateNum: int):
        return self.__lookup_stateNumToDelayMs[stateNum]
    
    def getProgressTimeMs(self, stateNum: int):
        return self.__lookup_stateNumToProgTimeMs[stateNum]
    
    def getFullTimeMs(self) -> int:
        '''
        Returns the full system switching time (from EZ=100 -> EZ=0).
        Full switching time is in milliseconds.
        '''
        return self.__fullTime_ms