# -------------------------------------------
# Minikube + Kubernetes Deployment Script
# -------------------------------------------

# Step 1: Point Docker CLI to Minikube
Write-Host "`n[1/8] Setting Docker environment to Minikube..."
& minikube -p minikube docker-env --shell powershell | Invoke-Expression

# Step 2: Build Docker images
Write-Host "`n[2/8] Building Docker images..."
docker build -t baseline-backend ./baseline/backend
docker build -t baseline-client ./baseline/client
docker build -t resilient-backend ./resilient/backend
docker build -t resilient-client ./resilient/client

# Step 3: Delete old deployments and services
Write-Host "`n[3/8] Deleting old deployments and services..."
kubectl delete deploy baseline-backend baseline-client resilient-backend resilient-client -n default --ignore-not-found
kubectl delete svc baseline-backend baseline-client resilient-backend resilient-client -n default --ignore-not-found

# Step 4: Apply new baseline deployments & services
Write-Host "`n[4/8] Applying baseline deployments & services..."
kubectl apply -f ./k8s/baseline/

# Step 5: Apply new resilient deployments & services
Write-Host "`n[5/8] Applying resilient deployments & services..."
kubectl apply -f ./k8s/resilient/

# Step 6: Wait for all pods to be ready
Write-Host "`n[6/8] Waiting for pods to be ready..."
kubectl wait --for=condition=ready pod -l app=baseline-backend --timeout=120s
kubectl wait --for=condition=ready pod -l app=baseline-client --timeout=120s
kubectl wait --for=condition=ready pod -l app=resilient-backend --timeout=120s
kubectl wait --for=condition=ready pod -l app=resilient-client --timeout=120s

# Step 7: List pods and services
Write-Host "`n[7/8] Current pods:"
kubectl get pods
Write-Host "`nServices:"
kubectl get svc

# Step 8: Port-forward clients (open in new terminal if needed)
Write-Host "`n[8/8] You can port-forward clients manually:"
Write-Host "Baseline client -> kubectl port-forward svc/baseline-client 8080:80"
Write-Host "Resilient client -> kubectl port-forward svc/resilient-client 8081:80"

Write-Host "`nDeployment complete! Test clients with curl or browser."
