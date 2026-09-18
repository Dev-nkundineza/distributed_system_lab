from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.request


SERVERS = [
    "http://localhost:8001",
    "http://localhost:8002",
    "http://localhost:8003"
]

current_server = 0


class LoadBalancerHandler(BaseHTTPRequestHandler):

    def do_GET(self):

        global current_server

        server = SERVERS[current_server]

        print(f"Forwarding request to {server}")

        current_server = (current_server + 1) % len(SERVERS)

        try:

            with urllib.request.urlopen(server + self.path) as response:

                data = response.read()

                self.send_response(response.status)

                self.send_header(
                    "Content-Type",
                    response.headers.get("Content-Type", "application/json")
                )

                self.send_header(
                    "Content-Length",
                    str(len(data))
                )

                self.end_headers()

                self.wfile.write(data)

        except Exception as error:

            print(f"Error contacting {server}: {error}")

            self.send_response(503)

            self.send_header(
                "Content-Type",
                "application/json"
            )

            self.end_headers()

            message = b'{"error": "Server unavailable"}'

            self.wfile.write(message)

    def log_message(self, format, *args):
        print(f"[Load Balancer] {format % args}")


server = HTTPServer(
    ("localhost", 8000),
    LoadBalancerHandler
)

print("---------------------------------------")
print("Distributed Systems Load Balancer")
print("---------------------------------------")
print("Port: 8000")
print("URL:  http://localhost:8000")
print("---------------------------------------")
print("Servers:")

for backend in SERVERS:
    print(f"  - {backend}")

print("---------------------------------------")
print("Press CTRL+C to stop.")
print()


try:
    server.serve_forever()

except KeyboardInterrupt:

    print("\nLoad balancer shutting down...")

    server.server_close()