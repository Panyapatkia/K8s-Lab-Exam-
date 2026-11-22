# Deployment Guide

## 1. Requirements

- Kubernetes cluster is operational.
- kubectl can access the cluster.
- Node k8s-worker1 exists.
- NGINX Ingress Controller is installed.
- IngressClass nginx exists.
- Required hostPath storage directories are prepared on k8s-worker1.

## 2. Prepare Storage

On the designated worker node, create:

```bash
sudo mkdir -p /var/lib/k8s-exam/portal
sudo mkdir -p /var/lib/k8s-exam/research
```

Check the directories:

```bash
sudo ls -ld /var/lib/k8s-exam/portal
sudo ls -ld /var/lib/k8s-exam/research
```

## 3. Clone the Repository

```bash
git clone https://github.com/Panyapatkia/K8s-Lab-Exam-.git
cd K8s-Lab-Exam-
```

## 4. Check the Cluster

```bash
kubectl get nodes -o wide
kubectl get ingressclass
kubectl cluster-info
```

## 5. Deploy the Applications

```bash
chmod +x scripts/*.sh
./scripts/deploy.sh
```

The deployment script applies resources in this order:

1. Namespace
2. PersistentVolumes and PersistentVolumeClaims
3. Portal ConfigMaps and Deployment/Service
4. Research ConfigMaps and Deployment/Service
5. API ConfigMap and Deployment/Service
6. Admin ConfigMaps and Deployment/Service
7. Ingress

## 6. Verify Resources

```bash
./scripts/verify.sh
```

Or inspect individual resources:

```bash
kubectl get pods,svc,pvc -n exam-589
kubectl get pv
kubectl get ingress -n exam-589
```

## 7. Configure Domain Resolution

Configure DNS or the client hosts file to resolve:

- www.iam-589.com
- admin.iam-589.com

Both domains must point to the Ingress entry point.

The external Load Balancer, NodePort and DNS configuration are environment-specific and are not created by the deployment script.

## 8. Test Applications

- http://www.iam-589.com/
- http://www.iam-589.com/edit
- http://www.iam-589.com/research
- http://www.iam-589.com/research/edit
- http://www.iam-589.com/api-589/Hello-Kubernetes-589
- http://admin.iam-589.com/

## 9. Troubleshooting

Check Pods:

```bash
kubectl get pods -n exam-589 -o wide
```

Check application logs:

```bash
kubectl logs deployment/portal-589 -n exam-589
kubectl logs deployment/app-research -n exam-589
kubectl logs deployment/api-589 -n exam-589
kubectl logs deployment/admin-589 -n exam-589
```

Check Ingress:

```bash
kubectl describe ingress exam-ingress -n exam-589
```

Check storage:

```bash
kubectl get pv,pvc -n exam-589
```

## Important

The manifests are designed for the original lab environment. Before using them on another cluster, review node affinity, hostPath directories, storage capacity, ingress configuration and domain settings.
