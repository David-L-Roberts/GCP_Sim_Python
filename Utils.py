import json

def load_settings():
    with open("SettingsComPort.json", "r") as json_file:
        return json.load(json_file)
    
SETTINGS = load_settings()