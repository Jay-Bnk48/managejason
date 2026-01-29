#!/usr/bin/env python3
"""
Example 3: Socket-based JSON Loopback Interface (Python)

This script demonstrates a TCP socket server running on the loopback interface (127.0.0.1)
that receives JSON data, processes it, and sends back responses. It uses raw sockets
instead of HTTP for lower-level network communication.

Usage:
    python3 example3_socket_loopback_python.py
    
    Then in another terminal:
    python3 -c "import socket, json; s=socket.socket(); s.connect(('127.0.0.1', 9999)); s.send(json.dumps({'type':'text','value':'hello'}).encode()+b'\n'); print(s.recv(1024).decode()); s.close()"
"""

import socket
import json
import threading
from datetime import datetime

LOOPBACK_HOST = "127.0.0.1"
PORT = 9999

# In-memory storage
json_storage = {
    "text_entries": [],
    "numeric_entries": [],
    "mixed_entries": []
}

def process_json_data(data):
    """Process incoming JSON data and categorize it"""
    try:
        json_obj = json.loads(data)
        
        # Add timestamp
        json_obj['received_at'] = datetime.now().isoformat()
        json_obj['loopback_interface'] = LOOPBACK_HOST
        
        # Categorize based on content
        if 'value' in json_obj:
            value = json_obj['value']
            if isinstance(value, str):
                json_storage['text_entries'].append(json_obj)
                category = 'text'
            elif isinstance(value, (int, float)):
                json_storage['numeric_entries'].append(json_obj)
                category = 'numeric'
            else:
                json_storage['mixed_entries'].append(json_obj)
                category = 'mixed'
        else:
            json_storage['mixed_entries'].append(json_obj)
            category = 'mixed'
        
        # Create response
        response = {
            "status": "success",
            "category": category,
            "stored_count": len(json_storage[f'{category}_entries']),
            "total_items": sum(len(v) for v in json_storage.values())
        }
        
        return json.dumps(response)
        
    except json.JSONDecodeError as e:
        return json.dumps({
            "status": "error",
            "message": f"Invalid JSON: {str(e)}"
        })

def handle_client(client_socket, client_address):
    """Handle individual client connections"""
    print(f"[{LOOPBACK_HOST}:{PORT}] New connection from {client_address}")
    
    try:
        # Receive data with size limit (1MB max)
        MAX_DATA_SIZE = 1024 * 1024
        data = b""
        while len(data) < MAX_DATA_SIZE:
            chunk = client_socket.recv(1024)
            if not chunk:
                break
            data += chunk
            # Check for newline delimiter
            if b'\n' in data:
                break
        
        if len(data) >= MAX_DATA_SIZE:
            error_response = json.dumps({
                "status": "error",
                "message": "Request too large (max 1MB)"
            })
            try:
                client_socket.send((error_response + '\n').encode('utf-8'))
            except:
                pass
            return
        
        if data:
            request = data.decode('utf-8').strip()
            print(f"[{LOOPBACK_HOST}:{PORT}] Received: {request}")
            
            # Process JSON
            response = process_json_data(request)
            
            # Send response
            client_socket.send((response + '\n').encode('utf-8'))
            print(f"[{LOOPBACK_HOST}:{PORT}] Sent: {response}")
    
    except Exception as e:
        error_response = json.dumps({
            "status": "error",
            "message": str(e)
        })
        try:
            client_socket.send((error_response + '\n').encode('utf-8'))
        except:
            pass  # Socket may already be closed
    
    finally:
        client_socket.close()

def start_server():
    """Start the socket server on loopback interface"""
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    # Bind to loopback interface only
    server_socket.bind((LOOPBACK_HOST, PORT))
    server_socket.listen(5)
    
    print(f"JSON Socket Loopback Server running on {LOOPBACK_HOST}:{PORT}")
    print(f"Listening only on loopback interface (localhost)")
    print(f"\nExample client code:")
    print(f"  python3 -c \"import socket, json; s=socket.socket(); s.connect(('{LOOPBACK_HOST}', {PORT})); s.send(json.dumps({{'type':'text','value':'hello'}}).encode()+b'\\\\n'); print(s.recv(1024).decode()); s.close()\"")
    print(f"\nOr create a client script:")
    print(f"  import socket, json")
    print(f"  s = socket.socket()")
    print(f"  s.connect(('{LOOPBACK_HOST}', {PORT}))")
    print(f"  s.send(json.dumps({{'value': 42}}).encode() + b'\\\\n')")
    print(f"  print(s.recv(1024).decode())")
    print(f"  s.close()")
    print("\nPress Ctrl+C to stop the server\n")
    
    try:
        while True:
            client_socket, client_address = server_socket.accept()
            # Handle each client in a separate thread
            client_thread = threading.Thread(
                target=handle_client,
                args=(client_socket, client_address)
            )
            client_thread.daemon = True
            client_thread.start()
    
    except KeyboardInterrupt:
        print("\nServer stopped")
    finally:
        server_socket.close()
        
        # Print final statistics
        print(f"\nFinal Statistics:")
        print(f"  Text entries: {len(json_storage['text_entries'])}")
        print(f"  Numeric entries: {len(json_storage['numeric_entries'])}")
        print(f"  Mixed entries: {len(json_storage['mixed_entries'])}")
        print(f"  Total: {sum(len(v) for v in json_storage.values())}")

if __name__ == "__main__":
    start_server()
