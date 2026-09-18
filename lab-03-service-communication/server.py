from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import sys
from datetime import datetime


DEFAULT_PORT = 8001


class RequestHandler(BaseHTTPRequestHandler):

    def send_json_response(self, data, status_code=200):
        response = json.dumps(data).encode("utf-8")

        self.send_response(status_code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(response)))
        self.end_headers()

        self.wfile.write(response)

    def do_GET(self):

        if self.path == "/":

            response = {
                "message": "Hello from the server!",
                "server": SERVER_NAME,
                "port": PORT,
                "time": datetime.now().isoformat(),
                "status": "running"
            }

            self.send_json_response(response)

        elif self.path == "/health":

            response = {
                "server": SERVER_NAME,
                "port": PORT,
                "status": "healthy"
            }

            self.send_json_response(response)

        else:

            response = {
                "error": "Endpoint not found"
            }

            self.send_json_response(response, 404)

    def log_message(self, format, *args):
        print(
            f"[{SERVER_NAME}:{PORT}] "
            f"{self.address_string()} - "
            f"{format % args}"
        )


if len(sys.argv) > 1:
    PORT = int(sys.argv[1])
else:
    PORT = DEFAULT_PORT


SERVER_NAME = f"Server-{PORT}"

server = HTTPServer(("localhost", PORT), RequestHandler)

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
    print(f"\n{SERVER_NAME} shutting down...")
    server.server_close()