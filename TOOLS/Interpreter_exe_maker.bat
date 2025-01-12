@echo off
pip show pyinstaller >nul 2>&1
if errorlevel 1 (
    echo PyInstaller is not installed... Installing now...
    pip install pyinstaller
    if errorlevel 1 (
        echo Couldn't install PyInstaller. Please check your Python installation!
        pause
        exit /b
    )
) else (
    echo PyInstaller is already installed! Yippe :333
)

set /p pythonPath=Enter the full path to the Interpreter.py file: 
set /p icoPath=Enter the full path to the icon for the Interpreter.py file: 

if not exist "%pythonPath%" (
    echo The specified Python file does not exist. Please check the path.
    pause
    exit /b
)

if not exist "%icoPath%" (
    echo The specified icon file does not exist. Please check the path.
    pause
    exit /b
)

echo Running PyInstaller...
powershell pyinstaller --onefile --icon="%icoPath%" "%pythonPath%"

if errorlevel 1 (
    echo The exe was not created. Maybe try to reinstall PyInstaller? (pip install pyinstaller)
    pause
    exit /b
) else (
    echo Your exe was created successfully!
    pause
)
exit /b
