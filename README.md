# GCP Simulator HMI
 HMI application for controlling GCP simulator hardware.
 Runs as a locally hosted web app, accessed through the browser.

## Requirements
- `pip install nicegui`
- `pip install pywebview`
- `pip install pyserial`

## References
- [NiceGui Docs](https://nicegui.io/documentation)
- [Tailwind Docs](https://v2.tailwindcss.com/docs)
- [Quasar Framework Docs](https://quasar.dev/docs)


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