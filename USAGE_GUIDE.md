# 🚀 FILE_SERVER.PY - USAGE GUIDE

## Quick Start

1. **Install Flask** (if not already installed):
   ```bash
   pip install flask
   ```

2. **Run the server**:
   ```bash
   python file_server.py
   ```

3. **Enter directory path** when prompted:
   ```
   Enter directory path to share: D:\github\repository\all-documentsss\compressed size=2472 x 3684
   ```

4. **Enter port** (or press Enter for 8000):
   ```
   Enter port number (default: 8000): 8000
   ```

5. **Access your files**:
   - Local: http://localhost:8000
   - Network: http://YOUR_IP:8000

## ✨ Pre-configured Features

✅ **Maximum Speed**: 8MB chunks (100x faster than default)
✅ **Resume Downloads**: Can pause/resume downloads
✅ **Multi-User**: Multiple users can download simultaneously
✅ **Professional UI**: Beautiful interface with file details
✅ **HTTP Cache**: 1-hour cache for better performance
✅ **Large Files**: Supports up to 16GB files

## 🌐 Share Over Internet

### Cloudflare Tunnel (Recommended - Fast & Free)
```bash
# Terminal 1: Run your server
python file_server.py

# Terminal 2: Start tunnel
cloudflared tunnel --url http://localhost:8000
```

### Serveo SSH Tunnel (Alternative)
```bash
# Terminal 1: Run your server
python file_server.py

# Terminal 2: Start tunnel
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

## 💡 Example Usage

```bash
python file_server.py
```

**When prompted:**
```
Enter directory path: D:\github\repository\all-documentsss\compressed size=2472 x 3684
Enter port number: 8000
```

**Output:**
```
✅ SERVER STARTED SUCCESSFULLY!

📁 Sharing directory: D:\github\repository\all-documentsss\compressed size=2472 x 3684

🌐 ACCESS URLS:
   Local:      http://127.0.0.1:8000
   Network:    http://10.5.234.63:8000

Press CTRL+C to stop
```

---

**This is a single-file solution - no configuration files needed!**
