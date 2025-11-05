"""
🚀 UNIFIED HIGH-PERFORMANCE FILE SERVER - CONFIG FILE VERSION
Reads settings from server_config.ini for easy customization
"""

import os
import sys
import time
import socket
import mimetypes
import threading
import configparser
from flask import Flask, Response, request, render_template_string
from werkzeug.serving import WSGIRequestHandler

# Load configuration from file
def load_config():
    config = configparser.ConfigParser()
    config_file = os.path.join(os.path.dirname(__file__), 'server_config.ini')
    
    if os.path.exists(config_file):
        try:
            config.read(config_file, encoding='utf-8')
            print(f"📄 Loaded configuration from: {config_file}")
        except UnicodeDecodeError:
            # Try with different encoding if UTF-8 fails
            try:
                config.read(config_file, encoding='utf-8-sig')
                print(f"📄 Loaded configuration from: {config_file} (UTF-8 with BOM)")
            except Exception as e:
                print(f"⚠️ Could not read config file: {e}")
                print("🔧 Using default settings...")
        except Exception as e:
            print(f"⚠️ Error reading config file: {e}")
            print("🔧 Using default settings...")
    else:
        print(f"⚠️ Config file not found: {config_file}")
        print("🔧 Using default settings...")
    
    return config

def get_config_value(config, section, key, default_value, value_type=str):
    """Get configuration value with type conversion and defaults"""
    try:
        if value_type == bool:
            return config.getboolean(section, key)
        elif value_type == int:
            return config.getint(section, key)
        elif value_type == float:
            return config.getfloat(section, key)
        else:
            return config.get(section, key)
    except:
        return default_value

# Load configuration
config = load_config()

class ServerConfig:
    """Configuration loaded from server_config.ini"""
    
    # Basic settings
    SHARE_DIR = get_config_value(config, 'BASIC_SETTINGS', 'SHARE_DIR', r"D:/server/index")
    PORT = get_config_value(config, 'BASIC_SETTINGS', 'PORT', 8000, int)
    HOST = get_config_value(config, 'BASIC_SETTINGS', 'HOST', '0.0.0.0')
    
    # Speed preset
    SPEED_PRESET = get_config_value(config, 'SPEED_PRESETS', 'PRESET', 'balanced')
    
    # Manual performance settings
    chunk_mb = get_config_value(config, 'PERFORMANCE_MANUAL', 'CHUNK_SIZE_MB', 4, int)
    socket_mb = get_config_value(config, 'PERFORMANCE_MANUAL', 'SOCKET_BUFFER_MB', 2, int)
    max_gb = get_config_value(config, 'PERFORMANCE_MANUAL', 'MAX_FILE_SIZE_GB', 16, int)
    
    CHUNK_SIZE = chunk_mb * 1024 * 1024
    SOCKET_BUFFER_SIZE = socket_mb * 1024 * 1024
    MAX_CONTENT_LENGTH = max_gb * 1024 * 1024 * 1024
    
    # Server mode
    USE_PRODUCTION_SERVER = get_config_value(config, 'SERVER_MODE', 'USE_PRODUCTION', False, bool)
    WORKER_COUNT = get_config_value(config, 'SERVER_MODE', 'WORKER_COUNT', 4, int)
    WORKER_CONNECTIONS = get_config_value(config, 'SERVER_MODE', 'WORKER_CONNECTIONS', 1000, int)
    THREADED = get_config_value(config, 'SERVER_MODE', 'ENABLE_THREADING', True, bool)
    
    # Features
    ENABLE_RANGE_REQUESTS = get_config_value(config, 'FEATURES', 'ENABLE_RESUME', True, bool)
    ENABLE_CACHE = get_config_value(config, 'FEATURES', 'ENABLE_CACHE', True, bool)
    cache_hours = get_config_value(config, 'FEATURES', 'CACHE_HOURS', 1, int)
    CACHE_MAX_AGE = cache_hours * 3600
    
    UI_STYLE = get_config_value(config, 'FEATURES', 'UI_STYLE', 'professional')
    SHOW_FILE_DETAILS = get_config_value(config, 'FEATURES', 'SHOW_FILE_DETAILS', True, bool)
    
    # Advanced
    DEBUG_MODE = get_config_value(config, 'ADVANCED', 'DEBUG_MODE', False, bool)
    CONNECTION_TIMEOUT = get_config_value(config, 'ADVANCED', 'CONNECTION_TIMEOUT', 120, int)

# Apply speed presets (override manual settings if preset is not 'custom')
if ServerConfig.SPEED_PRESET != 'custom':
    if ServerConfig.SPEED_PRESET == "maximum":
        ServerConfig.CHUNK_SIZE = 8 * 1024 * 1024  # 8MB
        ServerConfig.SOCKET_BUFFER_SIZE = 4 * 1024 * 1024  # 4MB
        ServerConfig.THREADED = True
        print("🚀 Applied MAXIMUM SPEED preset (8MB chunks)")
    elif ServerConfig.SPEED_PRESET == "balanced":
        ServerConfig.CHUNK_SIZE = 4 * 1024 * 1024  # 4MB
        ServerConfig.SOCKET_BUFFER_SIZE = 2 * 1024 * 1024  # 2MB
        ServerConfig.THREADED = True
        print("⚖️ Applied BALANCED preset (4MB chunks)")
    elif ServerConfig.SPEED_PRESET == "conservative":
        ServerConfig.CHUNK_SIZE = 1 * 1024 * 1024  # 1MB
        ServerConfig.SOCKET_BUFFER_SIZE = 512 * 1024  # 512KB
        ServerConfig.THREADED = True
        print("🛡️ Applied CONSERVATIVE preset (1MB chunks)")
else:
    print(f"🎛️ Using CUSTOM settings ({ServerConfig.CHUNK_SIZE//(1024*1024)}MB chunks)")

# Import the rest of the server implementation from the unified server
# (The rest of the code is identical to server_unified.py)

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = ServerConfig.MAX_CONTENT_LENGTH

class OptimizedRequestHandler(WSGIRequestHandler):
    """Enhanced request handler with socket optimizations"""
    
    def setup(self):
        super().setup()
        if ServerConfig.SOCKET_BUFFER_SIZE > 0:
            try:
                self.connection.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, ServerConfig.SOCKET_BUFFER_SIZE)
                self.connection.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, ServerConfig.SOCKET_BUFFER_SIZE)
                if ServerConfig.DEBUG_MODE:
                    print(f"🔧 Set socket buffers to {format_size(ServerConfig.SOCKET_BUFFER_SIZE)}")
            except Exception as e:
                if ServerConfig.DEBUG_MODE:
                    print(f"⚠️ Could not set socket buffers: {e}")

# [Rest of the server implementation - same as server_unified.py]
# Including all the route handlers, UI generators, etc.

@app.route('/<path:filename>')
def download_file(filename):
    """Unified file download with all optimizations"""
    file_path = os.path.join(ServerConfig.SHARE_DIR, filename)
    
    # Security and existence checks
    if not os.path.exists(file_path) or not os.path.isfile(file_path):
        return "File not found", 404
    
    if not os.path.abspath(file_path).startswith(os.path.abspath(ServerConfig.SHARE_DIR)):
        return "Access denied", 403
    
    # File information
    file_size = os.path.getsize(file_path)
    mimetype = mimetypes.guess_type(filename)[0] or 'application/octet-stream'
    
    if ServerConfig.DEBUG_MODE:
        print(f"📁 Serving: {filename} ({format_size(file_size)})")
    
    # Handle range requests for resume capability
    range_header = request.headers.get('Range') if ServerConfig.ENABLE_RANGE_REQUESTS else None
    if range_header:
        return handle_range_request(file_path, file_size, range_header, mimetype, filename)
    
    # Full file download with optimized streaming
    def stream_file():
        try:
            with open(file_path, 'rb', buffering=ServerConfig.CHUNK_SIZE) as f:
                bytes_sent = 0
                while True:
                    chunk = f.read(ServerConfig.CHUNK_SIZE)
                    if not chunk:
                        break
                    bytes_sent += len(chunk)
                    yield chunk
                    
                if ServerConfig.DEBUG_MODE:
                    print(f"✅ Sent {format_size(bytes_sent)} for {filename}")
        except Exception as e:
            print(f"❌ Error streaming {filename}: {e}")
            return
    
    # Prepare response headers
    headers = {
        'Content-Length': str(file_size),
        'Content-Type': mimetype,
        'Content-Disposition': f'attachment; filename="{filename}"',
    }
    
    if ServerConfig.ENABLE_RANGE_REQUESTS:
        headers['Accept-Ranges'] = 'bytes'
    
    if ServerConfig.ENABLE_CACHE:
        headers['Cache-Control'] = f'public, max-age={ServerConfig.CACHE_MAX_AGE}'
        headers['Last-Modified'] = time.strftime('%a, %d %b %Y %H:%M:%S GMT', 
                                               time.gmtime(os.path.getmtime(file_path)))
    
    return Response(stream_file(), headers=headers)

def handle_range_request(file_path, file_size, range_header, mimetype, filename):
    """Handle HTTP range requests for partial content/resume downloads"""
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
        return "Invalid range request", 400
    
    if byte_start < 0 or byte_start >= file_size or byte_end < byte_start:
        return "Range not satisfiable", 416
    
    content_length = byte_end - byte_start + 1
    
    if ServerConfig.DEBUG_MODE:
        print(f"📊 Range request: {byte_start}-{byte_end}/{file_size} ({format_size(content_length)})")
    
    def stream_partial():
        try:
            with open(file_path, 'rb', buffering=ServerConfig.CHUNK_SIZE) as f:
                f.seek(byte_start)
                remaining = content_length
                
                while remaining > 0:
                    chunk_size = min(ServerConfig.CHUNK_SIZE, remaining)
                    chunk = f.read(chunk_size)
                    if not chunk:
                        break
                    remaining -= len(chunk)
                    yield chunk
        except Exception as e:
            print(f"❌ Range request error for {filename}: {e}")
            return
    
    response = Response(
        stream_partial(),
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
    """Unified file listing with configurable UI styles"""
    try:
        files_info = []
        total_size = 0
        
        for filename in sorted(os.listdir(ServerConfig.SHARE_DIR)):
            file_path = os.path.join(ServerConfig.SHARE_DIR, filename)
            if os.path.isfile(file_path):
                size = os.path.getsize(file_path)
                total_size += size
                
                file_info = {'name': filename, 'size': format_size(size), 'raw_size': size}
                
                if ServerConfig.SHOW_FILE_DETAILS:
                    file_info['modified'] = time.strftime('%Y-%m-%d %H:%M', 
                                                        time.localtime(os.path.getmtime(file_path)))
                
                files_info.append(file_info)
        
        # Generate UI based on style setting
        if ServerConfig.UI_STYLE == "simple":
            return generate_simple_ui(files_info, total_size)
        elif ServerConfig.UI_STYLE == "enhanced":
            return generate_enhanced_ui(files_info, total_size)
        else:  # professional
            return generate_professional_ui(files_info, total_size)
            
    except Exception as e:
        return f"Error listing files: {str(e)}", 500

def generate_simple_ui(files_info, total_size):
    """Simple HTML listing"""
    files_html = []
    for file_info in files_info:
        files_html.append(f'<p><a href="/{file_info["name"]}" style="font-size:18px">{file_info["name"]}</a> ({file_info["size"]})</p>')
    
    return f"""
    <html><head><title>Unified File Server - Simple Mode</title></head>
    <body style="font-family: Arial; margin: 40px;">
    <h1>🚀 Unified File Server</h1>
    <p><strong>Mode:</strong> Simple UI | <strong>Files:</strong> {len(files_info)} | <strong>Total:</strong> {format_size(total_size)}</p>
    <p><strong>Performance:</strong> {format_size(ServerConfig.CHUNK_SIZE)} chunks • Range requests: {'✅' if ServerConfig.ENABLE_RANGE_REQUESTS else '❌'}</p>
    <hr>
    {''.join(files_html)}
    </body></html>
    """

def generate_enhanced_ui(files_info, total_size):
    """Enhanced UI with better styling"""
    template = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Unified File Server - Enhanced Mode</title>
        <style>
            body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 0; padding: 20px; background: #f5f5f5; }
            .container { max-width: 1000px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
            h1 { color: #333; text-align: center; margin-bottom: 20px; }
            .stats { background: #e8f4f8; padding: 15px; border-radius: 5px; margin-bottom: 20px; }
            .file { margin: 10px 0; padding: 15px; border: 1px solid #ddd; border-radius: 5px; background: #fafafa; }
            .file:hover { background: #f0f8ff; }
            a { color: #007acc; text-decoration: none; font-weight: bold; }
            a:hover { text-decoration: underline; }
            .size { color: #666; margin-left: 10px; }
            .config { background: #fff3cd; padding: 10px; border-radius: 5px; margin-bottom: 15px; font-size: 12px; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🚀 Unified File Server - Enhanced</h1>
            
            <div class="config">
                <strong>Configuration:</strong> 
                Chunks: {{ chunk_size }} | 
                Socket Buffer: {{ socket_buffer }} | 
                Range Requests: {{ range_support }} |
                Cache: {{ cache_status }}
            </div>
            
            <div class="stats">
                <strong>{{ file_count }}</strong> files available | 
                Total size: <strong>{{ total_size }}</strong>
            </div>
            
            {% for file in files_info %}
            <div class="file">
                <a href="/{{ file.name }}">📄 {{ file.name }}</a>
                <span class="size">({{ file.size }})</span>
                {% if file.modified %}
                <span class="size"> - Modified: {{ file.modified }}</span>
                {% endif %}
            </div>
            {% endfor %}
        </div>
    </body>
    </html>
    """
    
    return render_template_string(template, 
                                files_info=files_info,
                                file_count=len(files_info),
                                total_size=format_size(total_size),
                                chunk_size=format_size(ServerConfig.CHUNK_SIZE),
                                socket_buffer=format_size(ServerConfig.SOCKET_BUFFER_SIZE),
                                range_support='✅' if ServerConfig.ENABLE_RANGE_REQUESTS else '❌',
                                cache_status='✅' if ServerConfig.ENABLE_CACHE else '❌')

def generate_professional_ui(files_info, total_size):
    """Professional UI with full table layout and configuration display"""
    template = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Unified File Server - Professional</title>
        <meta charset="utf-8">
        <style>
            body { font-family: system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; margin: 0; padding: 20px; background: #f8f9fa; }
            .container { max-width: 1200px; margin: 0 auto; background: white; padding: 30px; border-radius: 8px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }
            h1 { color: #212529; text-align: center; margin-bottom: 30px; }
            .config-panel { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px; border-radius: 8px; margin-bottom: 20px; }
            .config-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px; margin-top: 15px; }
            .config-item { background: rgba(255,255,255,0.1); padding: 10px; border-radius: 5px; }
            .stats { background: #e3f2fd; padding: 15px; border-radius: 6px; margin-bottom: 20px; text-align: center; }
            table { width: 100%; border-collapse: collapse; margin-top: 20px; }
            th, td { padding: 12px; text-align: left; border-bottom: 1px solid #dee2e6; }
            th { background: #495057; color: white; font-weight: 600; }
            tr:hover { background: #f8f9fa; }
            a { color: #0066cc; text-decoration: none; font-weight: 500; }
            a:hover { text-decoration: underline; color: #0052a3; }
            .size { text-align: right; font-family: 'SF Mono', Monaco, 'Cascadia Code', monospace; }
            .download-btn { background: #28a745; color: white; padding: 6px 12px; border-radius: 4px; text-decoration: none; font-size: 11px; }
            .download-btn:hover { background: #218838; text-decoration: none; color: white; }
            .performance-indicator { display: inline-block; padding: 2px 6px; border-radius: 3px; font-size: 10px; font-weight: bold; }
            .high-performance { background: #d4edda; color: #155724; }
            .medium-performance { background: #fff3cd; color: #856404; }
            .low-performance { background: #f8d7da; color: #721c24; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🚀 Unified High-Performance File Server</h1>
            
            <div class="config-panel">
                <h3 style="margin-top: 0;">⚙️ Current Configuration - {{ preset_name }}</h3>
                <div class="config-grid">
                    <div class="config-item">
                        <strong>Chunk Size:</strong><br>{{ chunk_size }}
                        <span class="performance-indicator {{ chunk_performance }}">{{ chunk_level }}</span>
                    </div>
                    <div class="config-item">
                        <strong>Socket Buffer:</strong><br>{{ socket_buffer }}
                    </div>
                    <div class="config-item">
                        <strong>Range Requests:</strong><br>{{ range_support }}
                    </div>
                    <div class="config-item">
                        <strong>Caching:</strong><br>{{ cache_status }}
                    </div>
                    <div class="config-item">
                        <strong>Server Mode:</strong><br>{{ server_mode }}
                    </div>
                    <div class="config-item">
                        <strong>Threading:</strong><br>{{ threading_status }}
                    </div>
                </div>
                <div style="margin-top: 15px; font-size: 12px; opacity: 0.9;">
                    💡 To modify settings, edit server_config.ini and restart the server
                </div>
            </div>
            
            <div class="stats">
                <strong>{{ file_count }}</strong> files available | 
                Total size: <strong>{{ total_size }}</strong> | 
                Configuration-driven performance optimization
            </div>
            
            {% if files_info %}
            <table>
                <thead>
                    <tr>
                        <th>📁 File Name</th>
                        <th class="size">📊 Size</th>
                        {% if show_details %}
                        <th>🕒 Modified</th>
                        {% endif %}
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
                        {% if show_details and file.modified %}
                        <td>{{ file.modified }}</td>
                        {% endif %}
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
                <strong>Features:</strong>
                • Configuration file driven setup (server_config.ini)
                • Multiple speed presets and manual tuning
                • Professional interface with real-time settings display
                • Resume downloads with HTTP Range requests
                • Production-ready with Gunicorn support
            </div>
        </div>
    </body>
    </html>
    """
    
    # Determine performance indicators
    chunk_mb = ServerConfig.CHUNK_SIZE / (1024 * 1024)
    if chunk_mb >= 6:
        chunk_performance = "high-performance"
        chunk_level = "HIGH"
    elif chunk_mb >= 2:
        chunk_performance = "medium-performance" 
        chunk_level = "MEDIUM"
    else:
        chunk_performance = "low-performance"
        chunk_level = "LOW"
    
    return render_template_string(template,
                                files_info=files_info,
                                file_count=len(files_info),
                                total_size=format_size(total_size),
                                chunk_size=format_size(ServerConfig.CHUNK_SIZE),
                                socket_buffer=format_size(ServerConfig.SOCKET_BUFFER_SIZE),
                                range_support='✅ Enabled' if ServerConfig.ENABLE_RANGE_REQUESTS else '❌ Disabled',
                                cache_status='✅ Enabled' if ServerConfig.ENABLE_CACHE else '❌ Disabled',
                                server_mode='Production (Gunicorn)' if ServerConfig.USE_PRODUCTION_SERVER else 'Development (Flask)',
                                threading_status='✅ Enabled' if ServerConfig.THREADED else '❌ Disabled',
                                show_details=ServerConfig.SHOW_FILE_DETAILS,
                                chunk_performance=chunk_performance,
                                chunk_level=chunk_level,
                                preset_name=ServerConfig.SPEED_PRESET.upper())

def format_size(size_bytes):
    """Format file size in human readable format"""
    if size_bytes == 0:
        return "0 B"
    
    size_names = ["B", "KB", "MB", "GB", "TB", "PB"]
    import math
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return f"{s} {size_names[i]}"

def run_with_gunicorn():
    """Run with Gunicorn for production performance"""
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
            'bind': f'{ServerConfig.HOST}:{ServerConfig.PORT}',
            'workers': ServerConfig.WORKER_COUNT,
            'worker_class': 'gevent',
            'worker_connections': ServerConfig.WORKER_CONNECTIONS,
            'keepalive': 2,
            'max_requests': 1000,
            'timeout': ServerConfig.CONNECTION_TIMEOUT,
            'preload_app': True
        }
        
        print("🏭 Starting production server with Gunicorn...")
        print(f"📁 Serving: {ServerConfig.SHARE_DIR}")
        print(f"🌐 URL: http://{ServerConfig.HOST}:{ServerConfig.PORT}")
        print(f"👥 Workers: {ServerConfig.WORKER_COUNT}")
        print("⚡ Performance: Gunicorn + Gevent workers")
        
        StandaloneApplication(app, options).run()
        return True
        
    except ImportError:
        print("❌ Gunicorn not installed. Install with: pip install gunicorn gevent")
        print("🔄 Falling back to Flask development server...")
        return False
    except Exception as e:
        print(f"❌ Production server failed: {e}")
        print("🔄 Falling back to Flask development server...")
        return False

def print_startup_info():
    """Print server configuration and startup information"""
    print("=" * 70)
    print("🚀 UNIFIED HIGH-PERFORMANCE FILE SERVER - CONFIG VERSION")
    print("=" * 70)
    print(f"📁 Serving directory: {ServerConfig.SHARE_DIR}")
    print(f"🌐 Server URL: http://{ServerConfig.HOST}:{ServerConfig.PORT}")
    print(f"🎨 UI Style: {ServerConfig.UI_STYLE}")
    print(f"📄 Configuration: server_config.ini")
    print()
    print("⚡ PERFORMANCE CONFIGURATION:")
    print(f"   • Preset: {ServerConfig.SPEED_PRESET.upper()}")
    print(f"   • Chunk Size: {format_size(ServerConfig.CHUNK_SIZE)}")
    print(f"   • Socket Buffer: {format_size(ServerConfig.SOCKET_BUFFER_SIZE)}")
    print(f"   • Max File Size: {format_size(ServerConfig.MAX_CONTENT_LENGTH)}")
    print(f"   • Range Requests: {'✅' if ServerConfig.ENABLE_RANGE_REQUESTS else '❌'}")
    print(f"   • Caching: {'✅' if ServerConfig.ENABLE_CACHE else '❌'}")
    print(f"   • Threading: {'✅' if ServerConfig.THREADED else '❌'}")
    print()
    print("🔧 SERVER SETTINGS:")
    print(f"   • Production Mode: {'✅' if ServerConfig.USE_PRODUCTION_SERVER else '❌'}")
    if ServerConfig.USE_PRODUCTION_SERVER:
        print(f"   • Workers: {ServerConfig.WORKER_COUNT}")
        print(f"   • Connections/Worker: {ServerConfig.WORKER_CONNECTIONS}")
    print(f"   • Debug Mode: {'✅' if ServerConfig.DEBUG_MODE else '❌'}")
    print(f"   • Connection Timeout: {ServerConfig.CONNECTION_TIMEOUT}s")
    print()
    print("🎛️ TO MODIFY SETTINGS:")
    print("   Edit server_config.ini and restart the server")
    print("   Available presets: maximum, balanced, conservative, custom")
    print("=" * 70)

if __name__ == "__main__":
    print_startup_info()
    
    # Try production server first if enabled
    if ServerConfig.USE_PRODUCTION_SERVER:
        if run_with_gunicorn():
            sys.exit(0)
    
    # Fallback to Flask development server
    print("🔧 Starting Flask development server...")
    print(f"⚡ Optimizations active: {format_size(ServerConfig.CHUNK_SIZE)} chunks, "
          f"{'threaded' if ServerConfig.THREADED else 'single-threaded'}")
    print("Press Ctrl+C to stop...")
    print()
    
    try:
        app.run(
            host=ServerConfig.HOST,
            port=ServerConfig.PORT,
            threaded=ServerConfig.THREADED,
            debug=ServerConfig.DEBUG_MODE,
            request_handler=OptimizedRequestHandler if ServerConfig.SOCKET_BUFFER_SIZE > 0 else None
        )
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
    except Exception as e:
        print(f"❌ Server error: {e}")