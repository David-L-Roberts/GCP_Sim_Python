# GCP Simulator HMI
 HMI application for controlling GCP simulator hardware.
 Runs as a locally hosted web app, accessed through the browser.

## Requirements
Python version = 3.10.4
Run `install_library_requirements.bat` to create local python virtual environment and automatically install all library dependencies.

Specific libraries for reference:
- `pip install nicegui`
- `pip install pywebview`
- `pip install pyserial`

note: it is easy to install incompatible versions of these libraries, which will cause the application to fail. The `requirements.txt` file species the library versions that were proven to work during development.

## References
- [NiceGui Docs](https://nicegui.io/documentation)
- [Tailwind Docs](https://v2.tailwindcss.com/docs)
- [Quasar Framework Docs](https://quasar.dev/docs)


## Known Issues
- Serial Debug message: when recieving data on serial port, does not count the number of bytes recieved properly (All data is read properly. It simply displays the wrong byte count).

## To Do
- Change switching on Microcontroller to lockout relays if they need to swtich too fast (<200ms)
- Send state number
- Eliminate bad states
- Get EZ for each state
- find out function mapped to EZ curve


- switching speed
  - Fixed time
  - Distance and Speed
- Dynamic Speed control
  - Fit equation to curve and adjust accordingly
  - OR, Fixed / manual segments with different speeds
- periodically check that arduino connection is healthy
- Manual Switching control

- Read test cases from json file

- Convert to .exe