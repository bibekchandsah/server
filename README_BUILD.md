# 🚀 High-Performance File Server - Build Instructions

## 📦 Building the Executable

### Quick Build
Simply run:
```bash
python build_exe.py
```

### What the build script does:
1. ✅ Checks if PyInstaller is installed (installs if needed)
2. ✅ Downloads cloudflared.exe automatically (if not present)
3. ✅ Bundles cloudflared.exe with the application
4. ✅ Creates a single executable file
5. ✅ Excludes unnecessary modules for smaller file size

### Output
- **Location:** `dist/HighPerformanceFileServer.exe`
- **Size:** ~30-40 MB (includes Python, Flask, and cloudflared)
- **Portable:** No installation needed, just run the .exe!

## 🎯 What's Included

The compiled executable contains:
- ✅ Python runtime
- ✅ Flask web framework
- ✅ cloudflared.exe (Cloudflare Tunnel)
- ✅ All performance optimizations (8MB chunks, 4MB buffers)
- ✅ Professional responsive UI with purple theme
- ✅ Resume download support
- ✅ Multi-user support

## 🚀 Using the Executable

### For Users (No Python Required!)
1. Download/receive `HighPerformanceFileServer.exe`
2. Double-click to run
3. Enter the directory to share
4. Enter the port number (or use default)
5. Share files via:
   - Local: `http://127.0.0.1:8000`
   - Network: `http://YOUR_IP:8000`
   - Internet: Cloudflare URL (auto-displayed and copied to clipboard)

## 🔧 For Developers

### Manual Build Options
You can also build manually with custom options:

```bash
pyinstaller --onefile --name "HighPerformanceFileServer" --add-data "cloudflared.exe;." --exclude-module PyQt5 --exclude-module PyQt6 --exclude-module tkinter --console file_server.py
```

### Build Files
- `build_exe.py` - Automated build script
- `file_server.py` - Main server code
- `cloudflared.exe` - Downloaded automatically by build script
- `HighPerformanceFileServer.spec` - PyInstaller spec file (auto-generated)

### Clean Build
```bash
# Remove build artifacts
Remove-Item -Recurse -Force build, dist, *.spec
# Then rebuild
python build_exe.py
```

## 📋 Requirements (For Building Only)

- Python 3.8+
- Flask (`pip install flask`)
- PyInstaller (auto-installed by build script)
- Internet connection (to download cloudflared.exe)

## 🌐 Cloudflare Tunnel

The executable automatically:
- ✅ Detects bundled cloudflared.exe
- ✅ Starts tunnel in background (hidden window)
- ✅ Captures and displays the public URL
- ✅ Copies URL to clipboard
- ✅ Maintains maximum speed (4-5 MB/s)

## 🎁 Distribution

The final executable is completely standalone:
- No Python installation needed
- No external dependencies
- No manual cloudflared download
- Works on any Windows 10/11 PC
- Single file - easy to share!

## 💡 Tips

1. **First Build:** Download will take a few seconds for cloudflared.exe (~40 MB)
2. **Subsequent Builds:** Much faster as cloudflared.exe is cached
3. **File Size:** The .exe is ~30-40 MB due to bundled Python runtime and cloudflared
4. **Portable:** Copy the .exe anywhere and it will work
5. **No Installation:** Just double-click and run!

## 🐛 Troubleshooting

### Build fails with "cloudflared download error"
- Check your internet connection
- Download manually from: https://github.com/cloudflare/cloudflared/releases
- Place `cloudflared.exe` in the same folder as `build_exe.py`

### Executable is too large
- This is normal - it includes Python runtime, Flask, and cloudflared
- Cannot be reduced significantly without removing functionality

### Cloudflare tunnel not working
- The executable automatically uses the bundled cloudflared.exe
- No manual setup needed
- Check firewall if tunnel doesn't start

## 📊 Performance

The compiled executable has identical performance to the Python script:
- ✅ 8 MB chunks for maximum throughput
- ✅ 4 MB socket buffers
- ✅ Resume downloads supported
- ✅ Multi-user concurrent access
- ✅ Cloudflare tunnel at full speed (4-5 MB/s)

---

**Author:** Bibek Chand Sah  
**License:** Free to use and distribute  
**Version:** 1.0
