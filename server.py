#!/usr/bin/env python3
"""
Enhanced HTTP server that serves static files and provides image list API
"""
import http.server
import socketserver
import json
import os
from pathlib import Path
from urllib.parse import urlparse, parse_qs

PORT = 8001
IMAGE_FOLDER = "image"

class CustomHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        # Parse the URL
        parsed_path = urlparse(self.path)
        
        # API endpoint to list images
        if parsed_path.path == '/api/images':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            # Get all image files from image folder
            image_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.webp'}
            image_files = []
            
            image_path = Path(IMAGE_FOLDER)
            if image_path.exists():
                for file in image_path.iterdir():
                    if file.is_file() and file.suffix.lower() in image_extensions:
                        image_files.append(f"{IMAGE_FOLDER}/{file.name}")
            
            response = {
                'success': True,
                'images': image_files,
                'count': len(image_files)
            }
            
            self.wfile.write(json.dumps(response, ensure_ascii=False).encode('utf-8'))
        else:
            # Serve static files normally
            super().do_GET()

if __name__ == '__main__':
    with socketserver.TCPServer(("", PORT), CustomHandler) as httpd:
        print(f"Server running at http://localhost:{PORT}/")
        print(f"Image API available at http://localhost:{PORT}/api/images")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down server...")
            httpd.shutdown()

