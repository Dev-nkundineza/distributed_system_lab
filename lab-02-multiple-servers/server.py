from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import socket
import sys
import time
from datetime import datetime


# --------------------------------------------------
# Configuration
# --------------------------------------------------

DEFAULT_PORT = 8001


# --------------------------------------------------
# Server identity
# --------------------------------------------------

SERVER_NAME = socket.gethostname()


# --------------------------------------------------
# Request handler
# --------------------------------------------------

class RequestHandler(BaseHTTPRequestHandler):

    def send_json_response(self, data, status_code=200):

        response = json.dumps(data).encode("utf-8")

        self.send_response(status_code)

        self.send_header(
            "Content-Type",
            "application/json"
        )

        self.send_header(
            "Content-Length",
            str(len(response))
        )

        self.end_headers()

        self.wfile.write(response)

    def do_GET(self):

        if self.path == "/":

            response = {
                "message": "Hello from a distributed server!",
                "server": SERVER_NAME,
                "port": PORT,
                "time": datetime.now().isoformat(),
                "status": "running"
            }

            self.send_json_response(response)

        elif self.path == "/hello":

            response = {
                "message": "Hello, client!",
                "server": SERVER_NAME,
                "port": PORT
            }

            self.send_json_response(response)

        elif self.path == "/health":

            response = {
                "status": "healthy",
                "server": SERVER_NAME,
                "port": PORT
            }

            self.send_json_response(response)

        elif self.path == "/slow":
            time.sleep(5)
            response = {
                "message": "This server intentionally responds slowly.",
                "server": SERVER_NAME,
                "port": PORT
                }
            self.send_json_response(response)

        else:

            response = {
                "error": "Endpoint not found"
            }

            self.send_json_response(
                response,
                status_code=404
            )

    def log_message(self, format, *args):

        print(
            f"[Server:{PORT}] "
            f"{self.address_string()} - "
            f"{format % args}"
        )


# --------------------------------------------------
# Read port from command line
# --------------------------------------------------

if len(sys.argv) > 1:

    PORT = int(sys.argv[1])

else:

    PORT = DEFAULT_PORT


# --------------------------------------------------
# Start server
# --------------------------------------------------

server = HTTPServer(
    ("localhost", PORT),
    RequestHandler
)

print("---------------------------------------")
print("Distributed Systems Server")
print("---------------------------------------")
print(f"Server: {SERVER_NAME}")
print(f"Port:   {PORT}")
print(f"URL:    http://localhost:{PORT}")
print("---------------------------------------")
print("Press CTRL+C to stop the server.")
print()

try:

    server.serve_forever()

except KeyboardInterrupt:

    print("\nServer shutting down...")

    server.server_close()