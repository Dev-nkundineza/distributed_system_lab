import urllib.request
import json


SERVER = "http://localhost:8000"


def send_request(endpoint):

    url = SERVER + endpoint

    print(f"\nSending request to: {url}")

    try:
        with urllib.request.urlopen(url) as response:

            data = response.read().decode("utf-8")

            print(f"Status code: {response.status}")
            print("Response:")

            result = json.loads(data)

            for key, value in result.items():
                print(f"  {key}: {value}")

    except Exception as error:

        print(f"Request failed: {error}")


print("Distributed Systems Client")
print("---------------------------")

send_request("/")
send_request("/hello")
send_request("/health")