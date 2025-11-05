from flask import Flask, send_from_directory, Response, request
import os
import mimetypes
from werkzeug.wsgi import FileWrapper

app = Flask(__name__)
# SHARE_DIR = "D:/ShareFolder"
# SHARE_DIR = r"D:\Programming\program exercise\Python\screen share\files"
# SHARE_DIR = r"D:/project/major project/clean"
SHARE_DIR = r"D:/server/index"

# Increase buffer size for better performance
BUFFER_SIZE = 1024 * 1024  # 1MB chunks

@app.route('/<path:filename>')
def download_file(filename):
    file_path = os.path.join(SHARE_DIR, filename)
    
    if not os.path.exists(file_path):
        return "File not found", 404
    
    # Get file info
    file_size = os.path.getsize(file_path)
    mimetype = mimetypes.guess_type(filename)[0] or 'application/octet-stream'
    
    # Handle range requests for better streaming
    range_header = request.headers.get('Range', None)
    if range_header:
        byte_start = 0
        byte_end = file_size - 1
        
        # Parse range header
        if range_header.startswith('bytes='):
            range_match = range_header[6:].split('-')
            if range_match[0]:
                byte_start = int(range_match[0])
            if range_match[1]:
                byte_end = int(range_match[1])
        
        # Ensure valid range
        byte_start = max(0, byte_start)
        byte_end = min(file_size - 1, byte_end)
        content_length = byte_end - byte_start + 1
        
        def generate_partial():
            with open(file_path, 'rb') as f:
                f.seek(byte_start)
                remaining = content_length
                while remaining:
                    chunk_size = min(BUFFER_SIZE, remaining)
                    data = f.read(chunk_size)
                    if not data:
                        break
                    remaining -= len(data)
                    yield data
        
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
    
    # Full file download with streaming
    def generate_full():
        with open(file_path, 'rb') as f:
            while True:
                data = f.read(BUFFER_SIZE)
                if not data:
                    break
                yield data
    
    response = Response(
        generate_full(),
        headers={
            'Content-Length': str(file_size),
            'Content-Type': mimetype,
            'Accept-Ranges': 'bytes',
            'Content-Disposition': f'attachment; filename="{filename}"'
        }
    )
    return response

@app.route('/')
def list_files():
    files = []
    for f in os.listdir(SHARE_DIR):
        file_path = os.path.join(SHARE_DIR, f)
        if os.path.isfile(file_path):
            size = os.path.getsize(file_path)
            size_str = format_file_size(size)
            files.append(f'<a href="/{f}">{f}</a> ({size_str})')
    
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>File Server</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 40px; }}
            a {{ text-decoration: none; color: #007acc; }}
            a:hover {{ text-decoration: underline; }}
            .file {{ margin: 10px 0; padding: 10px; border: 1px solid #ddd; border-radius: 5px; }}
        </style>
    </head>
    <body>
        <h1>Available Files</h1>
        <div>{"</div><div>".join(f'<div class="file">{f}</div>' for f in files)}</div>
    </body>
    </html>
    """
    return html

def format_file_size(size_bytes):
    if size_bytes == 0:
        return "0B"
    size_names = ["B", "KB", "MB", "GB", "TB"]
    import math
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return f"{s} {size_names[i]}"

if __name__ == "__main__":
    # Use threaded mode for better concurrent handling
    app.run(host='0.0.0.0', port=8000, threaded=True, debug=False)
