from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import socket
import time
from datetime import datetime


HOST = "0.0.0.0"
PORT = 8000
## [TODO] Uncomment the following line to enable request counting
#request_count = 0

class RequestHandler(BaseHTTPRequestHandler):

    def send_json_response(self, data, status_code=200):
        response = json.dumps(data).encode("utf-8")

        self.send_response(status_code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", len(response))
        self.end_headers()

        self.wfile.write(response)

    def do_GET(self):
        
        ## [TODO] Uncomment the following lines to enable request counting
        # global request_count
        # request_count += 1

        if self.path == "/":

            response = {
                "message": "Hello from the distributed systems server!",
                "server": socket.gethostname(),
                "time": datetime.now().isoformat(),
                "status": "running",
                ## [TODO] Uncomment the line below to include the request count in the response
                #"request_number": request_count 
            }

            self.send_json_response(response)

        elif self.path == "/hello":

            response = {
                "message": "Hello, client!"
            }

            self.send_json_response(response)

        elif self.path == "/health":

            response = {
                "status": "healthy"
            }

            self.send_json_response(response)
        
        # elif self.path == "/slow":
        #     time.sleep(10)  # Simulate a slow response
        #     response = {
        #         "message": "The server took 10 seconds to respond."
        #     }

        #     self.send_json_response(response)

        else:

            response = {
                "error": "Endpoint not found"
            }

            self.send_json_response(response, 404)

    def log_message(self, format, *args):
        print(f"[SERVER] {self.address_string()} - {format % args}")


server = HTTPServer((HOST, PORT), RequestHandler)

print(f"Server is running on http://localhost:{PORT}")
print("Press CTRL+C to stop the server.")

try:
    server.serve_forever()
except KeyboardInterrupt:
    print("\nServer shutting down...")
    server.server_close()