from nicegui import ui, app
from nicegui.events import KeyEventArguments
import time
import sys
from datetime import datetime

from DataProcessor import DataProcessor
from ComReader import ComReader
from ComPort import ComPort
from SystemState import SystemMode, SystemTimes
from DynamicSwitch import DynamicSwitch

from MessageLib import ActionCodes, txMessageCodes
from Utils import SETTINGS
from Logging import Log

from ClsPage1 import Page1MainBody
from ClsFooter import clsFooter
from ClsTimeProgressThread import TimeProgressThread
from ClsAutoTestCase import AutoTestCase
from StyleSettings import *

DEBUG = True
COMS_READ_INTERVAL = 1.0

class MainApp:
    """ Class for running main application """
    def __init__(self) -> None:
        # remove defualt page padding
        ui.query('.nicegui-content').classes('p-30 m-0 gap-0')

        # initialise comPort object
        self.comPort = ComPort(
            portNum=SETTINGS["ComPort"],
            baudrate=SETTINGS["Baudrate"],
            timeout=SETTINGS["ReadTimeoutSec"]
        )

        self.comPort.reset_input_buffer()

        # Handle data received from serial 
        self.comReader = ComReader(self.comPort)

        self.dynamSwitch: DynamicSwitch = DynamicSwitch()
        self.systemTime: SystemTimes = SystemTimes(
            comPort=self.comPort, 
            dynamicSwitch=self.dynamSwitch
        )
        self.systemMode: SystemMode = SystemMode()
        self.timeProgressThread = TimeProgressThread(
            systemTime=self.systemTime, 
            systemMode=self.systemMode, 
            dynamicSwitch=self.dynamSwitch
        )

        # page header
        self.add_header()
        # page body
        with ui.element('div').classes(f"w-full {C_MAIN_BODY_1} relative px-2 py-2"):
            self.add_main_body()
        # page footer
        with ui.footer().classes(f'{C_FOOTER_DEFAULT} p-[10px] text-lg text-gray-400'):
            self.add_footer()
        
        # self.add_new_page()

        # object for processing received serial data
        self.dataProcessor = DataProcessor(self.headerRow, self.clockLabel)
        # add key bindings
        self.keyboard = ui.keyboard(on_key=self.handle_key)

        # start Async timers
        time.sleep(2.0)
        self.timerCheckComsHealth = ui.timer(5.0, self.startup_transaction)
        self.timerReadSerial = ui.timer(COMS_READ_INTERVAL, self.serviceRxData)

        if DEBUG:
            self.dataProcessor.processCharCode(b'<253>')


    def startup_transaction(self):
        
        if self.dataProcessor.checkACK():
            Log.log("Arduino connected successfully.")
            self.label_controllerCommsHealth.classes(replace=self.style_indLabel_connect)
            self.label_controllerCommsHealth.set_text("Connected")

            self.timerCheckComsHealth.deactivate()
            ui.notify("Arduino connected successfully", type='positive', position='center', progress=True, timeout=3_000)

            self.initialise_switchingSpeed()
            return 
        
        else:
            Log.log("Attempting to establish connection to Arduino.")

            msg: bytes = txMessageCodes[ActionCodes.HMI_HELLO]
            self.comPort.writeSerial(msg)
            
    def initialise_switchingSpeed(self):
        self.systemTime.set_defaults()
        self.systemTime.sendNewSwitchingTime()


    # ========================================================================================
    #   Header
    # ========================================================================================
    def add_header(self):
        # header spacing allocation
        basis_title = 30
        basis_statusText = 40
        basis_clock = 15
        basis_menu = 15
        # add header elements
        self.headerRow = ui.header().classes(f'flex flex-row py-8 px-4 no-wrap h-[5vh] {C_HEADER_DEFAULT} items-center')
        with self.headerRow:
            # Header title text & icon
            with ui.row().classes(f"basis-[{basis_title}%] items-center"):
                ui.icon("train", color="#818cf8"). \
                    classes(f"text-5xl")
                ui.html('GCP Simulator <a class="text-bold text-[#818cf8]">HMI</a>'). \
                    classes(f"text-lg text-left")
            
            # Controller status labels
            with ui.row().classes(f"basis-[{basis_statusText}%] flex-row justify-center text-lg"):
                self.style_indLabel_connect = "text-center text-teal-200"
                self.style_indLabel_disconnect = "text-center text-rose-300"
                self.style_indLabel_deactive = "text-center text-stone-500"

                ui.label("Controller Status: ") \
                    .classes("text-center text-bold text-[#818cf8]")
                self.label_controllerCommsHealth = ui.label("Disconnected") \
                    .classes(self.style_indLabel_disconnect)
            
            # TODO: remove from function, and take as input.
                # issue with different pages creating their own instance. Should all refer back to single object, which gives them the time string.
                # will be a similar system for updating controller status
            # clock  
            with ui.row().classes(f"basis-[{basis_clock}%] items-center justify-center gap-0 flex-row"):
                # ui.element('div').classes("basis-[25%]")
                # with ui.row().classes("basis-[75%]"):
                #     ui.icon("schedule", color="#818cf8"). \
                #         classes(f"text-3xl")
                self.clockLabel = ui.label("HH:MM:SS").classes(f"text-lg text-left pl-[3px] text-stone-200")
            ui.timer(1.0, self.update_time)

            # drop down menu    
            with ui.row().classes(f"basis-[{basis_menu}%] items-center"):
                ui.label("Menu").classes(f"text-lg text-right pr-[5px] ml-auto")
                self.create_menu()

    def create_menu(self):
        with ui.button(icon='menu', color="indigo-500"):
            with ui.menu() as menu:
                if SETTINGS['Testing']:
                    # ui.menu_item(
                    #     'TBD', 
                    #     lambda: self.dataProcessor.processCharCode(b'<103>'), 
                    #     auto_close=False
                    # )
                    # ui.menu_item(
                    #     'TBD', 
                    #     lambda: self.dataProcessor.processCharCode(b'<110>'), 
                    #     auto_close=False
                    # )
                    # ui.menu_item(
                    #     'TBD', 
                    #     lambda: self.dataProcessor.processCharCode(b'<101>'), 
                    #     auto_close=False
                    # )
                    ui.menu_item(
                        'TBD', 
                        lambda: self.dataProcessor.processCharCode(b'<102>'), 
                        auto_close=False
                    )
                    ui.separator()

                ui.menu_item(
                    'ACK_HELLO (H)', 
                    lambda: self.dataProcessor.processCharCode(b'<253>'),
                    auto_close=False
                )
                ui.menu_item(
                    'Test-btn-01', 
                    self.menu_testBtn01,
                    auto_close=False
                )
                ui.menu_item(
                    'TBD', 
                    lambda: print("VideoSelector.setSource(2)"),
                    auto_close=False
                )
                ui.separator()
                
                ui.menu_item('Terminate Application (K)', self.app_shutdown)
                ui.separator()
                
                ui.menu_item('Close', on_click=menu.close)
            
    def update_time(self):
            self.clockLabel.set_text(f"{datetime.now().strftime('%I:%M:%S')}")

    
    # ========================================================================================
    #   Page Elements
    # ========================================================================================
    def add_main_body(self):
        Page1MainBody(
            comPort=self.comPort, 
            systemTime=self.systemTime, 
            systemMode=self.systemMode,
        )
    
    def add_footer(self):
        clsFooter(
            systemTime=self.systemTime, 
            systemMode=self.systemMode, 
            timeProgressThread=self.timeProgressThread 
        )


    # ========================================================================================
    #   Key Bindings
    # ========================================================================================
    def handle_key(self, e: KeyEventArguments):
        if (not e.action.keydown) or (e.action.repeat):
            return
        if (e.key == 'h'):
            print("Key Pressed: H")
            self.dataProcessor.processCharCode(b'<253>'),
        elif (e.key == 'k'):
            print("Key Pressed: K")
            self.app_shutdown()
        elif (e.key == 'd'):
            print("Key Pressed: D")
            # self.eyeTrackingDisable()
        elif (e.key == 'c'):
            print("Key Pressed: C") # switch to front webcam feed
            # VideoSelector.setSource(0)
        elif (e.key == 'b'):
            print("Key Pressed: B") # switch to backward webcam feed
            # VideoSelector.setSource(1)


    # ========================================================================================
    #   Manage Data Received
    # ========================================================================================
    def serviceRxData(self):
        while True:
            actionCode = self.comReader.popNextMessage()
            if actionCode == None:
                return  # no data to process
            self.dataProcessor.processCharCode(actionCode)

    # ========================================================================================
    #   Testing Ground
    # ========================================================================================
    def testButton(self):
        print(self.comReader._rxDataQueue)

    def menu_testBtn01(self):
        print("Test Button pressed")
        AutoTestCase()

    # ========================================================================================
    #   NEW PAGE
    # ========================================================================================
    def add_new_page(self):
        @ui.page('/page_layout')
        def page_layout():
            self.add_header()

            with ui.left_drawer(top_corner=False, bottom_corner=False).classes(f'{C_SIDE_DRAWER}'):
                ui.label('LEFT DRAWER')

            with ui.right_drawer(fixed=False).classes(f'{C_SIDE_DRAWER}').props('bordered') as right_drawer:
                ui.label('RIGHT DRAWER')

            with ui.footer().classes(f'{C_HEADER_DEFAULT}'):
                ui.label('FOOTER')

            # with ui.column.classes(f'bg-[#0d326b] px-15 py-25'):
            with ui.column().classes(f'bg-[#0d326b] px-20 py-14 mx-5 my-2'):
                ui.label('CONTENT')
                [ui.label(f'Line {i}') for i in range(100)]

        # with ui.element('div').classes('flex flex-row text-lg flex-nowrap w-full h-full absolute'):
        with ui.element('div'):
            ui.link('show page with fancy layout', page_layout)
    
    # ========================================================================================
    #   System Shutdown
    # ========================================================================================
    def app_shutdown(self):
        ui.notify("System is shutting down.", type='negative', position='center', progress=False, close_button="OK", timeout=10_000)
        Log.log("Shutting Down Application.")
        app.shutdown()


# =====================================

def main():
    print("="*30)
    Log.log("Application Start")
    print("="*30)

    mainApp = MainApp()
    ui.run(
        title="GCP Simulator HMI", 
        host='127.0.0.1',
        port=10_000,
        dark=True,
        favicon='🚂',
        show=False,
        reload=False
    )

if __name__ in {"__main__", "__mp_main__"}:
    print("Python used:", sys.executable)
    main()

