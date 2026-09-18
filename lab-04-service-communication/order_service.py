from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.request
import json


PORT = 8000

USER_SERVICE = "http://localhost:8001"
PRODUCT_SERVICE = "http://localhost:8002"


def get_service_data(url):

    try:

        with urllib.request.urlopen(url) as response:

            data = response.read().decode("utf-8")

            return json.loads(data)

    except Exception as error:

        print(f"Service request failed: {error}")

        return None


class OrderServiceHandler(BaseHTTPRequestHandler):

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

        if self.path == "/order":

            print("\nReceived order request")

            # Ask User Service for user information
            print("→ Contacting User Service...")

            user = get_service_data(
                f"{USER_SERVICE}/users/1"
            )

            if user is None:

                self.send_json_response(
                    {
                        "error": "User Service unavailable"
                    },
                    503
                )

                return

            # Ask Product Service for product information
            print("→ Contacting Product Service...")

            product = get_service_data(
                f"{PRODUCT_SERVICE}/products/101"
            )

            if product is None:

                self.send_json_response(
                    {
                        "error": "Product Service unavailable"
                    },
                    503
                )

                return

            # Build the final order
            order = {

                "order_id": "ORD-001",

                "customer": user,

                "product": product,

                "quantity": 1,

                "total": product["price"]

            }

            print("✓ Order created successfully")

            self.send_json_response(order)

        elif self.path == "/health":

            self.send_json_response({
                "service": "order-service",
                "status": "healthy"
            })

        else:

            self.send_json_response(
                {"error": "Endpoint not found"},
                404
            )

    def log_message(self, format, *args):

        print(
            f"[Order Service] {format % args}"
        )


server = HTTPServer(
    ("localhost", PORT),
    OrderServiceHandler
)

print("--------------------------------")
print("Order Service")
print("--------------------------------")
print(f"Running on port {PORT}")
print(f"http://localhost:{PORT}")
print("--------------------------------")
print("Press CTRL+C to stop.")
print()


try:

    server.serve_forever()

except KeyboardInterrupt:

    print("\nOrder Service shutting down...")
    server.server_close()