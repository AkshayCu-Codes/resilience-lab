import requests
import time
from colorama import Fore, Style, init

init(autoreset=True)

URL = "http://localhost:8081/fetch"
STATE_URL = "http://localhost:8081/breaker-state"

previous_state = None

for i in range(1, 31):

    try:
        state_resp = requests.get(STATE_URL, timeout=2)
        cb_state = state_resp.json().get("circuit_breaker_state", "unknown")
    except Exception:
        cb_state = "unknown"

    if cb_state == "closed":
        color = Fore.GREEN
    elif cb_state == "open":
        color = Fore.RED
    elif cb_state == "half-open":
        color = Fore.YELLOW
    else:
        color = Fore.WHITE

    if cb_state != previous_state:
        print(f"{Style.BRIGHT}{color}[Circuit Breaker] Transition: {previous_state} → {cb_state}{Style.RESET_ALL}")
        previous_state = cb_state

    try:
        resp = requests.get(URL, timeout=5)
        status = resp.status_code
        data = resp.json()
    except Exception as e:
        status = "Error"
        data = str(e)

    print(f"{i}: Status: {status}, Response: {data}, CircuitBreaker: {cb_state}")
    time.sleep(0.5)
