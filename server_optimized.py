from flask import Flask, Response, request, render_template_string
import os
import mimetypes
from werkzeug.serving import WSGIRequestHandler
import threading
import time

app = Flask(__name__)
SHARE_DIR = r"D:/server/index"

# Optimized settings
BUFFER_SIZE = 2 * 1024 * 1024  # 2MB chunks for better performance
MAX_CONTENT_LENGTH = 16 * 1024 * 1024 * 1024  # 16GB max file size

class OptimizedRequestHandler(WSGIRequestHandler):
    """Custom request handler with optimized settings"""
    def setup(self):
        super().setup()
        # Increase socket buffer sizes
        try:
            self.connection.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 1024 * 1024)
            self.connection.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 1024 * 1024)
        except:
            pass

@app.route('/<path:filename>')
def download_file(filename):
    """Optimized file download with range support and streaming"""
    file_path = os.path.join(SHARE_DIR, filename)
    
    if not os.path.exists(file_path) or not os.path.isfile(file_path):
        return "File not found", 404
    
    # Security check - prevent directory traversal
    if not os.path.abspath(file_path).startswith(os.path.abspath(SHARE_DIR)):
        return "Access denied", 403
    
    file_size = os.path.getsize(file_path)
    mimetype = mimetypes.guess_type(filename)[0] or 'application/octet-stream'
    
    # Handle range requests (crucial for large files and resume support)
    range_header = request.headers.get('Range', None)
    if range_header:
        return handle_range_request(file_path, file_size, range_header, mimetype, filename)
    
    # Full file download with optimized streaming
    def generate_file():
        try:
            with open(file_path, 'rb', buffering=BUFFER_SIZE) as f:
                while True:
                    chunk = f.read(BUFFER_SIZE)
                    if not chunk:
                        break
                    yield chunk
        except Exception as e:
            print(f"Error reading file: {e}")
            return
    
    response = Response(
        generate_file(),
        headers={
            'Content-Length': str(file_size),
            'Content-Type': mimetype,
            'Accept-Ranges': 'bytes',
            'Content-Disposition': f'attachment; filename="{filename}"',
            'Cache-Control': 'public, max-age=3600',  # Cache for 1 hour
            'Last-Modified': time.strftime('%a, %d %b %Y %H:%M:%S GMT', 
                            time.gmtime(os.path.getmtime(file_path)))
        }
    )
    return response

def handle_range_request(file_path, file_size, range_header, mimetype, filename):
    """Handle HTTP range requests for partial content"""
    byte_start = 0
    byte_end = file_size - 1
    
    try:
        # Parse range header (format: bytes=start-end)
        if range_header.startswith('bytes='):
            range_spec = range_header[6:]
            ranges = range_spec.split(',')[0]  # Handle only first range
            
            if '-' in ranges:
                start, end = ranges.split('-', 1)
                if start:
                    byte_start = int(start)
                if end:
                    byte_end = min(int(end), file_size - 1)
    except ValueError:
        return "Invalid range", 400
    
    # Validate range
    if byte_start < 0 or byte_start >= file_size or byte_end < byte_start:
        return "Range not satisfiable", 416
    
    content_length = byte_end - byte_start + 1
    
    def generate_partial():
        try:
            with open(file_path, 'rb', buffering=BUFFER_SIZE) as f:
                f.seek(byte_start)
                remaining = content_length
                
                while remaining > 0:
                    chunk_size = min(BUFFER_SIZE, remaining)
                    chunk = f.read(chunk_size)
                    if not chunk:
                        break
                    remaining -= len(chunk)
                    yield chunk
        except Exception as e:
            print(f"Error reading partial file: {e}")
            return
    
    response = Response(
        generate_partial(),
        206,  # Partial Content
        headers={
            'Content-Range': f'bytes {byte_start}-{byte_end}/{file_size}',
            'Accept-Ranges': 'bytes',
            'Content-Length': str(content_length),
            'Content-Type': mimetype,
            'Content-Disposition': f'attachment; filename="{filename}"'
        }
    )
    return response

@app.route('/')
def list_files():
    """Enhanced file listing with size and download info"""
    try:
        files_info = []
        for filename in sorted(os.listdir(SHARE_DIR)):
            file_path = os.path.join(SHARE_DIR, filename)
            if os.path.isfile(file_path):
                size = os.path.getsize(file_path)
                size_str = format_file_size(size)
                modified = time.strftime('%Y-%m-%d %H:%M', 
                                       time.localtime(os.path.getmtime(file_path)))
                files_info.append({
                    'name': filename,
                    'size': size_str,
                    'modified': modified,
                    'raw_size': size
                })
        
        template = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>High-Speed File Server</title>
            <meta charset="utf-8">
            <style>
                body { 
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
                    margin: 0; 
                    padding: 20px; 
                    background: #f5f5f5; 
                }
                .container { 
                    max-width: 1200px; 
                    margin: 0 auto; 
                    background: white; 
                    padding: 30px; 
                    border-radius: 10px; 
                    box-shadow: 0 2px 10px rgba(0,0,0,0.1); 
                }
                h1 { 
                    color: #333; 
                    text-align: center; 
                    margin-bottom: 30px; 
                }
                .stats {
                    background: #e8f4f8;
                    padding: 15px;
                    border-radius: 5px;
                    margin-bottom: 20px;
                    text-align: center;
                }
                table { 
                    width: 100%; 
                    border-collapse: collapse; 
                    margin-top: 20px; 
                }
                th, td { 
                    padding: 12px; 
                    text-align: left; 
                    border-bottom: 1px solid #ddd; 
                }
                th { 
                    background: #007acc; 
                    color: white; 
                    font-weight: bold; 
                }
                tr:hover { 
                    background: #f8f9fa; 
                }
                a { 
                    color: #007acc; 
                    text-decoration: none; 
                    font-weight: 500; 
                }
                a:hover { 
                    text-decoration: underline; 
                    color: #005a9e; 
                }
                .size { 
                    text-align: right; 
                    font-family: monospace; 
                }
                .download-btn {
                    background: #28a745;
                    color: white;
                    padding: 6px 12px;
                    border-radius: 4px;
                    text-decoration: none;
                    font-size: 12px;
                }
                .download-btn:hover {
                    background: #218838;
                    text-decoration: none;
                    color: white;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>🚀 High-Speed File Server</h1>
                <div class="stats">
                    <strong>{{ files_info|length }}</strong> files available | 
                    Total size: <strong>{{ total_size }}</strong> |
                    Optimized for high-speed downloads with resume support
                </div>
                
                {% if files_info %}
                <table>
                    <thead>
                        <tr>
                            <th>📁 File Name</th>
                            <th class="size">📊 Size</th>
                            <th>🕒 Modified</th>
                            <th>⬇️ Download</th>
                        </tr>
                    </thead>
                    <tbody>
                        {% for file in files_info %}
                        <tr>
                            <td>
                                <a href="/{{ file.name }}" title="Click to download">
                                    {{ file.name }}
                                </a>
                            </td>
                            <td class="size">{{ file.size }}</td>
                            <td>{{ file.modified }}</td>
                            <td>
                                <a href="/{{ file.name }}" class="download-btn">
                                    Download
                                </a>
                            </td>
                        </tr>
                        {% endfor %}
                    </tbody>
                </table>
                {% else %}
                <p style="text-align: center; color: #666; margin: 40px 0;">
                    No files found in the directory.
                </p>
                {% endif %}
                
                <div style="margin-top: 30px; padding-top: 20px; border-top: 1px solid #ddd; color: #666; font-size: 12px;">
                    <strong>Performance Features:</strong>
                    • Resume support (HTTP Range requests) • Large file streaming • Optimized buffer sizes • Multi-threaded serving
                </div>
            </div>
        </body>
        </html>
        """
        
        total_size = sum(f['raw_size'] for f in files_info)
        total_size_str = format_file_size(total_size)
        
        return render_template_string(template, 
                                    files_info=files_info, 
                                    total_size=total_size_str)
        
    except Exception as e:
        return f"Error listing files: {str(e)}", 500

def format_file_size(size_bytes):
    """Format file size in human readable format"""
    if size_bytes == 0:
        return "0 B"
    
    size_names = ["B", "KB", "MB", "GB", "TB", "PB"]
    import math
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return f"{s} {size_names[i]}"

if __name__ == "__main__":
    print("🚀 Starting High-Speed File Server...")
    print(f"📁 Serving files from: {SHARE_DIR}")
    print(f"🌐 Server URL: http://localhost:8000")
    print(f"🔧 Buffer size: {format_file_size(BUFFER_SIZE)}")
    print("✅ Features: Range requests, streaming, resume support, optimized buffers")
    
    # Use optimized settings
    app.run(
        host='0.0.0.0', 
        port=8000, 
        threaded=True,  # Enable multi-threading
        debug=False,    # Disable debug mode for better performance
        request_handler=OptimizedRequestHandler
    )