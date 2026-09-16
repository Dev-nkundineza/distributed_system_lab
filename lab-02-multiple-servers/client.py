import urllib.request
import json


SERVERS = [
    "http://localhost:8001",
    "http://localhost:8002",
    "http://localhost:8003"
]


def contact_server(server):

    print(f"\nConnecting to {server}")

    try:

        with urllib.request.urlopen(server) as response:

            data = response.read().decode("utf-8")

            result = json.loads(data)

            print(f"Status: {response.status}")
            print(f"Server: {result['server']}")
            print(f"Port:   {result['port']}")
            print(f"Status: {result['status']}")

    except Exception as error:

        print(f"ERROR: Could not contact {server}")
        print(f"Reason: {error}")


print("================================")
print("Distributed Systems Client")
print("================================")

for server in SERVERS:

    contact_server(server)