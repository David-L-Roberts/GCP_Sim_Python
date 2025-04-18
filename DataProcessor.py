from Logging import Log
from nicegui import ui
from MessageLib import ActionCodes, txMessageCodes, msgTypeLookup
import time

C_HEADER_DEFAULT = "bg-[#0d1117]"
C_HEADER_STOP = "bg-rose-900"

MAX_DIST_VAL = 500  # max distance reading of sensor, in cm
CONV_FACT = MAX_DIST_VAL/255    # conversion factor for distance reading

class DataProcessor:
    def __init__(self, headerRow: ui.header, distanceLabel: ui.label) -> None:
        # match action codes to service functions
        self.processorDict = {
            txMessageCodes[ActionCodes.HMI_ACK]:            self.__service_ACK,
            txMessageCodes[ActionCodes.INCREASE_EZ]:        self.__service_breakEnabled,
            txMessageCodes[ActionCodes.RESET_HIGH_EZ]:      self.__service_breakDisabled,
            txMessageCodes[ActionCodes.RESET_LOW_EZ]:       self.__service_stopEnabled,
            txMessageCodes[ActionCodes.MANUAL]:             self.__service_stopDisabled,
            txMessageCodes[ActionCodes.IDLE]:               self.__service_stopDisabled,
            }
        # var for holding distance sensor reading
        self.dataVal = ""
        # store reference to header row element
        self.headerRow = headerRow
        # store reference to distance label element
        self.distlabel = distanceLabel
        # flag for acknowledgement reception
        self.recACK = False

    def processCharCode(self, charCode: bytes):
        charCode_Str = charCode.decode()
        # check for starting and ending chars
        if ((charCode_Str[0] != '<') and (charCode_Str[-1] != '>')):
            Log.log(f"Received Message <- {charCode_Str}", Log.INFO)
            return

        charCode_bytes = charCode[1:-1]   # strip < & >

        try:
            func = self.processorDict[charCode_bytes]
        except KeyError:
            Log.log(f"Cannot process char code ({charCode_bytes}) in {DataProcessor}.", Log.WARNING)
        else:
            Log.log(f"Received Action Code <- {msgTypeLookup[charCode_bytes]} ({charCode_bytes.decode()})", Log.INFO)
            func()
    
    def __service_ACK(self):
        Log.log("Processing: ACK", Log.DEBUG)
        self.recACK = True

    def checkACK(self):
        """Returns `True` if an ACK was received. Will reset ACK flag."""
        response = self.recACK
        self.recACK = False
        return response

    

    # ====================================================================
    #   LEGACY REFERENCE
    # ====================================================================
    
    def __service_breakEnabled(self):
        Log.log("Automatic Breaking ACTIVATED.")
        ui.notify("Automatic Breaking Activated. Forward movement prevented.", type='warning', position='center', progress=True, timeout=4_000)
    
    def __service_breakDisabled(self):
        Log.log("Automatic Breaking RELEASED.")
        ui.notify("Automatic Breaking Released.", type='positive', position='center', progress=True, timeout=3_000)
    
    def __service_stopEnabled(self):
        Log.log("Emergency Stop ACTIVATED.")
        ui.notify("Emergency Stop Activated. All movement is disabled.", type='negative', position='center', progress=True, timeout=5_000)
        self.headerRow.classes(remove=C_HEADER_DEFAULT, add=C_HEADER_STOP)
    
    def __service_stopDisabled(self):
        Log.log("Emergency Stop DEACTIVATED.")
        ui.notify("Emergency Stop Deactivated. Movement enabled.", type='positive', position='center', progress=True, timeout=4_000)
        self.headerRow.classes(remove=C_HEADER_STOP, add=C_HEADER_DEFAULT)
    