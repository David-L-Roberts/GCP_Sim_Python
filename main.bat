@echo off
echo Activating virtual environment...
call GcpSimEnv\Scripts\activate.bat

echo Running Python script...
python main.py

echo Exit complete!

