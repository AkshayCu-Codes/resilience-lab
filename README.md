# Lab 3: Designing for Resilience and Observability  

## Overview
This lab focuses on applying resilience design patterns and chaos engineering to distributed systems deployed on Kubernetes.  
The goal is to ensure applications can gracefully handle failures, self-heal, and maintain availability under adverse conditions.

Through this lab, the following were achieved:
- Implemented Circuit Breaker and Retry with Exponential Backoff + Jitter
- Conducted Chaos Engineering Experiments using the Chaos Toolkit
- Quantitatively measured improvements in availability, latency, and recovery time

## Architecture Overview
The system consists of two microservices:
- ClientService — makes REST API calls to the backend
- BackendService — randomly introduces latency or HTTP 500 failures to simulate instability

Both are containerized and deployed on Kubernetes, with defined Deployment and Service YAMLs.


## Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/<your-username>/resilience-lab.git
cd resilience-lab
```

### 2. Build and Push Docker Images
```bash
docker build -t client-service ./client
docker build -t backend-service ./backend
```

### 3. Deploy to Kubernetes
```bash
kubectl apply -f k8s/backend-deployment.yaml
kubectl apply -f k8s/client-deployment.yaml
kubectl get pods
```

### 4. Verify Communication
Access ClientService via NodePort or port-forwarding:
```bash
kubectl port-forward svc/client-service 8080:80
```

## Lab Tasks & Experiments

### Part A: Baseline
- Deployed ClientService and BackendService without resilience mechanisms.
- Observed client timeouts, blocked threads, and unavailable responses during backend delays.

### Part B: Implementing Resilience Patterns
#### Circuit Breaker
- Integrated circuit breaker using pybreaker-style logic.
- Config: fail_max=2, reset_timeout=10s
- Behavior:
  - Opens after 2 consecutive failures  
  - Returns fallback immediately (fast-fail)  
  - Half-opens after 10s and recovers automatically  

#### Retries with Exponential Backoff + Jitter
- Used for transient errors (HTTP 500 / 429)
- Config: base delay = 100ms, max retries = 5, jitter ±20%
- Result: reduced request storming, improved transient recovery.

### Part C: Chaos Engineering
- Tool: Chaos Toolkit
- Experiment: Terminate backend pod (kill pod) while ClientService is active.
- Command:
```bash
chaos run chaos/experiment_kill_backend.json
```

#### Observations:
- Backend pod killed → circuit breaker opened in 5s  
- Client returned fallback instantly (50ms)  
- System auto-recovered when pod restarted (in ~16s)

## Key Results

| Metric | Without Resilience | With Resilience | Improvement |
|--------|--------------------|----------------|-------------|
| Availability | 70% | 100% (degraded) | +43% |
| Avg. Response Time | 30s | 2.8s | 99% faster |
| Recovery Time | 5–10 min (manual) | 16s (auto) | 96% faster |

## Unexpected Observations
1. Circuit Breaker Flapping – High failure rates caused oscillation  
   → Fixed with sliding window threshold  
2. Pod Restart vs Circuit Reset Mismatch – Timeout too short  
   → Adjusted reset timeout dynamically  
3. Retry Storm During Recovery – Surge in traffic after restart  
   → Added gradual traffic ramp-up  

## Connecting Theory to Practice

| Principle | Validation |
|------------|-------------|
| CAP Theorem | Chose AP → prioritized availability & partition tolerance over consistency |
| Failure Mode Patterns | Matched resilience pattern per failure type (fail-stop → circuit breaker, fail-slow → backoff) |
| End-to-End Principle | Application-layer resilience > network retries (context-aware) |

Insight:  
No single resilience mechanism fits all — effectiveness depends on matching failure semantics to recovery strategy.

## Conclusion
The lab demonstrated how resilient distributed architectures can transform failure handling from reactive to proactive.  
Chaos experiments confirmed that resilience mechanisms like circuit breakers and exponential backoff significantly enhance availability, fault tolerance, and user experience.  
By quantifying performance improvements and linking them to distributed systems theory, this lab bridges the gap between conceptual principles and practical fault-tolerant design.



## Author
Akshay Channapla Udaya Kumar  

