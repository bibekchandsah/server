@echo off
echo ===============================================
echo       COMPLETE CLOUDFLARE TUNNEL SETUP
echo ===============================================
echo.
echo This will set up a fast, stable file sharing solution
echo that bypasses ngrok's 1 Mbps limitation!
echo.
echo Step 1: Starting tunnel-optimized server...
start /B python server_tunnel.py
timeout /t 3 /nobreak >nul

echo Step 2: Starting Cloudflare Tunnel...
echo.
echo ⚠️  IMPORTANT: Keep this window open!
echo    Your tunnel URL will appear below.
echo    Share that URL with others for fast downloads.
echo.
echo Starting tunnel in 5 seconds...
timeout /t 5 /nobreak >nul

"C:\Program Files (x86)\cloudflared\cloudflared.exe" tunnel --url http://localhost:8000

echo.
echo ===============================================
echo Tunnel stopped. Press any key to restart...
echo ===============================================
pause
goto :eof