import requests
import time

url = "http://127.0.0.1:8000/ask"

for i in range(5):

    start = time.time()

    response = requests.get(url)

    end = time.time()

    print(f"Request {i+1}")
    print(response.json())
    print(f"Time Taken: {end-start:.2f} sec")
    print("-" * 30)