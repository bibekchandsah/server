@echo off
echo Installing required packages for high-speed file server...
pip install -r requirements.txt

echo.
echo Starting production file server...
echo Server will be available at: http://localhost:8000
echo Press Ctrl+C to stop the server
echo.

python server_production.py