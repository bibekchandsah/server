# 🚀 High-Performance File Server

**Single-file Python solution for fast, professional file sharing**

---

## 📥 Download & Install

### Option 1: Download Executable (No Python Required!)
**Just download and run - everything is included!**

**[📦 Download HighPerformanceFileServer.exe](https://github.com/bibekchandsah/server/releases)**

✅ No Python installation needed  
✅ No dependencies to install  
✅ Cloudflare Tunnel built-in  
✅ Just double-click and run!

### Option 2: Run Python Script

## 📋 What You Need

1. **Python** (3.6 or higher)
2. **Flask** - Install with: `pip install flask`
3. **One file**: `file_server.py`

That's it! No configuration files, no complex setup.

---

## 🎯 Quick Start (3 Steps)

### from requirements file
```bash
pip install -r requirements.txt
```

or
-----

### Step 1: Install Flask
```bash
pip install flask
```

### Step 2: Run the Server
```bash
python file_server.py
```

### Step 3: Enter Your Details

**When prompted, enter:**

1. **Enter directory path** when prompted:
   ```
   Example: D:\sharefiles
   ```

2. **Enter port** (or press Enter for 8000):
   ```
   Enter port number (default: 8000): 8000
   ```

3. **Access your files**:
   - Local: http://localhost:8000
   - Network: http://YOUR_IP:8000

**Done!** Server will show you the URLs to access your files.

---

## ✨ Pre-configured Features (No Setup Needed)

✅ **Maximum Speed** - 8MB chunks (100x faster than default)  
✅ **Resume Downloads** - Pause and resume anytime  
✅ **Multi-User Support** - Multiple downloads simultaneously  
✅ **Professional UI** - Beautiful interface with file details  
✅ **Large Files** - Supports up to 16GB  
✅ **HTTP Caching** - 1-hour cache for performance  
✅ **Secure** - Read-only, path traversal protection  

---

## 🌐 Sharing Options

### 🏠 Local Network (Same WiFi)
Use the **Network URL** shown by the server:
```
http://10.5.234.63:8000
```

### 🌍 Internet (Outside Your Network)

**Option 1: Cloudflare Tunnel** (Recommended - Fast & Free)
```bash
# Terminal 1
python file_server.py

✅ Cloudflare Tunnel active: https://polished-adjusted-trade-monroe.trycloudflare.com
📋 URL copied to clipboard!
```

**Option 2: Serveo SSH Tunnel** (Alternative - Easy)
```bash
# Terminal 1
python file_server.py

# Terminal 2
ssh -R 80:localhost:8000 serveo.net
```

## 📊 Configuration Details

| Feature | Value | Description |
|---------|-------|-------------|
| Chunk Size | 8 MB | Maximum speed transfers |
| Socket Buffer | 4 MB | Optimized networking |
| Max File Size | 16 GB | Large file support |
| Threading | Enabled | Multi-user concurrent access |
| Resume | Enabled | Download pause/resume |
| Cache | 1 hour | HTTP caching |

---

## 📊 Performance

| Environment | Speed |
|-------------|-------|
| Same Computer | 1000+ Mbps |
| Local Network | 200-1000 Mbps |
| Cloudflare Tunnel | 50-100 Mbps |
| Serveo Tunnel | 30-80 Mbps |
| Ngrok Free | ~1 Mbps |

---

## 💡 Example Run

```bash
python file_server.py
```

```
================================================================================
🚀 HIGH-PERFORMANCE FILE SERVER                          𝓓𝓮𝓿𝓮𝓵𝓸𝓹𝓮𝓭 𝓫𝔂 𝓑𝓲𝓫𝓮𝓴.....
================================================================================

📁 DIRECTORY CONFIGURATION:
Enter directory path to share (or press Enter for 'D:\server\index'):
✅ Selected directory: D:\server\index
✅ Found 16 files in directory

🌐 PORT CONFIGURATION:
Enter port number (default: 8000):
✅ Selected port: 8000

--------------------------------------------------------------------------------

================================================================================
📋 SERVER CONFIGURATION:
--------------------------------------------------------------------------------
📦 Chunk Size:           8 MB
🔧 Socket Buffer:        4 MB
📊 Max File Size:        16 GB
⚡ Speed Mode:           MAXIMUM
♻️  Resume Downloads:    ✅ Enabled
👥 Multi-User Support:   ✅ Enabled (Threading)
💾 HTTP Caching:         ✅ Enabled (1h)
================================================================================

✅ SERVER STARTED SUCCESSFULLY!

💡 SHARING TIPS:
   • Use Local URLs on this computer
   • Use Network URL on your local network (LAN)
   • For internet sharing, we will use Cloudflare Tunnel

🛑 Press CTRL+C to stop the server
--------------------------------------------------------------------------------

🌐 Starting Cloudflare Tunnel...
🚀 Starting high-performance file server...

 * Serving Flask app 'file_server'
 * Debug mode: off
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:8000
 * Running on http://10.5.234.63:8000
Press CTRL+C to quit

📡 ACCESS YOUR FILES:
   • http://127.0.0.1:8000 (for this pc)
   • http://10.5.234.63:8000 (for same wifi pc)
   • https://polished-adjusted-trade-monroe.trycloudflare.com (for global share)


✅ Cloudflare Tunnel active: https://polished-adjusted-trade-monroe.trycloudflare.com
📋 URL copied to clipboard!
```

---

## 🎨 Professional Web Interface

When you open the URL in a browser, you'll see:

- **Beautiful gradient design** with modern UI
- **File listing** with names, sizes, and dates
- **Download buttons** for each file
- **Live configuration** showing server settings
- **Statistics** - total files, size, etc.
- **Responsive design** - works on mobile too

---

## 🛑 Stop Server

Press `CTRL + C` in the terminal where the server is running.

---

## 🔧 Troubleshooting

**"Port already in use"**
→ Choose a different port when prompted (e.g., 8080, 9000)

**"Directory not found"**
→ Check the path is correct and exists

**"Flask not installed"**
→ Run: `pip install flask`

**"Python not found"**
→ Install Python from: https://www.python.org/

---

## 📝 Technical Details

| Setting | Value | Purpose |
|---------|-------|---------|
| Chunk Size | 8 MB | Maximum throughput |
| Socket Buffer | 4 MB | Network optimization |
| Max File Size | 16 GB | Large file support |
| Threading | Enabled | Concurrent users |
| Range Requests | Enabled | Resume capability |
| Cache Control | 1 hour | Performance boost |
| UI Mode | Professional | Full featured |

---

## 🤝 Share This File

You can share `file_server.py` with anyone. It's completely self-contained:

- ✅ No external configuration files
- ✅ No database setup
- ✅ No complex dependencies
- ✅ Just Python + Flask

## Server Versions
1. **server_fast.py** - Enhanced for fast sharing
2. **server_optimized.py** - Enhanced Flask version with range support
3. **server_production.py** - Production-ready with Gunicorn 
4. **file_server.py** - user control with all features of above 3 files (RECOMMENDED)

---

## 👤 Author

**Bibek Chand Sah**

Repository: https://github.com/bibekchandsah/server

---

## 📄 License

Free to use, modify, and share.

---

**Remember**: This is a single-file solution. Just run it and share files instantly!
