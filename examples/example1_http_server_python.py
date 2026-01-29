#!/usr/bin/env python3
"""
Example 1: HTTP Server with JSON Loopback Interface (Python)

This script demonstrates a simple HTTP server running on the loopback interface (127.0.0.1)
that can handle JSON data for both text and numeric values.

Usage:
    python3 example1_http_server_python.py
    
    Then in another terminal:
    curl -X POST http://127.0.0.1:8080/data -H "Content-Type: application/json" -d '{"name":"test","value":123}'
"""

import http.server
import socketserver
import json
from urllib.parse import urlparse, parse_qs

PORT = 8080
LOOPBACK_HOST = "127.0.0.1"

# In-memory storage for JSON data
data_store = {
    "text_data": [],
    "numeric_data": []
}

class JSONLoopbackHandler(http.server.BaseHTTPRequestHandler):
    
    def do_GET(self):
        """Handle GET requests to retrieve stored JSON data"""
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        
        # Return all stored data as JSON
        response = {
            "status": "success",
            "data": data_store,
            "loopback_interface": LOOPBACK_HOST,
            "port": PORT
        }
        self.wfile.write(json.dumps(response, indent=2).encode())
    
    def do_POST(self):
        """Handle POST requests to store JSON data"""
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        
        try:
            # Parse JSON data
            json_data = json.loads(post_data.decode('utf-8'))
            
            # Categorize data by type
            if isinstance(json_data.get('value'), str):
                data_store['text_data'].append(json_data)
            elif isinstance(json_data.get('value'), (int, float)):
                data_store['numeric_data'].append(json_data)
            else:
                data_store['text_data'].append(json_data)
            
            self.send_response(201)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            
            response = {
                "status": "success",
                "message": "Data stored successfully",
                "received": json_data
            }
            self.wfile.write(json.dumps(response, indent=2).encode())
            
        except json.JSONDecodeError as e:
            self.send_response(400)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            
            response = {
                "status": "error",
                "message": f"Invalid JSON: {str(e)}"
            }
            self.wfile.write(json.dumps(response).encode())
    
    def log_message(self, format, *args):
        """Custom log message to show loopback interface"""
        print(f"[{LOOPBACK_HOST}:{PORT}] {format % args}")

if __name__ == "__main__":
    with socketserver.TCPServer((LOOPBACK_HOST, PORT), JSONLoopbackHandler) as httpd:
        print(f"JSON Loopback Server running on http://{LOOPBACK_HOST}:{PORT}")
        print(f"Listening only on loopback interface (localhost)")
        print(f"\nTry these commands:")
        print(f"  curl http://{LOOPBACK_HOST}:{PORT}/data")
        print(f"  curl -X POST http://{LOOPBACK_HOST}:{PORT}/data -H 'Content-Type: application/json' -d '{{\"name\":\"test\",\"value\":123}}'")
        print(f"  curl -X POST http://{LOOPBACK_HOST}:{PORT}/data -H 'Content-Type: application/json' -d '{{\"name\":\"hello\",\"value\":\"world\"}}'")
        print("\nPress Ctrl+C to stop the server")
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nServer stopped")
