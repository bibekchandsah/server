"""
Ngrok-optimized file server
Designed to work better with ngrok's limitations
"""

from flask import Flask, Response, request, stream_template_string
import os
import mimetypes
import time
import threading

app = Flask(__name__)
SHARE_DIR = r"D:/server/index"

# Ngrok-optimized settings
CHUNK_SIZE = 512 * 1024  # 512KB chunks (smaller for ngrok)
MAX_CONCURRENT = 3  # Limit concurrent downloads

# Track active downloads
active_downloads = threading.Semaphore(MAX_CONCURRENT)

@app.route('/<path:filename>')
def download_file(filename):
    """Ngrok-optimized file download"""
    
    # Limit concurrent downloads to prevent ngrok throttling
    if not active_downloads.acquire(blocking=False):
        return "Server busy, please try again", 503
    
    try:
        file_path = os.path.join(SHARE_DIR, filename)
        
        if not os.path.exists(file_path):
            return "File not found", 404
        
        file_size = os.path.getsize(file_path)
        mimetype = mimetypes.guess_type(filename)[0] or 'application/octet-stream'
        
        # Handle range requests (still important for resume)
        range_header = request.headers.get('Range')
        if range_header:
            return handle_range_request(file_path, file_size, range_header, mimetype, filename)
        
        # Optimized streaming for ngrok
        def stream_file():
            try:
                with open(file_path, 'rb', buffering=CHUNK_SIZE*2) as f:
                    while True:
                        chunk = f.read(CHUNK_SIZE)
                        if not chunk:
                            break
                        yield chunk
                        # Small delay to prevent ngrok throttling
                        time.sleep(0.001)
            except Exception as e:
                print(f"Streaming error: {e}")
            finally:
                active_downloads.release()
        
        response = Response(
            stream_file(),
            headers={
                'Content-Length': str(file_size),
                'Content-Type': mimetype,
                'Accept-Ranges': 'bytes',
                'Content-Disposition': f'attachment; filename="{filename}"',
                'Cache-Control': 'public, max-age=86400',  # 24 hour cache
                'Connection': 'keep-alive'
            }
        )
        return response
    
    except Exception as e:
        active_downloads.release()
        return f"Error: {str(e)}", 500

def handle_range_request(file_path, file_size, range_header, mimetype, filename):
    """Optimized range requests for ngrok"""
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
            active_downloads.release()
            return "Invalid range", 400
    
    if byte_start >= file_size or byte_end < byte_start:
        active_downloads.release()
        return "Range not satisfiable", 416
    
    content_length = byte_end - byte_start + 1
    
    def stream_partial():
        try:
            with open(file_path, 'rb', buffering=CHUNK_SIZE*2) as f:
                f.seek(byte_start)
                remaining = content_length
                while remaining > 0:
                    chunk_size = min(CHUNK_SIZE, remaining)
                    chunk = f.read(chunk_size)
                    if not chunk:
                        break
                    remaining -= len(chunk)
                    yield chunk
                    time.sleep(0.001)  # Prevent ngrok throttling
        except Exception as e:
            print(f"Partial streaming error: {e}")
        finally:
            active_downloads.release()
    
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
    """Enhanced file listing for ngrok"""
    files_info = []
    for filename in sorted(os.listdir(SHARE_DIR)):
        if os.path.isfile(os.path.join(SHARE_DIR, filename)):
            size = os.path.getsize(os.path.join(SHARE_DIR, filename))
            files_info.append({
                'name': filename,
                'size': format_size(size),
                'raw_size': size
            })
    
    template = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Ngrok File Server</title>
        <meta charset="utf-8">
        <style>
            body { font-family: system-ui; margin: 20px; background: #f8f9fa; }
            .container { max-width: 800px; margin: 0 auto; background: white; padding: 20px; border-radius: 8px; }
            .warning { background: #fff3cd; border: 1px solid #ffeaa7; padding: 15px; border-radius: 5px; margin: 15px 0; }
            .file { margin: 10px 0; padding: 15px; border: 1px solid #ddd; border-radius: 5px; }
            .file a { text-decoration: none; font-weight: bold; color: #0066cc; }
            .file a:hover { text-decoration: underline; }
            .download-btn { background: #28a745; color: white; padding: 8px 15px; border-radius: 4px; text-decoration: none; margin-left: 10px; }
            .download-btn:hover { background: #218838; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🌐 Ngrok File Server</h1>
            
            <div class="warning">
                <strong>⚠️ Ngrok Limitations:</strong><br>
                • Free tier: ~1 Mbps speed limit<br>
                • 40 requests/minute limit<br>
                • For faster speeds, consider upgrading ngrok or using alternatives below
            </div>
            
            <h3>📁 Available Files ({{ files_info|length }})</h3>
            {% for file in files_info %}
            <div class="file">
                <a href="/{{ file.name }}">📄 {{ file.name }}</a>
                <span style="color: #666;">({{ file.size }})</span>
                <a href="/{{ file.name }}" class="download-btn">Download</a>
            </div>
            {% endfor %}
            
            <hr style="margin: 30px 0;">
            <h3>🚀 For Faster Speeds:</h3>
            <ul>
                <li><strong>Upgrade ngrok:</strong> <a href="https://ngrok.com/pricing">ngrok Pro/Business plans</a></li>
                <li><strong>Alternative:</strong> Use direct IP + port forwarding</li>
                <li><strong>Cloud:</strong> Upload to cloud storage (Google Drive, Dropbox)</li>
                <li><strong>P2P:</strong> Use torrents for large files</li>
            </ul>
        </div>
    </body>
    </html>
    """
    
    return stream_template_string(template, files_info=files_info)

def format_size(bytes):
    for unit in ['B', 'KB', 'MB', 'GB']:
        if bytes < 1024:
            return f"{bytes:.1f} {unit}"
        bytes /= 1024
    return f"{bytes:.1f} TB"

@app.route('/speed-test')
def speed_test():
    """Simple speed test endpoint"""
    return """
    <html><body>
    <h2>Speed Test</h2>
    <p>Download this <a href="/speed-test-file">1MB test file</a> to check your speed through ngrok.</p>
    </body></html>
    """

@app.route('/speed-test-file')
def speed_test_file():
    """Generate a test file for speed testing"""
    def generate_test_data():
        # Generate 1MB of test data
        chunk = b'A' * 1024  # 1KB chunk
        for _ in range(1024):  # 1024 chunks = 1MB
            yield chunk
    
    return Response(
        generate_test_data(),
        headers={
            'Content-Type': 'application/octet-stream',
            'Content-Disposition': 'attachment; filename="speed-test-1MB.bin"',
            'Content-Length': str(1024 * 1024)
        }
    )

if __name__ == "__main__":
    print("🌐 Starting Ngrok-Optimized File Server")
    print(f"📁 Directory: {SHARE_DIR}")
    print(f"🌐 Local URL: http://localhost:8000")
    print(f"⚡ Chunk size: {CHUNK_SIZE//1024}KB (optimized for ngrok)")
    print(f"👥 Max concurrent: {MAX_CONCURRENT} downloads")
    print("📝 Ngrok limitations: ~1 Mbps on free tier")
    print("\n🚀 For better performance:")
    print("• Upgrade to ngrok paid plan")
    print("• Use direct IP with port forwarding")
    print("• Consider cloud storage alternatives")
    
    app.run(host='0.0.0.0', port=8000, threaded=True, debug=False)