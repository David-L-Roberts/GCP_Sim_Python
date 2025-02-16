class ActionCodes:
    DECREASE_EZ     = "DECREASE_EZ"
    INCREASE_EZ     = "INCREASE_EZ"
    RESET_HIGH_EZ   = "RESET_HIGH_EZ"
    RESET_LOW_EZ    = "RESET_LOW_EZ"
    MANUAL          = "MANUAL"
    IDLE            = "IDLE"
    HMI_ACK         = "HMI_ACK"
    HMI_HELLO       = "HMI_HELLO"
    CHANGE_SWITCH_T = "CHANGE_SWITCH_T"

# types of messages and their control characters
txMessageCodes: dict[str, bytes] = {
    ActionCodes.DECREASE_EZ:        b'100',
    ActionCodes.INCREASE_EZ:        b'101',
    ActionCodes.RESET_HIGH_EZ:      b'102',
    ActionCodes.RESET_LOW_EZ:       b'103',
    ActionCodes.MANUAL:             b'110',
    ActionCodes.IDLE:               b'111',
    ActionCodes.CHANGE_SWITCH_T:    b'200',
    ActionCodes.HMI_ACK:            b'253',
    ActionCodes.HMI_HELLO:          b'254',
}

# types of control characters and their message types
msgTypeLookup: dict[bytes, str] = {
    b'0': "Toggle Relay-09",
    b'1': "Toggle Relay-08",
    b'2': "Toggle Relay-07",
    b'3': "Toggle Relay-06",
    b'4': "Toggle Relay-05",
    b'5': "Toggle Relay-04",
    b'6': "Toggle Relay-03",
    b'7': "Toggle Relay-02",
    b'8': "Toggle Relay-01",
    b'100': "DECREASE_EZ",
    b'101': "INCREASE_EZ",
    b'102': "RESET_HIGH_EZ",
    b'103': "RESET_LOW_EZ",
    b'110': "MANUAL",
    b'111': "IDLE",
    b'200': "CHANGE_SWITCH_T",
    b'253': "HMI_ACK",
    b'254': "HMI_HELLO",
}
