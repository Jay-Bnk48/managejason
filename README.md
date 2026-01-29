# managejason
handle jason

## JSON Loopback Interface Examples

This repository contains example scripts demonstrating loopback interfaces for JSON data management. These examples show how to set up servers that listen only on the loopback interface (127.0.0.1/localhost) to handle JSON data including text, numbers, arrays, and objects.

### What is a Loopback Interface?

A loopback interface is a virtual network interface that allows network connections to the local machine only. It uses the IP address 127.0.0.1 (IPv4) or ::1 (IPv6), commonly referred to as "localhost". This is useful for:
- Testing network applications locally
- Secure local-only communication
- Development and debugging
- Inter-process communication on the same machine

### Examples

#### Example 1: HTTP Server with JSON Loopback (Python)
**File:** `examples/example1_http_server_python.py`

A Python-based HTTP server that handles JSON data on the loopback interface. Supports both GET and POST requests.

**Features:**
- Stores text and numeric JSON data separately
- RESTful API design
- Port: 8080

**Usage:**
```bash
# Start the server
python3 examples/example1_http_server_python.py

# In another terminal, test it:
curl http://127.0.0.1:8080/data
curl -X POST http://127.0.0.1:8080/data -H "Content-Type: application/json" -d '{"name":"test","value":123}'
curl -X POST http://127.0.0.1:8080/data -H "Content-Type: application/json" -d '{"name":"hello","value":"world"}'
```

#### Example 2: HTTP Server with JSON Loopback (Node.js)
**File:** `examples/example2_http_server_nodejs.js`

A Node.js-based HTTP server with JSON handling capabilities, including statistics tracking.

**Features:**
- Categorizes data by type (text, numeric, array, object)
- Tracks request statistics
- CORS support for local development
- Port: 3000

**Usage:**
```bash
# Start the server
node examples/example2_http_server_nodejs.js

# In another terminal, test it:
curl http://127.0.0.1:3000/json
curl -X POST http://127.0.0.1:3000/json -H "Content-Type: application/json" -d '{"text":"hello","number":123}'
curl -X POST http://127.0.0.1:3000/json -H "Content-Type: application/json" -d '{"array":[1,2,3],"nested":{"key":"value"}}'
```

#### Example 3: Socket-based JSON Loopback (Python)
**File:** `examples/example3_socket_loopback_python.py`

A low-level TCP socket server that handles JSON data using raw sockets instead of HTTP.

**Features:**
- Direct TCP socket communication
- Multi-threaded client handling
- JSON data categorization
- Port: 9999

**Usage:**
```bash
# Start the server
python3 examples/example3_socket_loopback_python.py

# In another terminal, test it with Python:
python3 -c "import socket, json; s=socket.socket(); s.connect(('127.0.0.1', 9999)); s.send(json.dumps({'type':'text','value':'hello'}).encode()+b'\n'); print(s.recv(1024).decode()); s.close()"

# Or create a simple client script:
python3 -c "import socket, json; s=socket.socket(); s.connect(('127.0.0.1', 9999)); s.send(json.dumps({'value': 42}).encode()+b'\n'); print(s.recv(1024).decode()); s.close()"
```

### Requirements

- **Python examples**: Python 3.6 or higher (uses only standard library)
- **Node.js example**: Node.js 10.0 or higher (uses only built-in modules)

No external dependencies required - all examples use standard libraries only.

### Security Note

These servers are configured to listen **only** on the loopback interface (127.0.0.1), which means they are not accessible from other machines on the network. This is intentional for security and is appropriate for local development and testing.
