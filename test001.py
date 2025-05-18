from nicegui import ui
from ClsAutoTestCase import AutoTestCase

# def handle_upload(e):
#     # This function will be called when a file is uploaded
#     # e.file_name contains the name of the uploaded file
#     # e.content contains the file content as bytes
#     print(f"File uploaded: {e.file_name}")
#     # Process your file here

# ui.upload(on_upload=handle_upload, label="Select a file", auto_upload=True)
clsTestCase = AutoTestCase(5)

ui.run(
    host='127.0.0.1',
    port=10_000,
)