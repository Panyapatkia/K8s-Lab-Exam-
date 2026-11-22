#!/usr/bin/env bash
set -Eeuo pipefail

NAMESPACE="exam-589"

echo "=========================================="
echo " ระบบตรวจสอบ Kubernetes Lab Exam"
echo "=========================================="

echo
echo "===== 1. ตรวจสอบ Kubernetes Nodes ====="
kubectl get nodes -o wide

echo
echo "===== 2. ตรวจสอบ Pods ====="
kubectl get pods -n "$NAMESPACE" -o wide

echo
echo "===== 3. ตรวจสอบ Deployments ====="
kubectl get deployments -n "$NAMESPACE"

echo
echo "===== 4. ตรวจสอบ Services ====="
kubectl get svc -n "$NAMESPACE"

echo
echo "===== 5. ตรวจสอบ PersistentVolumeClaims ====="
kubectl get pvc -n "$NAMESPACE"

echo
echo "===== 6. ตรวจสอบ PersistentVolumes ====="
kubectl get pv

echo
echo "===== 7. ตรวจสอบ Ingress ====="
kubectl get ingress -n "$NAMESPACE"

echo
echo "===== 8. ตรวจสอบสถานะ Rollout ====="

for deployment in portal-589 app-research api-589 admin-589
do
    echo
    echo "กำลังตรวจสอบ Deployment: $deployment"

    kubectl rollout status "deployment/$deployment" \
        -n "$NAMESPACE" --timeout=60s
done

echo
echo "=========================================="
echo " การตรวจสอบระบบเสร็จสมบูรณ์"
echo "=========================================="
