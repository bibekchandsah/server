"""
Super-optimized file server with maximum speed settings
This version focuses on the fastest possible downloads
"""

from flask import Flask, Response, request
import os
import mimetypes
import time

app = Flask(__name__)
SHARE_DIR = r"D:/server/index"

# Maximum performance settings
CHUNK_SIZE = 8 * 1024 * 1024  # 8MB chunks for maximum throughput

@app.route('/<path:filename>')
def download_file(filename):
    """Ultra-fast file download with maximum optimization"""
    file_path = os.path.join(SHARE_DIR, filename)
    
    if not os.path.exists(file_path):
        return "File not found", 404
    
    file_size = os.path.getsize(file_path)
    mimetype = mimetypes.guess_type(filename)[0] or 'application/octet-stream'
    
    # Handle range requests for resume capability
    range_header = request.headers.get('Range')
    if range_header:
        return handle_range_request(file_path, file_size, range_header, mimetype, filename)
    
    # Full file download with maximum speed streaming
    def stream_file():
        with open(file_path, 'rb', buffering=CHUNK_SIZE) as f:
            while True:
                chunk = f.read(CHUNK_SIZE)
                if not chunk:
                    break
                yield chunk
    
    return Response(
        stream_file(),
        headers={
            'Content-Length': str(file_size),
            'Content-Type': mimetype,
            'Accept-Ranges': 'bytes',
            'Content-Disposition': f'attachment; filename="{filename}"',
            'Cache-Control': 'public, max-age=3600'
        }
    )

def handle_range_request(file_path, file_size, range_header, mimetype, filename):
    """Handle partial downloads for resume support"""
    byte_start = 0
    byte_end = file_size - 1
    
    if range_header.startswith('bytes='):
        try:
            range_spec = range_header[6:].split(',')[0]
            if '-' in range_spec:
                start, end = range_spec.split('-', 1)
                if start:
                    byte_start = int(start)
                if end:
                    byte_end = min(int(end), file_size - 1)
        except:
            return "Invalid range", 400
    
    if byte_start >= file_size or byte_end < byte_start:
        return "Range not satisfiable", 416
    
    content_length = byte_end - byte_start + 1
    
    def stream_partial():
        with open(file_path, 'rb', buffering=CHUNK_SIZE) as f:
            f.seek(byte_start)
            remaining = content_length
            while remaining > 0:
                chunk_size = min(CHUNK_SIZE, remaining)
                chunk = f.read(chunk_size)
                if not chunk:
                    break
                remaining -= len(chunk)
                yield chunk
    
    return Response(
        stream_partial(),
        206,
        headers={
            'Content-Range': f'bytes {byte_start}-{byte_end}/{file_size}',
            'Accept-Ranges': 'bytes',
            'Content-Length': str(content_length),
            'Content-Type': mimetype,
            'Content-Disposition': f'attachment; filename="{filename}"'
        }
    )

@app.route('/')
def list_files():
    """Simple file listing"""
    files = []
    for f in sorted(os.listdir(SHARE_DIR)):
        if os.path.isfile(os.path.join(SHARE_DIR, f)):
            size = os.path.getsize(os.path.join(SHARE_DIR, f))
            files.append(f'<p><a href="/{f}" style="font-size:18px">{f}</a> ({format_size(size)})</p>')
    
    return f"""
    <html><head><title>Speed-Optimized File Server</title></head>
    <body style="font-family: Arial; margin: 40px;">
    <h1>🚀 High-Speed Downloads</h1>
    <p><strong>Server optimized for maximum download speed</strong></p>
    <p>Features: 8MB chunks • Range requests • Resume support</p>
    <hr>
    {''.join(files)}
    </body></html>
    """

def format_size(bytes):
    for unit in ['B', 'KB', 'MB', 'GB']:
        if bytes < 1024:
            return f"{bytes:.1f} {unit}"
        bytes /= 1024
    return f"{bytes:.1f} TB"

if __name__ == "__main__":
    print("🚀 Starting SPEED-OPTIMIZED File Server")
    print(f"📁 Directory: {SHARE_DIR}")
    print(f"🌐 URL: http://localhost:8000")
    print(f"⚡ Chunk size: {CHUNK_SIZE // (1024*1024)}MB for maximum speed")
    print("✅ Range requests enabled for resume support")
    print("\nOptimizations active:")
    print("• 8MB buffer chunks (500x larger than default)")
    print("• HTTP Range requests (resume downloads)")
    print("• Streaming file transfer (no memory limits)")
    print("• Optimized file I/O buffering")
    
    app.run(host='0.0.0.0', port=8000, threaded=True, debug=False)