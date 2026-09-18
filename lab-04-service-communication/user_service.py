from http.server import BaseHTTPRequestHandler, HTTPServer
import json


PORT = 8001

USERS = {
    "1": {
        "id": "1",
        "name": "Alice",
        "email": "alice@example.com"
    },
    "2": {
        "id": "2",
        "name": "Bob",
        "email": "bob@example.com"
    },
    "3": {
        "id": "3",
        "name": "Charlie",
        "email": "charlie@example.com"
    }
}


class UserServiceHandler(BaseHTTPRequestHandler):

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

        if self.path.startswith("/users/"):

            user_id = self.path.split("/")[-1]

            user = USERS.get(user_id)

            if user:

                self.send_json_response(user)

            else:

                self.send_json_response(
                    {"error": "User not found"},
                    404
                )

        elif self.path == "/health":

            self.send_json_response({
                "service": "user-service",
                "status": "healthy"
            })

        else:

            self.send_json_response(
                {"error": "Endpoint not found"},
                404
            )

    def log_message(self, format, *args):

        print(
            f"[User Service] {format % args}"
        )


server = HTTPServer(
    ("localhost", PORT),
    UserServiceHandler
)

print("--------------------------------")
print("User Service")
print("--------------------------------")
print(f"Running on port {PORT}")
print(f"http://localhost:{PORT}")
print("--------------------------------")
print("Press CTRL+C to stop.")
print()


try:

    server.serve_forever()

except KeyboardInterrupt:

    print("\nUser Service shutting down...")
    server.server_close()