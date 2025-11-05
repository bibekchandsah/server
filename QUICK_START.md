# 📝 QUICK REFERENCE CARD

## 🚀 Start Server

**Windows:**
- Double-click: `launch_server.bat`
- Or: `python file_server.py`

**Linux/Mac:**
```bash
python3 file_server.py
```

## 📋 What You'll Be Asked

1. **Directory Path**:
   ```
   Example: D:\github\repository\all-documentsss\compressed size=2472 x 3684
   Or press Enter for: D:\server\index
   ```

2. **Port Number**:
   ```
   Press Enter for: 8000
   Or enter custom: 9000
   ```

## 🌐 Access URLs

After starting, you'll get:

```
Local:      http://127.0.0.1:8000
Network:    http://YOUR_IP:8000
```

## ⚡ Performance Features

| Feature | Status | Value |
|---------|--------|-------|
| Speed Mode | ✅ | Maximum (8MB chunks) |
| Resume Downloads | ✅ | Enabled |
| Multi-User | ✅ | Enabled |
| Max File Size | ✅ | 16 GB |
| HTTP Cache | ✅ | 1 hour |

## 🌍 Share Over Internet

**Cloudflare Tunnel (Fastest):**
```bash
cloudflared tunnel --url http://localhost:8000
```

**Serveo (Easy):**
```bash
ssh -R 80:localhost:8000 serveo.net
```

## 🛑 Stop Server

Press `CTRL + C` in the terminal

## 📦 Requirements

```bash
pip install flask
```

That's it! Single file, no configuration needed.

---

**File**: `file_server.py`
**Author**: Bibek Chand Sah
**Purpose**: High-performance file sharing with professional UI
