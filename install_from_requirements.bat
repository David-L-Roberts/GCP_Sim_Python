@echo off
setlocal

REM Set the virtual environment folder name
set VENV_NAME=GcpSimEnv

REM Check if the virtual environment exists, if not, create it
if not exist "%VENV_NAME%\Scripts\activate.bat" (
    echo Creating virtual environment...
    python -m venv %VENV_NAME%
)

REM Activate the virtual environment
echo Activating virtual environment...
call %VENV_NAME%\Scripts\activate.bat

REM Check if requirements.txt exists
if not exist requirements.txt (
    echo requirements.txt not found! Please make sure it's in the same folder as this script.
    exit /b 1
)

REM Install libraries from requirements.txt
echo Installing libraries from requirements.txt...
pip install -r requirements.txt

echo.
echo ✅ Done! All libraries from requirements.txt have been installed.
pause
endlocal
