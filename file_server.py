#!/usr/bin/env python3
"""
🚀 HIGH-PERFORMANCE FILE SERVER
Single-file solution for fast file sharing with professional UI

Author: Bibek Chand Sah
Features: Maximum speed, resume downloads, multi-user support, professional interface
"""

import os
import sys
import time
import socket
import mimetypes
from flask import Flask, Response, request, render_template_string
from werkzeug.serving import WSGIRequestHandler

# ============================================================================
# SERVER CONFIGURATION - Maximum Performance Settings
# ============================================================================

class ServerConfig:
    """Pre-configured for maximum performance and features"""
    
    # Performance Settings - Maximum Speed
    CHUNK_SIZE_MB = 8                    # 8 MB chunks for maximum throughput
    SOCKET_BUFFER_MB = 4                 # 4 MB socket buffers
    MAX_FILE_SIZE_GB = 16                # 16 GB file size limit
    
    # Calculated values
    CHUNK_SIZE = CHUNK_SIZE_MB * 1024 * 1024
    SOCKET_BUFFER_SIZE = SOCKET_BUFFER_MB * 1024 * 1024
    MAX_CONTENT_LENGTH = MAX_FILE_SIZE_GB * 1024 * 1024 * 1024
    
    # Features - All Enabled
    ENABLE_RANGE_REQUESTS = True         # Resume downloads support
    ENABLE_THREADING = True              # Multiple users & files
    ENABLE_CACHE = True                  # HTTP caching
    CACHE_HOURS = 1                      # 1 hour cache
    CACHE_MAX_AGE = CACHE_HOURS * 3600
    
    # UI Settings
    UI_STYLE = "professional"            # Professional with file details
    SHOW_FILE_DETAILS = True
    
    # Server Settings (will be set by user)
    SHARE_DIR = None
    PORT = 8000
    HOST = '0.0.0.0'
    DEBUG_MODE = False

# Get user input for configuration
def get_user_configuration():
    """Prompt user for directory and port configuration"""
    
    print("=" * 80)
    print("🚀 HIGH-PERFORMANCE FILE SERVER")
    print("=" * 80)
    print()
    
    # Get share directory
    print("📁 DIRECTORY CONFIGURATION:")
    default_dir = r"D:\server\index"
    
    while True:
        share_dir = input(f"Enter directory path to share (or press Enter for '{default_dir}'): ").strip()
        
        if not share_dir:
            share_dir = default_dir
        
        # Remove quotes if user pasted path with quotes
        share_dir = share_dir.strip('"').strip("'")
        
        # Normalize path
        share_dir = os.path.abspath(share_dir)
        
        if os.path.exists(share_dir) and os.path.isdir(share_dir):
            ServerConfig.SHARE_DIR = share_dir
            print(f"✅ Selected directory: {share_dir}")
            break
        else:
            print(f"❌ Directory not found: {share_dir}")
            print("Please enter a valid directory path.")
            print()
    
    # Count files in directory
    try:
        file_count = len([f for f in os.listdir(ServerConfig.SHARE_DIR) 
                        if os.path.isfile(os.path.join(ServerConfig.SHARE_DIR, f))])
        print(f"✅ Found {file_count} files in directory")
    except:
        file_count = 0
    
    print()
    
    # Get port
    print("🌐 PORT CONFIGURATION:")
    while True:
        port_input = input(f"Enter port number (default: {ServerConfig.PORT}): ").strip()
        
        if not port_input:
            port_input = str(ServerConfig.PORT)
        
        try:
            port = int(port_input)
            if 1024 <= port <= 65535:
                ServerConfig.PORT = port
                print(f"✅ Selected port: {port}")
                break
            else:
                print("❌ Port must be between 1024 and 65535")
        except ValueError:
            print("❌ Invalid port number. Please enter a number.")
    
    print()
    print("-" * 80)
    print()

# ============================================================================
# FLASK APPLICATION SETUP
# ============================================================================

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = ServerConfig.MAX_CONTENT_LENGTH

class OptimizedRequestHandler(WSGIRequestHandler):
    """Enhanced request handler with socket optimizations"""
    
    def setup(self):
        super().setup()
        try:
            # Set large socket buffers for maximum throughput
            self.connection.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, ServerConfig.SOCKET_BUFFER_SIZE)
            self.connection.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, ServerConfig.SOCKET_BUFFER_SIZE)
        except Exception as e:
            if ServerConfig.DEBUG_MODE:
                print(f"⚠️ Socket buffer setup warning: {e}")

def format_size(size_bytes):
    """Format file size in human readable format"""
    if size_bytes == 0:
        return "0 B"
    
    size_names = ["B", "KB", "MB", "GB", "TB"]
    import math
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return f"{s} {size_names[i]}"

# ============================================================================
# FILE DOWNLOAD ROUTE - Optimized for Maximum Speed
# ============================================================================

@app.route('/<path:filename>')
def download_file(filename):
    """High-performance file download with resume support"""
    file_path = os.path.join(ServerConfig.SHARE_DIR, filename)
    
    # Security and existence checks
    if not os.path.exists(file_path) or not os.path.isfile(file_path):
        return "❌ File not found", 404
    
    if not os.path.abspath(file_path).startswith(os.path.abspath(ServerConfig.SHARE_DIR)):
        return "❌ Access denied", 403
    
    # File information
    file_size = os.path.getsize(file_path)
    mimetype = mimetypes.guess_type(filename)[0] or 'application/octet-stream'
    
    # Handle range requests for resume capability
    range_header = request.headers.get('Range') if ServerConfig.ENABLE_RANGE_REQUESTS else None
    if range_header:
        return handle_range_request(file_path, file_size, range_header, mimetype, filename)
    
    # Full file download with maximum speed streaming
    def stream_file():
        try:
            with open(file_path, 'rb', buffering=ServerConfig.CHUNK_SIZE) as f:
                while True:
                    chunk = f.read(ServerConfig.CHUNK_SIZE)
                    if not chunk:
                        break
                    yield chunk
        except Exception as e:
            print(f"❌ Error streaming {filename}: {e}")
            return
    
    # Prepare response headers
    headers = {
        'Content-Length': str(file_size),
        'Content-Type': mimetype,
        'Content-Disposition': f'attachment; filename="{filename}"',
        'Accept-Ranges': 'bytes',
        'Cache-Control': f'public, max-age={ServerConfig.CACHE_MAX_AGE}',
        'Last-Modified': time.strftime('%a, %d %b %Y %H:%M:%S GMT', 
                                      time.gmtime(os.path.getmtime(file_path)))
    }
    
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
        return "❌ Invalid range request", 400
    
    if byte_start < 0 or byte_start >= file_size or byte_end < byte_start:
        return "❌ Range not satisfiable", 416
    
    content_length = byte_end - byte_start + 1
    
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

# ============================================================================
# FILE LISTING ROUTE - Professional UI
# ============================================================================

@app.route('/')
def list_files():
    """Professional file listing with detailed information"""
    try:
        files_info = []
        total_size = 0
        
        for filename in sorted(os.listdir(ServerConfig.SHARE_DIR)):
            file_path = os.path.join(ServerConfig.SHARE_DIR, filename)
            if os.path.isfile(file_path):
                size = os.path.getsize(file_path)
                total_size += size
                
                file_info = {
                    'name': filename,
                    'size': format_size(size),
                    'raw_size': size,
                    'modified': time.strftime('%Y-%m-%d %H:%M:%S', 
                                            time.localtime(os.path.getmtime(file_path)))
                }
                
                files_info.append(file_info)
        
        return generate_professional_ui(files_info, total_size)
            
    except Exception as e:
        return f"❌ Error listing files: {str(e)}", 500

def generate_professional_ui(files_info, total_size):
    """Professional HTML interface with full features"""
    template = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>High-Performance File Server</title>
        <link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='0.9em' font-size='90'>🚀</text></svg>">
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body {
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                padding: 20px;
                min-height: 100vh;
            }
            .container {
                max-width: 1200px;
                margin: 0 auto;
                background: white;
                border-radius: 12px;
                box-shadow: 0 20px 60px rgba(0,0,0,0.3);
                overflow: hidden;
            }
            .header {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 30px;
                text-align: center;
            }
            .header h1 {
                font-size: 32px;
                margin-bottom: 10px;
                font-weight: 700;
            }
            .header p {
                opacity: 0.9;
                font-size: 16px;
            }
            .config-panel {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                padding: 20px 30px;
                border-bottom: 1px solid rgba(102, 126, 234, 0.2);
            }
            .config-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                gap: 15px;
                margin-top: 15px;
            }
            .config-item {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                padding: 15px;
                border-radius: 8px;
                border-left: 4px solid #8899e3;
            }
            .config-label {
                font-size: 12px;
                color: #eeeeff;
                text-transform: uppercase;
                font-weight: 600;
                margin-bottom: 5px;
            }
            .config-value {
                font-size: 18px;
                color: #212529;
                font-weight: 600;
            }
            .stats {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 20px 30px;
                display: flex;
                justify-content: space-around;
                flex-wrap: wrap;
                gap: 20px;
                border-bottom: 1px solid rgba(102, 126, 234, 0.2);
            }
            .stat-item {
                text-align: center;
            }
            .stat-value {
                font-size: 28px;
                font-weight: 700;
                margin-bottom: 5px;
            }
            .stat-label {
                font-size: 14px;
                opacity: 0.9;
            }
            .content {
                padding: 30px;
            }
            table {
                width: 100%;
                border-collapse: collapse;
                margin-top: 20px;
            }
            thead {
                background: #f8f9fa;
            }
            th {
                padding: 15px;
                text-align: left;
                font-weight: 600;
                color: #495057;
                border-bottom: 2px solid #dee2e6;
                font-size: 14px;
                text-transform: uppercase;
            }
            td {
                padding: 15px;
                border-bottom: 1px solid #dee2e6;
            }
            tr:hover {
                background: #f8f9fa;
                transition: background 0.2s;
            }
            .file-name {
                display: flex;
                align-items: center;
                gap: 10px;
            }
            .file-icon {
                font-size: 24px;
            }
            .file-link {
                color: #667eea;
                text-decoration: none;
                font-weight: 500;
                word-break: break-all;
            }
            .file-link:hover {
                text-decoration: underline;
                color: #764ba2;
            }
            .size-cell {
                font-family: 'SF Mono', Monaco, 'Courier New', monospace;
                color: #495057;
                text-align: right;
            }
            .date-cell {
                color: #6c757d;
                font-size: 14px;
            }
            .download-btn {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 8px 16px;
                border-radius: 6px;
                text-decoration: none;
                font-size: 13px;
                font-weight: 600;
                display: inline-block;
                transition: transform 0.2s, box-shadow 0.2s;
            }
            .download-btn:hover {
                transform: translateY(-2px);
                box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
            }
            .empty-state {
                text-align: center;
                padding: 60px 20px;
                color: #6c757d;
            }
            .empty-icon {
                font-size: 64px;
                margin-bottom: 20px;
            }
            .footer {
                background: #f8f9fa;
                padding: 20px 30px;
                border-top: 1px solid #dee2e6;
                text-align: center;
                color: #6c757d;
                font-size: 13px;
            }
            .feature-badge {
                display: inline-block;
                background: #28a745;
                color: white;
                padding: 2px 8px;
                border-radius: 4px;
                font-size: 11px;
                font-weight: 600;
                margin: 0 3px;
            }
            
            /* Mobile Responsive Styles */
            @media (max-width: 768px) {
                body {
                    padding: 10px;
                }
                
                .container {
                    border-radius: 8px;
                }
                
                .header h1 {
                    font-size: 24px;
                }
                
                .header p {
                    font-size: 14px;
                }
                
                .header {
                    padding: 20px;
                }
                
                .config-panel {
                    padding: 15px;
                }
                
                .config-grid {
                    grid-template-columns: 1fr;
                    gap: 10px;
                }
                
                .config-item {
                    padding: 12px;
                }
                
                .config-label {
                    font-size: 11px;
                }
                
                .config-value {
                    font-size: 16px;
                }
                
                .stats {
                    padding: 15px;
                    flex-direction: column;
                    gap: 15px;
                }
                
                .stat-item {
                    padding: 10px 0;
                }
                
                .stat-value {
                    font-size: 24px;
                }
                
                .stat-label {
                    font-size: 13px;
                }
                
                .content {
                    padding: 15px;
                    overflow-x: auto;
                }
                
                table {
                    display: block;
                    overflow-x: auto;
                    white-space: nowrap;
                    -webkit-overflow-scrolling: touch;
                }
                
                th, td {
                    padding: 10px 8px;
                    font-size: 13px;
                }
                
                th {
                    font-size: 11px;
                }
                
                .file-icon {
                    font-size: 20px;
                }
                
                .file-link {
                    font-size: 14px;
                }
                
                .size-cell {
                    font-size: 13px;
                }
                
                .date-cell {
                    font-size: 12px;
                }
                
                .download-btn {
                    padding: 6px 12px;
                    font-size: 12px;
                }
                
                .footer {
                    padding: 15px;
                    font-size: 12px;
                }
                
                .empty-state {
                    padding: 40px 15px;
                }
                
                .empty-icon {
                    font-size: 48px;
                }
            }
            
            /* Extra small devices */
            @media (max-width: 480px) {
                .header h1 {
                    font-size: 20px;
                }
                
                .header p {
                    font-size: 13px;
                }
                
                .config-value {
                    font-size: 14px;
                }
                
                .stat-value {
                    font-size: 20px;
                }
                
                th, td {
                    padding: 8px 6px;
                    font-size: 12px;
                }
                
                .file-name {
                    gap: 5px;
                }
                
                .file-icon {
                    font-size: 18px;
                }
                
                .file-link {
                    font-size: 13px;
                }
                
                .download-btn {
                    padding: 5px 10px;
                    font-size: 11px;
                }
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🚀 High-Performance File Server</h1>
                <p>Maximum Speed • Resume Support • Multi-User Ready</p>
            </div>
            
            <div class="config-panel">
                <div style="font-size: 14px; font-weight: 600; color: #ffffff; margin-bottom: 10px;">
                    ⚙️ Server Configuration
                </div>
                <div class="config-grid">
                    <div class="config-item">
                        <div class="config-label">Speed Mode</div>
                        <div class="config-value">⚡ Maximum</div>
                    </div>
                    <div class="config-item">
                        <div class="config-label">Chunk Size</div>
                        <div class="config-value">{{ chunk_size }}</div>
                    </div>
                    <div class="config-item">
                        <div class="config-label">Socket Buffer</div>
                        <div class="config-value">{{ socket_buffer }}</div>
                    </div>
                    <div class="config-item">
                        <div class="config-label">Features</div>
                        <div class="config-value" style="font-size: 14px;">
                            <span class="feature-badge">Resume</span>
                            <span class="feature-badge">Cache</span>
                            <span class="feature-badge">Multi-User</span>
                        </div>
                    </div>
                </div>
            </div>
            
            <div class="stats">
                <div class="stat-item">
                    <div class="stat-value">{{ file_count }}</div>
                    <div class="stat-label">Total Files</div>
                </div>
                <div class="stat-item">
                    <div class="stat-value">{{ total_size }}</div>
                    <div class="stat-label">Total Size</div>
                </div>
                <div class="stat-item">
                    <div class="stat-value">{{ max_file_size }}</div>
                    <div class="stat-label">Max File Limit</div>
                </div>
            </div>
            
            <div class="content">
                {% if files_info %}
                <table>
                    <thead>
                        <tr>
                            <th style="width: 50%;">📁 File Name</th>
                            <th style="width: 15%;">📊 Size</th>
                            <th style="width: 20%;">🕒 Modified</th>
                            <th style="width: 15%; text-align: center;">⬇️ Action</th>
                        </tr>
                    </thead>
                    <tbody>
                        {% for file in files_info %}
                        <tr>
                            <td>
                                <div class="file-name">
                                    <span class="file-icon">📄</span>
                                    <a href="/{{ file.name }}" class="file-link" title="Click to download {{ file.name }}">
                                        {{ file.name }}
                                    </a>
                                </div>
                            </td>
                            <td class="size-cell">{{ file.size }}</td>
                            <td class="date-cell">{{ file.modified }}</td>
                            <td style="text-align: center;">
                                <a href="/{{ file.name }}" class="download-btn">
                                    Download
                                </a>
                            </td>
                        </tr>
                        {% endfor %}
                    </tbody>
                </table>
                {% else %}
                <div class="empty-state">
                    <div class="empty-icon">📂</div>
                    <h3>No Files Available</h3>
                    <p>The shared directory is empty.</p>
                </div>
                {% endif %}
            </div>
            
            <div class="footer">
                <strong>High-Performance File Server</strong> • 
                Optimized for maximum speed with {{ chunk_size }} chunks • 
                Resume downloads enabled • 
                Multi-user support active
            </div>
        </div>
    </body>
    </html>
    """
    
    return render_template_string(
        template,
        files_info=files_info,
        file_count=len(files_info),
        total_size=format_size(total_size),
        chunk_size=format_size(ServerConfig.CHUNK_SIZE),
        socket_buffer=format_size(ServerConfig.SOCKET_BUFFER_SIZE),
        max_file_size=f"{ServerConfig.MAX_FILE_SIZE_GB} GB"
    )

# ============================================================================
# MAIN EXECUTION
# ============================================================================

def get_local_ip():
    """Get local IP address for LAN access"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "Unable to detect"

def display_startup_info():
    """Display server configuration and start info"""
    print("=" * 80)
    print("📋 SERVER CONFIGURATION:")
    print("-" * 80)
    print(f"📦 Chunk Size:           {ServerConfig.CHUNK_SIZE_MB} MB")
    print(f"🔧 Socket Buffer:        {ServerConfig.SOCKET_BUFFER_MB} MB")
    print(f"📊 Max File Size:        {ServerConfig.MAX_FILE_SIZE_GB} GB")
    print(f"⚡ Speed Mode:           MAXIMUM")
    print(f"♻️  Resume Downloads:    {'✅ Enabled' if ServerConfig.ENABLE_RANGE_REQUESTS else '❌ Disabled'}")
    print(f"👥 Multi-User Support:   {'✅ Enabled (Threading)' if ServerConfig.ENABLE_THREADING else '❌ Disabled'}")
    print(f"💾 HTTP Caching:         {'✅ Enabled' if ServerConfig.ENABLE_CACHE else '❌ Disabled'} ({ServerConfig.CACHE_HOURS}h)")
    print("=" * 80)
    print()
    print("✅ SERVER STARTED SUCCESSFULLY!")
    print()
    print("💡 SHARING TIPS:")
    print("   • Use Local URLs on this computer")
    print("   • Use Network URL on your local network (LAN)")
    print("   • For internet sharing, we will use Cloudflare Tunnel")
    print()
    print("🛑 Press CTRL+C to stop the server")
    print("-" * 80)
    print()

def display_clarified_urls():
    """Display clarified URLs after Flask starts"""
    time.sleep(1.5)  # Wait for Flask to print its messages
    local_ip = get_local_ip()
    
    print()
    print("📡 ACCESS YOUR FILES:")
    print(f"   • http://127.0.0.1:{ServerConfig.PORT} (for this pc)")
    if local_ip != "Unable to detect":
        print(f"   • http://{local_ip}:{ServerConfig.PORT} (for same wifi pc)")
    print()

def main():
    """Main entry point"""
    try:
        # STEP 1: Get user configuration FIRST
        get_user_configuration()
        
        # STEP 2: Display configuration
        display_startup_info()
        
        # STEP 3: Start server
        print("🚀 Starting high-performance file server...")
        print()
        
        # Start a thread to display clarified URLs after Flask starts
        import threading
        url_thread = threading.Thread(target=display_clarified_urls, daemon=True)
        url_thread.start()
        
        # Start Flask server
        app.run(
            host=ServerConfig.HOST,
            port=ServerConfig.PORT,
            threaded=ServerConfig.ENABLE_THREADING,
            debug=ServerConfig.DEBUG_MODE,
            request_handler=OptimizedRequestHandler
        )
        
    except KeyboardInterrupt:
        print("\n\n🛑 Server stopped by user")
        print("Thank you for using High-Performance File Server!")
    except Exception as e:
        print(f"\n❌ Server error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    # Check Flask installation
    try:
        import flask
    except ImportError:
        print("❌ Flask is not installed!")
        print("Please install it with: pip install flask")
        sys.exit(1)
    
    # Run the server
    main()
