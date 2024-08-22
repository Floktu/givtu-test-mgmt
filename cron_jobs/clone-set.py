import requests
import time
from threading import Thread


def ping_clone_first_set():
    url = "http://localhost:8741/apiv3/cron/clone-first-set"
    while True:
        try:
            response = requests.get(url)
            print(f"Pinged {url}: {response.status_code}")
            print(response.text)  # Print response body content
        except requests.exceptions.RequestException as e:
            print(f"Failed to ping {url}: {e}")
        time.sleep(5)  # Wait for 1/2 minutes


if __name__ == "__main__":
    # Create and start threads for each function
    thread1 = Thread(target=ping_clone_first_set)

    thread1.start()

    thread1.join()
