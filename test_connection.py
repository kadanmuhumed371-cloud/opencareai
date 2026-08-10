import urllib.request
import json
import urllib.error

def test_backend():
    url = "http://127.0.0.1:8000/"
    print(f"Testing connection to {url} ...")
    try:
        response = urllib.request.urlopen(url)
        data = response.read()
        print(f"Success! Backend is reachable.")
        print(f"Status Code: {response.getcode()}")
        try:
            print(f"Response: {json.loads(data.decode('utf-8'))}")
        except json.JSONDecodeError:
            print(f"Response: {data.decode('utf-8')}")
    except urllib.error.URLError as e:
        print(f"Failed to connect to backend: {e.reason}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    test_backend()
