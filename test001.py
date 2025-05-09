import math
from Utils import SETTINGS

class DynamicSwitch:
    def __init__(self):
        self.switch_base_mult = SETTINGS["SWITCH_BASE_MULT"]
        self.max_state = SETTINGS["MAX_STATE"]
    
    def calcFullTime(self, baseTime_ms: int) -> int:
        '''
        Returns the full system switching time (from EZ=100 -> EZ=0).
        Full switching time is in milliseconds.
        '''
        fullTime_ms = 0
        for stateNum in range(0, self.max_state+1):
            fullTime_ms += self.getTimePerState(stateNum, baseTime_ms)
        
        return fullTime_ms
    
    
    def calcBaseStepTime(self, fullTime_ms: int) -> int:
        '''
        Returns the base step time for a given full switching time, in milliseconds.
        '''
        dynamicCoeff: float = 0
        for stateNum in range(0, self.max_state+1):
            dynamicCoeff += self.__dynamFuncNormalised(stateNum) * self.switch_base_mult + 1

        baseTime_ms: int = math.ceil(fullTime_ms / dynamicCoeff)
        return baseTime_ms

    def getTimePerState(self, stateNum: int, baseTime: int) -> int:
        '''
        Returns total time spent in a given state number, including the time adjustment. 
        Time is in ms.

        baseTime is in ms.
        stateNum is system state of microcontroller.
        '''
        
        # int timeAdjust = floor((7*pow(10, -6)*pow(stateNum, 2) - 0.0055*stateNum + 1.02) * (switchTime*SWITCH_BASE_MULT)); // c code from microcontroller
        timeAdjust: int = math.floor(self.__dynamFuncNormalised(stateNum) * (baseTime*self.switch_base_mult));
        timeStepFull: int =  baseTime + timeAdjust

        if stateNum == 1: print(timeStepFull)
        return timeStepFull


    def __dynamFuncNormalised(self, stateNum: int) -> float:
        '''Normalised dynamic function -> val range: [0, 1]'''
        timeAdjustNorm: float = 7*math.pow(10, -6)*math.pow(stateNum, 2) - 0.0055*stateNum + 1.02
        return timeAdjustNorm


def main():
    pass
    test01()
    print("---")
    test02()


def test01():
    dynamicCalc = DynamicSwitch()
    
    baseTime = 76*2

    fullTimeMs = dynamicCalc.calcFullTime(baseTime)
    print("Full Time:", fullTimeMs/1000, "sec")

    baseTimeMs = dynamicCalc.calcBaseStepTime(fullTimeMs)
    print("step Time:", baseTimeMs, "ms")

def test02():
    dynamicCalc = DynamicSwitch()
    
    fullTimeMs = 180_000

    baseTimeMs = dynamicCalc.calcBaseStepTime(fullTimeMs)
    print("step Time:", baseTimeMs, "ms")

    fullTimeMs = dynamicCalc.calcFullTime(baseTimeMs)
    print("Full Time:", fullTimeMs/1000, "sec")


main()