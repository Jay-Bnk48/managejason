#!/usr/bin/env node
/**
 * Example 2: HTTP Server with JSON Loopback Interface (Node.js)
 * 
 * This script demonstrates an HTTP server running on the loopback interface (127.0.0.1)
 * that handles JSON data including text, numbers, arrays, and objects.
 * 
 * Usage:
 *     node example2_http_server_nodejs.js
 *     
 *     Then in another terminal:
 *     curl -X POST http://127.0.0.1:3000/json -H "Content-Type: application/json" -d '{"id":1,"text":"sample","count":42}'
 */

const http = require('http');

const LOOPBACK_HOST = '127.0.0.1';
const PORT = 3000;

// In-memory storage for JSON data
const dataStore = {
    items: [],
    stats: {
        totalRequests: 0,
        textItems: 0,
        numericItems: 0,
        objectItems: 0
    }
};

/**
 * Categorize JSON data by type
 */
function categorizeData(data) {
    if (typeof data === 'string') return 'text';
    if (typeof data === 'number') return 'numeric';
    if (Array.isArray(data)) return 'array';
    if (typeof data === 'object') return 'object';
    return 'unknown';
}

/**
 * Handle HTTP requests
 */
const server = http.createServer((req, res) => {
    dataStore.stats.totalRequests++;
    
    // CORS headers for loopback interface only
    res.setHeader('Access-Control-Allow-Origin', 'http://127.0.0.1');
    res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
    res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
    
    // Handle OPTIONS request
    if (req.method === 'OPTIONS') {
        res.writeHead(200);
        res.end();
        return;
    }
    
    // GET - Retrieve all stored JSON data
    if (req.method === 'GET' && req.url === '/json') {
        res.writeHead(200, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({
            status: 'success',
            loopback_interface: LOOPBACK_HOST,
            port: PORT,
            data: dataStore
        }, null, 2));
        return;
    }
    
    // POST - Store JSON data
    if (req.method === 'POST' && req.url === '/json') {
        let body = '';
        const MAX_BODY_SIZE = 1024 * 1024; // 1MB limit
        
        req.on('data', chunk => {
            body += chunk.toString();
            
            // Check body size limit
            if (body.length > MAX_BODY_SIZE) {
                res.writeHead(413, { 'Content-Type': 'application/json' });
                res.end(JSON.stringify({
                    status: 'error',
                    message: 'Request body too large (max 1MB)'
                }));
                req.connection.destroy();
            }
        });
        
        req.on('end', () => {
            try {
                const jsonData = JSON.parse(body);
                const dataType = categorizeData(jsonData);
                
                // Store the data with metadata
                const item = {
                    id: dataStore.items.length + 1,
                    type: dataType,
                    data: jsonData,
                    timestamp: new Date().toISOString()
                };
                
                dataStore.items.push(item);
                
                // Update stats
                if (dataType === 'text') dataStore.stats.textItems++;
                else if (dataType === 'numeric') dataStore.stats.numericItems++;
                else if (dataType === 'object') dataStore.stats.objectItems++;
                
                res.writeHead(201, { 'Content-Type': 'application/json' });
                res.end(JSON.stringify({
                    status: 'success',
                    message: 'JSON data stored via loopback interface',
                    item: item
                }, null, 2));
                
                console.log(`[${LOOPBACK_HOST}:${PORT}] Stored ${dataType} data: ${JSON.stringify(jsonData)}`);
                
            } catch (error) {
                res.writeHead(400, { 'Content-Type': 'application/json' });
                res.end(JSON.stringify({
                    status: 'error',
                    message: 'Invalid JSON',
                    error: error.message
                }));
            }
        });
        return;
    }
    
    // 404 - Not found
    res.writeHead(404, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify({
        status: 'error',
        message: 'Endpoint not found'
    }));
});

// Bind to loopback interface only
server.listen(PORT, LOOPBACK_HOST, () => {
    console.log(`JSON Loopback Server running on http://${LOOPBACK_HOST}:${PORT}`);
    console.log(`Listening only on loopback interface (localhost)`);
    console.log(`\nTry these commands:`);
    console.log(`  curl http://${LOOPBACK_HOST}:${PORT}/json`);
    console.log(`  curl -X POST http://${LOOPBACK_HOST}:${PORT}/json -H "Content-Type: application/json" -d '{"text":"hello","number":123}'`);
    console.log(`  curl -X POST http://${LOOPBACK_HOST}:${PORT}/json -H "Content-Type: application/json" -d '{"array":[1,2,3],"nested":{"key":"value"}}'`);
    console.log(`\nPress Ctrl+C to stop the server`);
});

// Graceful shutdown
process.on('SIGINT', () => {
    console.log('\nServer stopped');
    process.exit(0);
});
