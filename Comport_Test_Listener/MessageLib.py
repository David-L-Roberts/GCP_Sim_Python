class Directions:
    DOWN    = "down"
    UP      = "up"
    LEFT    = "left"
    RIGHT   = "right"
    STOP    = "stop"


# types of messages and their control characters
txMessageCodes = {
    Directions.UP:      b'\xE1',
    Directions.DOWN:    b'\xE2',
    Directions.LEFT:    b'\xE3',
    Directions.RIGHT:   b'\xE4',
    Directions.STOP:    b'\xE0',
    "Hello":            b'\xD1'
}

# types of control characters and their message types
msgTypeLookup = {
    "E1": "Forward",
    "E2": "Backward",
    "E3": "Turn Left",
    "E4": "Turn Right",
    "E0": "Stop",
    "D1": "Hello",
    "D2": "ACK",
    "FB": "Auto Breaking Enabled Alert",
    "FC": "Auto Breaking Disabled Alert",
    "FA": "Emergency Stop Enabled Alert",
    "FE": "Emergency Stop Disabled Alert",
    "FD": "Distance Sensor Reading",
}
