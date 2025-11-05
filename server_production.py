"""
Production-ready file server with maximum performance
Install required packages: pip install gunicorn gevent
Run with: python server_production.py
"""

from flask import Flask, Response, request, render_template_string
import os
import mimetypes
import time
import socket

app = Flask(__name__)
SHARE_DIR = r"D:/server/index"

# Ultra-optimized settings
BUFFER_SIZE = 4 * 1024 * 1024  # 4MB chunks
SOCKET_BUFFER_SIZE = 2 * 1024 * 1024  # 2MB socket buffer

@app.route('/<path:filename>')
def download_file(filename):
    """Ultra-optimized file download"""
    file_path = os.path.join(SHARE_DIR, filename)
    
    if not os.path.exists(file_path) or not os.path.isfile(file_path):
        return "File not found", 404
    
    # Security check
    if not os.path.abspath(file_path).startswith(os.path.abspath(SHARE_DIR)):
        return "Access denied", 403
    
    file_size = os.path.getsize(file_path)
    mimetype = mimetypes.guess_type(filename)[0] or 'application/octet-stream'
    
    # Handle range requests
    range_header = request.headers.get('Range', None)
    if range_header:
        return handle_range_request(file_path, file_size, range_header, mimetype, filename)
    
    # Ultra-fast streaming with optimized file reading
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
            'Cache-Control': 'public, max-age=3600',
            'Connection': 'keep-alive',
            'Last-Modified': time.strftime('%a, %d %b %Y %H:%M:%S GMT', 
                            time.gmtime(os.path.getmtime(file_path)))
        }
    )
    return response

def handle_range_request(file_path, file_size, range_header, mimetype, filename):
    """Optimized range request handling"""
    byte_start = 0
    byte_end = file_size - 1
    
    try:
        if range_header.startswith('bytes='):
            range_spec = range_header[6:]
            ranges = range_spec.split(',')[0]
            
            if '-' in ranges:
                start, end = ranges.split('-', 1)
                if start:
                    byte_start = int(start)
                if end:
                    byte_end = min(int(end), file_size - 1)
    except ValueError:
        return "Invalid range", 400
    
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
        206,
        headers={
            'Content-Range': f'bytes {byte_start}-{byte_end}/{file_size}',
            'Accept-Ranges': 'bytes',
            'Content-Length': str(content_length),
            'Content-Type': mimetype,
            'Content-Disposition': f'attachment; filename="{filename}"',
            'Connection': 'keep-alive'
        }
    )
    return response

@app.route('/')
def list_files():
    """File listing page"""
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
            <title>Production File Server</title>
            <meta charset="utf-8">
            <style>
                body { font-family: system-ui, -apple-system, sans-serif; margin: 0; padding: 20px; background: #f8f9fa; }
                .container { max-width: 1200px; margin: 0 auto; background: white; padding: 30px; border-radius: 8px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }
                h1 { color: #212529; text-align: center; margin-bottom: 30px; }
                .stats { background: #e3f2fd; padding: 15px; border-radius: 6px; margin-bottom: 20px; text-align: center; }
                table { width: 100%; border-collapse: collapse; margin-top: 20px; }
                th, td { padding: 12px; text-align: left; border-bottom: 1px solid #dee2e6; }
                th { background: #495057; color: white; }
                tr:hover { background: #f8f9fa; }
                a { color: #0066cc; text-decoration: none; }
                a:hover { text-decoration: underline; }
                .size { text-align: right; font-family: 'Courier New', monospace; }
                .download-btn { background: #28a745; color: white; padding: 4px 8px; border-radius: 3px; font-size: 11px; }
                .download-btn:hover { background: #218838; text-decoration: none; color: white; }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>⚡ Production File Server</h1>
                <div class="stats">
                    <strong>{{ files_info|length }}</strong> files | 
                    Total: <strong>{{ total_size }}</strong> |
                    Optimized for maximum speed
                </div>
                
                {% if files_info %}
                <table>
                    <tr><th>File Name</th><th class="size">Size</th><th>Modified</th><th>Download</th></tr>
                    {% for file in files_info %}
                    <tr>
                        <td><a href="/{{ file.name }}">{{ file.name }}</a></td>
                        <td class="size">{{ file.size }}</td>
                        <td>{{ file.modified }}</td>
                        <td><a href="/{{ file.name }}" class="download-btn">Download</a></td>
                    </tr>
                    {% endfor %}
                </table>
                {% endif %}
            </div>
        </body>
        </html>
        """
        
        total_size = sum(f['raw_size'] for f in files_info)
        return render_template_string(template, files_info=files_info, total_size=format_file_size(total_size))
        
    except Exception as e:
        return f"Error: {str(e)}", 500

def format_file_size(size_bytes):
    if size_bytes == 0:
        return "0 B"
    import math
    size_names = ["B", "KB", "MB", "GB", "TB"]
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return f"{s} {size_names[i]}"

def run_with_gunicorn():
    """Run with Gunicorn for maximum performance"""
    try:
        import gunicorn.app.base
        
        class StandaloneApplication(gunicorn.app.base.BaseApplication):
            def __init__(self, app, options=None):
                self.options = options or {}
                self.application = app
                super().__init__()
            
            def load_config(self):
                for key, value in self.options.items():
                    self.cfg.set(key.lower(), value)
            
            def load(self):
                return self.application
        
        options = {
            'bind': '0.0.0.0:8000',
            'workers': 4,  # Adjust based on CPU cores
            'worker_class': 'gevent',  # Async workers for better I/O
            'worker_connections': 1000,
            'keepalive': 2,
            'max_requests': 1000,
            'timeout': 120,
            'preload_app': True
        }
        
        print("🚀 Starting production server with Gunicorn...")
        print(f"📁 Serving: {SHARE_DIR}")
        print(f"🌐 URL: http://localhost:8000")
        print("⚡ Performance: Gunicorn + Gevent workers")
        
        StandaloneApplication(app, options).run()
        
    except ImportError:
        print("❌ Gunicorn not installed. Install with: pip install gunicorn gevent")
        print("🔄 Falling back to Flask development server...")
        return False
    return True

if __name__ == "__main__":
    # Try to run with Gunicorn first for best performance
    if not run_with_gunicorn():
        # Fallback to Flask dev server with optimizations
        print("🔧 Using Flask development server with optimizations...")
        app.run(
            host='0.0.0.0',
            port=8000,
            threaded=True,
            debug=False
        )