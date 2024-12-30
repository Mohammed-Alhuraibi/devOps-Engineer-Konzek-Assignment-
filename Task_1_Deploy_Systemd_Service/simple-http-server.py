#!/usr/bin/python3
from http.server import HTTPServer, BaseHTTPRequestHandler
import logging
import datetime
import socket

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        message = f"Hello! hostname: { socket.gethostname() } \nThe current time is: {current_time}"
        
        self.send_response(200)
        self.send_header('Content-Type', 'text/plain')
        self.end_headers()
        self.wfile.write(message.encode())
        
        # Log the request
        logger.info(f"Received request from {self.client_address[0]} for path: {self.path}")

def run_server(port=8000):
    server_address = ('', port)
    httpd = HTTPServer(server_address, SimpleHTTPRequestHandler)
    logger.info(f"Starting server on port {port}")
    httpd.serve_forever()

if __name__ == '__main__':
    run_server()