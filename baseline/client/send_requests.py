import requests
import time

URL = "http://localhost:8080/fetch"

for i in range(1, 21):
    try:
        r = requests.get(URL, timeout=5)
        print(f"{i}: Status {r.status_code}, Response: {r.json()}")
    except Exception as e:
        print(f"{i}: Exception - {e}")
    time.sleep(0.5)
