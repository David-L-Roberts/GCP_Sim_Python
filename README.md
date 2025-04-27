# GCP Simulator HMI
HMI application for controlling GCP simulator hardware.

Runs as a locally hosted web app, accessed through a web browser on:
- `http://localhost:10000/`


## Install Requirements
Use Python version = `3.10.4`

Run `install_library_requirements.bat` to create local python virtual environment and automatically install all library dependencies.

note: it is easy to install incompatible versions of these libraries, which will cause the application to fail. The `requirements.txt` file specifies the library versions that were proven to work during development.

For reference, specific external core libraries used are as follows (no need to install in addition to running .bat script):
- `pip install nicegui`
- `pip install pywebview`
- `pip install pyserial`


## JSON Test Case Definitions
Test cases to be defined in json and placed in the `Test Case Definitions` folder.

Required Parameters:
- `name`

One of the following parameter sets:
1.  `time_sec`
2.  or, `distance_meter` AND `speed_kph`

Optional parameters:
- `stop_time_sec` and `pause_time_sec`



Example json schema given below:
```json
{
  "test_cases": [
    {
      "name":           "Test Case name here",
      "time_sec":       120.0,
      "distance_meter": 500.0,
      "speed_kph":      4.2,
      "stop_time_sec":  true,
      "pause_time_sec": 10.0
    },
    {
      "name":           "Approach in 180 sec",
      "time_sec":       180,
      "distance_meter": 300.0,
      "speed_kph":      3.3,
      "stop_time_sec":  false,
      "pause_time_sec": 0.0
    },
    {
      "...": "..."
    }
  ]
}
```

## References
- [Python Releases](https://www.python.org/downloads/windows/)
- [NiceGui Docs](https://nicegui.io/documentation)
- [Tailwind Docs](https://v2.tailwindcss.com/docs)
- [Quasar Framework Docs](https://quasar.dev/docs)


## Known Issues
- Serial Debug message: when recieving data on serial port, does not count the number of bytes recieved properly (All data is read properly. It simply displays the wrong byte count).

## DEV: To Do
- periodically check that arduino connection is healthy
- Manual Switching control

- Read test cases from json file

- Convert to .exe