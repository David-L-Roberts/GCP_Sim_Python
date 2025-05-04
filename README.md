# GCP Simulator HMI
HMI application for controlling GCP simulator hardware.

Runs as a locally hosted web app, accessed through a web browser on:
- `http://localhost:10000/`


## Install Requirements
Use Python version = `3.10.4`

Run `install_library_requirements.bat` to create local python virtual environment and automatically install all required libraries.

note: it is easy to install incompatible versions of these libraries, which will cause the application to fail. The `requirements.txt` file specifies the library versions that were proven to work during development.

For reference, specific external core libraries used are as follows (no need to install in addition to running .bat script):
- `pip install nicegui`
- `pip install pywebview`
- `pip install pyserial`


## JSON Test Case Definitions
You may predefine test cases for automated test runs.

Test cases are to be defined in json and placed in the `Test Case Definitions` folder.

Below is the syntax used to define a test case.
See the `Template_Test_Cases.json` for a full set of example test case definitions to get you started.

#### Required Parameters:
- `name`
- `ez_start_point`
- `direction`
- `approach_time_sec`


#### Optional parameters:
- `stop_at_time_sec` 
- `pause_time_sec`
- `multiple_tests`



Example json schema given below:
```json
{
    "test_cases": [
    {
        "name":                 "Approach in 180 sec",
        "ez_start_point":       100,
        "direction":            "approach",
        "approach_time_sec":    180,
        "stop_at_time_sec":     60,
        "pause_time_sec":       5.0,
        "multiple_tests":       [
            "wait 10 seconds",
            "Depart in 90 sec"
        ]
    },
    {
        "name":                 "wait 10 seconds",
        "ez_start_point":       null,
        "direction":            "stationary",
        "approach_time_sec":    10,
    },
    {
        "name":                 "Depart in 90 sec",
        "ez_start_point":       0,
        "direction":            "depart",
        "approach_time_sec":    90,
    },
    {
        "...": "..."
    }
    ]
}
```

### Parameter descriptions:
- `name`: (string) unique name used to identify the test case
- `ez_start_point`: (int) specify initial conditions before starting test case. 
    - Valid values:
      - `100` = reset system to EZ = 100 before beginning the test case.
      - `0`   = reset system to EZ = 0 before beginning the test case.
      - `null` = use the current state of the system as the starting point (dont change the state number).
- `direction`: (string) whether train should be approaching or departing the level crossing.
    - Valid values:
      - `"approach"`    = test case will decrease EZ
      - `"depart"`      = test case will increase EZ
      - `"stationary"`  = test case will not change EZ. Used when you want the test case to just add a delay. Delay time will be the 'approach_time_sec' value
- `approach_time_sec`: (int) total train approach time (or departure time) in seconds (ignoring any duration while train is 'stopped')
- `stop_at_time_sec`: (int) if the train should stop during approach, specify how many seconds into the approach the train should move before stopping (e.g. val = 60 -> train will move at the specified speed for 60 seconds, then stop)
    - must be less than the total apparoch time ('approach_time_sec')
- `pause_time_sec`: (float) if a 'stop_at_time_sec' value is provided, this parameter will specify for how long the train will remain stopped for, before continuing its approach (or departure).
    - If a 'stop_at_time_sec' val is provided, but no pause time val is given, then the train will remain stopped and not continue its approach movement (test case finishes)
- `multiple_tests`: (List[strings]) a list of strings, where each string is the name of another test case. The listed test cases will be automatically executed after the current test case has finished. Test cases will be executed in order, as given in the list (first element executed first, etc.)
    - All test cases in the list will have their own 'multiple_tests' property ignored (no recursive behaviour)


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

## General
**Author**: David Roberts
