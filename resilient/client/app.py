from flask import Flask, jsonify
import requests, os
from pybreaker import CircuitBreaker, CircuitBreakerError
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type, RetryCallState

app = Flask(__name__)
BACKEND_URL = os.environ.get("BACKEND_URL", "http://backend:5000/account/123")

# Circuit Breaker
breaker = CircuitBreaker(fail_max=int(os.environ.get("CB_FAIL_MAX", "2")),
                         reset_timeout=int(os.environ.get("CB_RESET_TIMEOUT", "10")))

def before_retry(retry_state: RetryCallState):
    print(f"[retry] attempt #{retry_state.attempt_number} after {retry_state.outcome.exception() if retry_state.outcome else 'n/a'}")

@retry(
    retry=retry_if_exception_type(requests.exceptions.RequestException),
    stop=stop_after_attempt(int(os.environ.get("RETRY_MAX_ATTEMPTS", "2"))),
    wait=wait_exponential(multiplier=0.5, min=0.5, max=10),
    before_sleep=before_retry,
    reraise=True
)
def call_backend_once():
    @breaker
    def do_call():
        resp = requests.get(BACKEND_URL, timeout=float(os.environ.get("BACKEND_TIMEOUT", "1.0")))
        resp.raise_for_status()
        return resp.json()
    return do_call()

@app.route("/fetch")
def fetch():
    try:
        data = call_backend_once()
        return jsonify({"status": "ok", "data": data})
    except CircuitBreakerError:
        return jsonify({"status": "fallback", "reason": "circuit_open", "data": None}), 503
    except requests.exceptions.RequestException as e:
        return jsonify({"status": "error", "reason": str(e)}), 502

@app.route("/breaker-state")
def breaker_state():
    state = breaker.current_state
    return jsonify({"circuit_breaker_state": str(state)})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
