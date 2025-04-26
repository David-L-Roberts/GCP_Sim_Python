from Logging import Log
import threading
import time
from MessageLib import ActionCodes
from DynamicSwitch import DynamicSwitch
from SystemState import SystemMode, SystemTimes
from Utils import SETTINGS

class TimeProgressThread:
    '''
    Starts a thread used for estimating the apporach time progress.
    '''
    def __init__(self, systemTime: SystemTimes, systemMode: SystemMode, initial_baseStepT_sec=1.0):
        self._systemTime: SystemTimes = systemTime
        self._systemMode: SystemMode = systemMode

        self._baseStepT_ms = initial_baseStepT_sec*1000
        self._direction = 1
        # self._delay = None
        self._delay_ms = 0

        self.max_state = SETTINGS["MAX_STATE"]
        self.min_state = 0

        self.target_function = self.mainThreadFunc
        self._stop_event = threading.Event()
        self._pause_event = threading.Event()
        self._pause_event.set()  # Start in paused state
        self._lock = threading.Lock()

        self._dynamSwitch: DynamicSwitch = DynamicSwitch()

        self._systemMode.subscribeTo_activeModeChange(self.threadActiveCheck)
        self._systemTime.subscribeTo_fullTimeChange(self.set_baseStepT)

        self._thread = threading.Thread(target=self._run, daemon=True)

    def _run(self):
        print("Thread running.")
        while not self._stop_event.is_set():
            self._pause_event.wait()  # Wait here if paused
            self.target_function()
            print("Cycle")
            with self._lock:
                current_delay_sec = float(self._delay_ms) / 1000
                print("current_delay_sec", current_delay_sec)
            time.sleep(current_delay_sec)

    def start(self, direction=1):
        ''' 
        direction:
            +1 for approach (decrease EZ)
            -1 for departure (increase EZ)
        '''
        if not self._thread.is_alive():
            self._thread.start()
            self._direction = direction

    def stop(self):
        self._stop_event.set()
        self.resume()  # Ensure it’s not stuck paused
        self._thread.join()

    def pause(self):
        print("Thread Paused")
        self._pause_event.clear()

    def resume(self, direction=1):
        ''' 
        direction:
            +1 for approach (decrease EZ)
            -1 for departure (increase EZ)
        '''
        print("Thread Resuming")
        self._pause_event.set()
        self._direction = direction
        self.start()

    def is_paused(self):
        return not self._pause_event.is_set()

    def threadActiveCheck(self):
        activeMode = self._systemMode.get_activeMode()
        print("threadActiveCheck", activeMode)
        if (activeMode == ActionCodes.DECREASE_EZ):
            self.resume(direction=1)
        elif (activeMode == ActionCodes.INCREASE_EZ):
            self.resume(direction= -1)
        elif (activeMode == ActionCodes.IDLE) or \
            (activeMode == ActionCodes.MANUAL):
            self.pause()
        elif (activeMode == ActionCodes.RESET_HIGH_EZ):
            self._systemMode.set_stateNum(self.min_state)
            self.pause()
        elif (activeMode == ActionCodes.RESET_LOW_EZ):
            self._systemMode.set_stateNum(self.max_state)
            self.pause()
        else:
            Log.log(f"Unexpected activeMode read in timeProgressThread: {activeMode}", Log.ERROR)
            self.pause()
            
            
            
    # ===========================================

    def set_baseStepT(self):
        new_baseTime_ms = self._systemTime.get_baseStepPeriod_ms()
        with self._lock:
            self._baseStepT_ms = new_baseTime_ms

    def get_baseStepT(self):
        with self._lock:
            return self._baseStepT_ms

    # ===========================================

    def mainThreadFunc(self):
        # state number bounds checking
        stateNum = self._systemMode.get_stateNum()
        if ((stateNum >= self.max_state) and (self._direction == 1)) \
                or ((stateNum <= self.min_state) and (self._direction == -1)):
            print("StateNum Threshold Reached", stateNum)
            self.pause()
            return
        
        # move to next state
        self._delay_ms = self._dynamSwitch.getTimePerState(stateNum=stateNum, baseTime_ms=self._baseStepT_ms)
        progressTime_ms = self._systemTime.get_approachProgTime_ms() + (self._direction * self._delay_ms)
        
        stateNum += self._direction    # TODO <--- doesn't account for skipped states at low switching times ???
        self._systemMode.set_stateNum(stateNum)

        # DEBUG
        print("_direction", self._direction)
        print("_stateNum: ", stateNum)

        # TODO: change progress time to come from stateNum, instead of adding up delay times 
            # getApproachProgTime_ms(stateNum) -> use dynamic func to get progress time or percent of fullTime
            # will also help solve rounding issues.
        self._systemTime.set_approachProgTime_ms(progressTime_ms)

        
