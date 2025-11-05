# High-Speed File Server

This is an optimized file server that can utilize your full network bandwidth.

## Quick Start

1. **Install dependencies and run:**
   ```
   start_server.bat
   ```

2. **Or run manually:**
   ```
   pip install -r requirements.txt
   python server_production.py
   ```

## Performance Optimizations

### What was causing slow speeds:
- Small buffer sizes (default Flask uses small chunks)
- No range request support (no resume capability)
- Single-threaded Flask dev server
- No socket optimizations
- No streaming for large files

### Optimizations implemented:
- ✅ **Large buffer sizes** (4MB chunks instead of default 8KB)
- ✅ **HTTP Range requests** (resume support, partial downloads)
- ✅ **Multi-threaded/async serving** (Gunicorn + Gevent workers)
- ✅ **Optimized file streaming** (direct file-to-socket transfer)
- ✅ **Keep-alive connections** (reduces connection overhead)
- ✅ **Proper MIME types** (better client handling)
- ✅ **Socket buffer optimization** (larger OS-level buffers)

## Server Versions

1. **server.py** - Your original with basic optimizations
2. **server_optimized.py** - Enhanced Flask version with range support
3. **server_production.py** - Production-ready with Gunicorn (RECOMMENDED)

## Expected Performance

With these optimizations, you should see:
- **Download speeds**: Close to your 250 Mbps upload capacity
- **Large file support**: Efficient streaming without memory issues
- **Resume capability**: Downloads can be paused and resumed
- **Better concurrent handling**: Multiple downloads simultaneously

## Usage Tips

- Use `server_production.py` for best performance
- Large files (like your 720p movie) will stream efficiently
- Downloads can be resumed if interrupted
- Multiple clients can download simultaneously

## Troubleshooting

If speeds are still slow:
1. Check if your drive read speed is the bottleneck
2. Test with multiple concurrent downloads
3. Check network conditions between client and server
4. Consider using a dedicated file server like nginx for ultimate performance