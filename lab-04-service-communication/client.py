import urllib.request
import json


ORDER_SERVICE = "http://localhost:8000"


print("================================")
print("Distributed Systems Client")
print("================================")

print()
print("Requesting an order...")
print()


try:

    with urllib.request.urlopen(
        f"{ORDER_SERVICE}/order"
    ) as response:

        data = response.read().decode("utf-8")

        order = json.loads(data)

        print(f"Status: {response.status}")
        print()

        print("Order Information")
        print("-------------------------")

        print(
            f"Order ID: "
            f"{order['order_id']}"
        )

        print(
            f"Customer: "
            f"{order['customer']['name']}"
        )

        print(
            f"Product: "
            f"{order['product']['name']}"
        )

        print(
            f"Price: "
            f"${order['product']['price']}"
        )

        print(
            f"Quantity: "
            f"{order['quantity']}"
        )

        print(
            f"Total: "
            f"${order['total']}"
        )


except Exception as error:

    print("Request failed.")
    print(f"Reason: {error}")