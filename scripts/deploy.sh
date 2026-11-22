#!/usr/bin/env bash
set -Eeuo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

NAMESPACE="exam-589"

echo "=========================================="
echo "  ระบบติดตั้ง Kubernetes Lab Exam"
echo "=========================================="

command -v kubectl >/dev/null 2>&1 || {
    echo "ข้อผิดพลาด: ไม่พบคำสั่ง kubectl"
    exit 1
}

echo
echo "[1/5] ตรวจสอบการเชื่อมต่อ Kubernetes Cluster"

kubectl cluster-info >/dev/null || {
    echo "ข้อผิดพลาด: ไม่สามารถเชื่อมต่อ Kubernetes Cluster ได้"
    exit 1
}

echo "เชื่อมต่อ Kubernetes Cluster สำเร็จ"

echo
echo "[2/5] ตรวจสอบ Worker Node"

kubectl get node k8s-worker1 >/dev/null || {
    echo "ข้อผิดพลาด: ไม่พบ Worker Node ชื่อ k8s-worker1"
    exit 1
}

echo "พบ Worker Node k8s-worker1"

echo
echo "[3/5] ตรวจสอบ NGINX Ingress Controller"

kubectl get ingressclass nginx >/dev/null || {
    echo "ข้อผิดพลาด: ไม่พบ IngressClass ชื่อ nginx"
    echo "กรุณาติดตั้งและกำหนดค่า NGINX Ingress Controller ก่อน"
    exit 1
}

echo "พบ IngressClass nginx"

echo
echo "[4/5] เริ่มติดตั้ง Kubernetes Resources"

echo "กำลังสร้าง Namespace..."
kubectl apply -f k8s/00-namespace.yaml

echo "กำลังสร้าง PersistentVolume และ PersistentVolumeClaim..."
kubectl apply -f k8s/01-storage.yaml

echo "กำลังติดตั้ง Student Portal..."
kubectl apply -f k8s/02-portal-configmap.yaml
kubectl apply -f k8s/02-portal-templates.yaml
kubectl apply -f k8s/02-portal.yaml

echo "กำลังติดตั้ง Research..."
kubectl apply -f k8s/03-research-configmap.yaml
kubectl apply -f k8s/03-research-templates.yaml
kubectl apply -f k8s/03-research.yaml

echo "กำลังติดตั้ง API Service..."
kubectl apply -f k8s/04-api-configmap.yaml
kubectl apply -f k8s/04-api.yaml

echo "กำลังติดตั้ง Admin Dashboard..."
kubectl apply -f k8s/05-admin-configmap.yaml
kubectl apply -f k8s/05-admin-templates.yaml
kubectl apply -f k8s/05-admin.yaml

echo "กำลังสร้าง Ingress..."
kubectl apply -f k8s/06-ingress.yaml

echo
echo "[5/5] ตรวจสอบสถานะ Deployment"

for deployment in portal-589 app-research api-589 admin-589
do
    echo "กำลังรอ Deployment: $deployment"

    kubectl rollout status "deployment/$deployment" \
        -n "$NAMESPACE" --timeout=300s
done

echo
echo "=========================================="
echo " ติดตั้งระบบเสร็จสมบูรณ์"
echo "=========================================="

echo
echo "===== สถานะ Pod, Service และ PVC ====="
kubectl get pods,svc,pvc -n "$NAMESPACE"

echo
echo "===== สถานะ Ingress ====="
kubectl get ingress -n "$NAMESPACE"

echo
echo "สามารถใช้ scripts/verify.sh เพื่อตรวจสอบระบบเพิ่มเติมได้"
