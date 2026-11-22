#!/usr/bin/env bash
set -Eeuo pipefail

NAMESPACE="exam-589"

echo "======================================"
echo " Kubernetes Lab Exam - Verification"
echo "======================================"

echo
echo "===== NODES ====="
kubectl get nodes -o wide

echo
echo "===== PODS ====="
kubectl get pods -n "$NAMESPACE" -o wide

echo
echo "===== SERVICES ====="
kubectl get svc -n "$NAMESPACE"

echo
echo "===== PVC ====="
kubectl get pvc -n "$NAMESPACE"

echo
echo "===== PV ====="
kubectl get pv

echo
echo "===== INGRESS ====="
kubectl get ingress -n "$NAMESPACE"

echo
echo "===== DEPLOYMENT STATUS ====="
kubectl get deployments -n "$NAMESPACE"

echo
echo "===== ROLLOUT STATUS ====="
for deployment in portal-589 app-research api-589 admin-589
do
    kubectl rollout status "deployment/$deployment" \
        -n "$NAMESPACE" --timeout=60s
done

echo
echo "Verification completed."
