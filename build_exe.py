"""
Build script to compile file_server.py to executable with bundled cloudflared.exe
This script will:
1. Download cloudflared.exe if not present
2. Bundle it with the application
3. Create a single executable file
"""

import os
import sys
import urllib.request
import zipfile
import subprocess

def download_cloudflared():
    """Download cloudflared.exe if not present"""
    cloudflared_path = os.path.join(os.getcwd(), "cloudflared.exe")
    
    if os.path.exists(cloudflared_path):
        print("✅ cloudflared.exe already exists")
        return cloudflared_path
    
    print("📥 Downloading cloudflared.exe...")
    
    # Cloudflare download URL for Windows
    url = "https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-windows-amd64.exe"
    
    try:
        # Download with progress
        print(f"   Downloading from: {url}")
        urllib.request.urlretrieve(url, cloudflared_path)
        print(f"✅ Downloaded cloudflared.exe ({os.path.getsize(cloudflared_path) / (1024*1024):.1f} MB)")
        return cloudflared_path
    except Exception as e:
        print(f"❌ Failed to download cloudflared.exe: {e}")
        print("Please download manually from:")
        print("https://github.com/cloudflare/cloudflared/releases")
        return None

def install_pyinstaller():
    """Install PyInstaller if not present"""
    try:
        import PyInstaller
        print("✅ PyInstaller is already installed")
        return True
    except ImportError:
        print("📦 Installing PyInstaller...")
        try:
            subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"], 
                         check=True)
            print("✅ PyInstaller installed successfully")
            return True
        except Exception as e:
            print(f"❌ Failed to install PyInstaller: {e}")
            return False

def build_executable():
    """Build the executable with bundled cloudflared"""
    
    print("=" * 80)
    print("🚀 HIGH-PERFORMANCE FILE SERVER - BUILD SCRIPT")
    print("=" * 80)
    print()
    
    # Step 1: Install PyInstaller
    if not install_pyinstaller():
        return False
    
    # Step 2: Download cloudflared.exe
    cloudflared_path = download_cloudflared()
    if not cloudflared_path:
        return False
    
    print()
    print("🔨 Building executable...")
    print("-" * 80)
    
    # Check if icon.ico exists
    icon_path = os.path.join(os.getcwd(), "icon.ico")
    if not os.path.exists(icon_path):
        print(f"⚠️  Warning: icon.ico not found at {icon_path}")
        print("   Building without custom icon...")
        icon_param = []
    else:
        print(f"✅ Found icon: {icon_path}")
        icon_param = ["--icon", icon_path]
    
    # Step 3: Build with PyInstaller
    # Bundle cloudflared.exe as a data file
    build_command = [
        "pyinstaller",
        "--onefile",                                    # Single file
        "--name", "HighPerformanceFileServer",          # Output name
        "--clean",                                      # Clean build
        *icon_param,                                    # Add icon if available
        "--add-data", f"{cloudflared_path};.",         # Bundle cloudflared.exe
        "--exclude-module", "PyQt5",                    # Exclude unnecessary modules
        "--exclude-module", "PyQt6",
        "--exclude-module", "tkinter",
        "--exclude-module", "matplotlib",
        "--exclude-module", "numpy",
        "--exclude-module", "IPython",
        "--exclude-module", "kivy",
        "--exclude-module", "kivymd",
        "--exclude-module", "pygame",
        "--console",                                     # Show console
        "file_server.py"
    ]
    
    try:
        result = subprocess.run(build_command, check=True)
        print()
        print("=" * 80)
        print("✅ BUILD SUCCESSFUL!")
        print("=" * 80)
        print()
        print("📦 Your executable is ready:")
        print(f"   Location: {os.path.join(os.getcwd(), 'dist', 'HighPerformanceFileServer.exe')}")
        print()
        print("📝 What's included:")
        print("   ✅ Python runtime")
        print("   ✅ Flask framework")
        print("   ✅ cloudflared.exe (bundled)")
        print("   ✅ All optimizations (8MB chunks, 4MB buffers)")
        print()
        print("🚀 You can now:")
        print("   1. Run HighPerformanceFileServer.exe")
        print("   2. Share the .exe file with anyone (no Python needed)")
        print("   3. Cloudflare Tunnel works automatically!")
        print()
        print("💡 The .exe file is portable and includes everything!")
        print("=" * 80)
        return True
        
    except subprocess.CalledProcessError as e:
        print()
        print("❌ BUILD FAILED")
        print(f"Error: {e}")
        return False
    except Exception as e:
        print()
        print("❌ UNEXPECTED ERROR")
        print(f"Error: {e}")
        return False

if __name__ == "__main__":
    success = build_executable()
    sys.exit(0 if success else 1)
