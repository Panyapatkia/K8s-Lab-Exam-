#!/usr/bin/env bash
set -Eeuo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

NAMESPACE="exam-589"

echo "======================================"
echo " Kubernetes Lab Exam - Deployment"
echo "======================================"

command -v kubectl >/dev/null 2>&1 || {
    echo "ERROR: kubectl is not installed."
    exit 1
}

kubectl cluster-info >/dev/null || {
    echo "ERROR: Cannot access Kubernetes cluster."
    exit 1
}

echo
echo "[1/5] Checking worker node..."

kubectl get node k8s-worker1 >/dev/null || {
    echo "ERROR: Required node k8s-worker1 was not found."
    exit 1
}

echo
echo "[2/5] Checking NGINX Ingress Class..."

kubectl get ingressclass nginx >/dev/null || {
    echo "ERROR: NGINX Ingress Class 'nginx' was not found."
    echo "Install/configure NGINX Ingress Controller first."
    exit 1
}

echo
echo "[3/5] Applying namespace and storage..."

kubectl apply -f k8s/00-namespace.yaml
kubectl apply -f k8s/01-storage.yaml

echo
echo "[4/5] Applying application resources..."

for file in \
    k8s/02-portal-configmap.yaml \
    k8s/02-portal-templates.yaml \
    k8s/02-portal.yaml \
    k8s/03-research-configmap.yaml \
    k8s/03-research-templates.yaml \
    k8s/03-research.yaml \
    k8s/04-api-configmap.yaml \
    k8s/04-api.yaml \
    k8s/05-admin-configmap.yaml \
    k8s/05-admin-templates.yaml \
    k8s/05-admin.yaml \
    k8s/06-ingress.yaml
do
    echo "Applying: $file"
    kubectl apply -f "$file"
done

echo
echo "[5/5] Waiting for Deployments..."

for deployment in portal-589 app-research api-589 admin-589
do
    kubectl rollout status "deployment/$deployment" \
        -n "$NAMESPACE" --timeout=300s
done

echo
echo "======================================"
echo " Deployment completed"
echo "======================================"

kubectl get pods,svc,pvc -n "$NAMESPACE"
kubectl get ingress -n "$NAMESPACE"
