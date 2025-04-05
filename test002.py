from nicegui import ui

ui.label("This is a test")
ui.run(
    title="GCP Simulator HMI", 
    host='127.0.0.1',
    port=10_000,
    dark=True,
    show=False,
    reload=False
)

