@echo off
echo ===============================================
echo    CLOUDFLARE TUNNEL - FAST NGROK ALTERNATIVE
echo ===============================================
echo.
echo Cloudflare Tunnel is 50-100x faster than ngrok free!
echo.
echo Step 1: Download Cloudflare Tunnel
echo.
echo Please download cloudflared from:
echo https://github.com/cloudflare/cloudflared/releases
echo.
echo Download: cloudflared-windows-amd64.exe
echo Rename it to: cloudflared.exe
echo Put it in this folder: D:\server\
echo.
echo Step 2: After download, run this command:
echo cloudflared.exe tunnel --url http://localhost:8000
echo.
echo This will give you a fast public URL!
echo.
echo Alternative quick install (if you have chocolatey):
echo choco install cloudflared
echo.
pause