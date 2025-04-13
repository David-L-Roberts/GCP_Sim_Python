from Utils import SETTINGS
from Logging import Log
import threading
import time
from MessageLib import ActionCodes
from DynamicSwitch import DynamicSwitch
from SystemState import SystemMode, SystemTimes

class TimeProgressThread:
    '''
    Starts a thread used for estimating the apporach time progress.
    '''
    def __init__(self, systemTime: SystemTimes, systemMode: SystemMode, initial_baseStepT=1.0, initial_stateNum: int=0):
        self._systemTime: SystemTimes = systemTime
        self._systemMode: SystemMode = systemMode

        self._stateNum = initial_stateNum
        self._baseStepT = initial_baseStepT
        self._direction = 1
        # self._delay = None
        self._delay = initial_stateNum

        self.max_state = SETTINGS["MAX_STATE"]
        self.min_state = 0

        self.target_function = self.mainThreadFunc
        self._stop_event = threading.Event()
        self._pause_event = threading.Event()
        self._pause_event.clear()  # Start in paused state
        self._lock = threading.Lock()

        self._dynamSwitch: DynamicSwitch = DynamicSwitch()

        self._systemMode.subscribeTo_activeModeChange(self.threadActiveCheck)

        self._thread = threading.Thread(target=self._run, daemon=True)

    def _run(self):
        while not self._stop_event.is_set():
            self._pause_event.wait()  # Wait here if paused
            self.target_function()
            print("Cycle")
            with self._lock:
                current_delay = self._delay
            time.sleep(current_delay)

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
        print("Thread Resuming")
        self._pause_event.set()
        self._direction = direction

    def is_paused(self):
        return not self._pause_event.is_set()

    def threadActiveCheck(self):
        activeMode = self._systemMode.get_activeMode()
        print(activeMode)
        if (activeMode == ActionCodes.DECREASE_EZ):
            self.resume(direction=1)
        elif (activeMode == ActionCodes.INCREASE_EZ):
            self.resume(direction=-1)
        elif (activeMode == ActionCodes.IDLE) or \
            (activeMode == ActionCodes.MANUAL):
            self.pause()
        elif (activeMode == ActionCodes.RESET_HIGH_EZ):
            self.set_stateNum(self.min_state)
            self.pause()
        elif (activeMode == ActionCodes.RESET_LOW_EZ):
            self.set_stateNum(self.max_state)
            self.pause()
        else:
            Log.log(f"Unexpected activeMode read in timeProgressThread: {activeMode}", Log.ERROR)
            self.pause()
            
            
            
    # ===========================================

    def set_baseStepT(self, new_baseTime):
        with self._lock:
            self._baseStepT = new_baseTime

    def get_baseStepT(self):
        with self._lock:
            return self._baseStepT

    def set_stateNum(self, new_stateNum):
        with self._lock:
            self._stateNum = new_stateNum

    def get_stateNum(self):
        with self._lock:
            return self._stateNum

    # ===========================================

    def mainThreadFunc(self):
        self._delay = self._dynamSwitch.getTimePerState(stateNum=self._stateNum, baseTime=self._baseStepT)
        self._stateNum += self._direction    # TODO <--- doesn't account for skipped states at low switching times ???
        progressTime_ms = self._systemTime.get_approachProgTime_ms() + self._delay
        print()
        self._systemTime.set_approachProgTime_ms(progressTime_ms)

        if (self._stateNum >= self.max_state) or (self._stateNum <= self.min_state):
            self.pause()
