import json

def load_settings() -> dict:
    with open("SettingsComPort.json", "r") as json_file:
        return json.load(json_file)
    
settings_temp = load_settings()

# ========================================================================================
#   Add configurables to SETTINGS    
# ========================================================================================
SWITCH_T_MULT = 2           # constant for dividing switch period for serial transmission
SWITCH_BASE_MULT = 4        # constant coefficient used in dynamic switching function
MAX_STATE = 299             # max state number of microcontroller (State # ranges from 0 -> to MAX_STATE)

APPROACH_T_MIN_MS = 25_000      # minimum approach time in milliseconds
APPROACH_T_MAX_MS = 180_000     # maximum approach time in milliseconds
MAX_SPEED = 300     # maximum allowable speed in kph
MIN_SPEED = 10      # minimum allowable speed in kph
MAX_DIST = 3050     # maximum allowable distance in meters
MIN_DIST = 100      # minimum allowable distance in meters

settings_temp["SWITCH_T_MULT"] = SWITCH_T_MULT
settings_temp["SWITCH_BASE_MULT"] = SWITCH_BASE_MULT
settings_temp["MAX_STATE"] = MAX_STATE
settings_temp["MAX_STATE"] = MAX_STATE

settings_temp["APPROACH_T_MIN_MS"] = APPROACH_T_MIN_MS
settings_temp["APPROACH_T_MAX_MS"] = APPROACH_T_MAX_MS
settings_temp["MAX_SPEED"] = MAX_SPEED
settings_temp["MIN_SPEED"] = MIN_SPEED
settings_temp["MAX_DIST"] = MAX_DIST
settings_temp["MIN_DIST"] = MIN_DIST



# settings dictionary to be presented to other modules
SETTINGS = settings_temp