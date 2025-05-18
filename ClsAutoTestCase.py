from nicegui import ui, events
import json


class AutoTestCase():
    
    def __init__(self, x):
        print("AutoTestCase init running")
        self.loadTestCaseFile()

    def loadTestCaseFile(self):
        self.__select_file()
        with open("SettingsComPort.json", "r") as json_file:
            return json.load(json_file)
    
    def __select_file(self):
        ui.upload(
            on_upload=self.__handle_fileUpload,
            label="Select a json test case file.",
            auto_upload=True,
            # accept=".json"
        )

    def __handle_fileUpload(self, e: events.UploadEventArguments):
        print(f"File uploaded: {e.name}")
        self.uploadIO = json.load(e.content)
        print(self.uploadIO)