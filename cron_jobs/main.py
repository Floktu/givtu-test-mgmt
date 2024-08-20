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
        time.sleep(30)  # Wait for 1/2 minutes


# def ping_clone_fortune_draw():
#     url = "https://gamedev.givtu.com/apiv3/cron/clone-fortune-draw"
#     while True:
#         try:
#             response = requests.get(url)
#             print(f"Pinged {url}: {response.status_code}")
#             print(response.text)  # Print response body content
#         except requests.exceptions.RequestException as e:
#             print(f"Failed to ping {url}: {e}")
#         time.sleep(1800)  # Wait for 30 minutes

# def ping_subscriptions():
#     url = "http://localhost:8741/process-subscription/5"
#     while True:
#         try:
#             response = requests.get(url)
#             print(f"Pinged {url}: {response.status_code}")
#             print(response.text)  # Print response body content
#         except requests.exceptions.RequestException as e:
#             print(f"Failed to ping {url}: {e}")
#         time.sleep(1800)  # Wait for 30 minutes


if __name__ == "__main__":
    # Create and start threads for each function
    thread1 = Thread(target=ping_clone_first_set)
    # thread2 = Thread(target=ping_clone_fortune_draw)
    # thread3 = Thread(target=ping_subscriptions)
    thread1.start()
    # thread2.start()
    # thread3.start()

    thread1.join()
    # thread2.join()
    # thread3.join()
