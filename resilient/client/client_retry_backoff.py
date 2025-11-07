import requests
import time
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

BACKEND_URL = "http://127.0.0.1:5000/account/123"

@retry(
    stop=stop_after_attempt(4),
    wait=wait_exponential(multiplier=0.5, min=0.5, max=10),
    retry=retry_if_exception_type(requests.exceptions.RequestException),
)
def call_backend():
    print("[Client] Sending request to backend...")
    response = requests.get(BACKEND_URL, timeout=3)
    response.raise_for_status()  
    return response.json()

def main():
    for i in range(1, 6):
        print(f"\nAttempt {i}:")
        try:
            data = call_backend()
            print(f"[Success] Response: {data}")
        except Exception as e:
            print(f"[Error] {e}")
        time.sleep(2)

if __name__ == "__main__":
    main()
