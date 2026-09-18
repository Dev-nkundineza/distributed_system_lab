from http.server import BaseHTTPRequestHandler, HTTPServer
import json


PORT = 8002

PRODUCTS = {
    "101": {
        "id": "101",
        "name": "Laptop",
        "price": 1200
    },
    "102": {
        "id": "102",
        "name": "Keyboard",
        "price": 80
    },
    "103": {
        "id": "103",
        "name": "Mouse",
        "price": 40
    }
}


class ProductServiceHandler(BaseHTTPRequestHandler):

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

        if self.path.startswith("/products/"):

            product_id = self.path.split("/")[-1]

            product = PRODUCTS.get(product_id)

            if product:

                self.send_json_response(product)

            else:

                self.send_json_response(
                    {"error": "Product not found"},
                    404
                )

        elif self.path == "/health":

            self.send_json_response({
                "service": "product-service",
                "status": "healthy"
            })

        else:

            self.send_json_response(
                {"error": "Endpoint not found"},
                404
            )

    def log_message(self, format, *args):

        print(
            f"[Product Service] {format % args}"
        )


server = HTTPServer(
    ("localhost", PORT),
    ProductServiceHandler
)

print("--------------------------------")
print("Product Service")
print("--------------------------------")
print(f"Running on port {PORT}")
print(f"http://localhost:{PORT}")
print("--------------------------------")
print("Press CTRL+C to stop.")
print()


try:

    server.serve_forever()

except KeyboardInterrupt:

    print("\nProduct Service shutting down...")
    server.server_close()