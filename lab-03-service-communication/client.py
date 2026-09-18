import urllib.request
import json
import time


LOAD_BALANCER = "http://localhost:8000"


print("================================")
print("Distributed Systems Client")
print("================================")

print(f"Connecting to load balancer: {LOAD_BALANCER}")
print()


for request_number in range(1, 6):

    print(f"Request {request_number}")

    try:

        with urllib.request.urlopen(LOAD_BALANCER) as response:

            data = response.read().decode("utf-8")

            result = json.loads(data)

            print(f"Status: {response.status}")
            print(f"Server: {result['server']}")
            print(f"Port:   {result['port']}")

    except Exception as error:

        print(f"ERROR: {error}")

    print()

    time.sleep(1)