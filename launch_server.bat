@echo off
REM High-Performance File Server Launcher
REM Double-click to start the server

echo.
echo ================================================================================
echo       HIGH-PERFORMANCE FILE SERVER
echo ================================================================================
echo.

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not found!
    echo Install from: https://www.python.org/
    pause
    exit /b 1
)

REM Check Flask
python -c "import flask" >nul 2>&1
if errorlevel 1 (
    echo Installing Flask...
    pip install flask
    echo.
)

REM Run server
python file_server.py

pause
