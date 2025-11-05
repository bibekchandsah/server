@echo off
echo ===============================================
echo    CLOUDFLARE TUNNEL - EASY SETUP
echo ===============================================
echo.
echo Step 1: Starting optimized file server...
@REM start /B python server_fast.py
@REM start /B python server_optimized.py
start /B python server_production.py
timeout /t 2 /nobreak >nul

echo Step 2: Starting Cloudflare Tunnel with HTTP protocol...
echo This should work better than HTTP2 for file downloads.
echo.
echo Your tunnel URL will appear below:
echo.

"C:\Program Files (x86)\cloudflared\cloudflared.exe" tunnel --url http://localhost:8000 --protocol h2mux

pause