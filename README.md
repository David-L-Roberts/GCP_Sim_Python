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
- log serial received messages (non code messages)
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