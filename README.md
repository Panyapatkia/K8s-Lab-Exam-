# K8s-Lab-Exam

Kubernetes Lab Examination Project

A multi-application web platform deployed on Kubernetes using Flask, ConfigMap, PersistentVolume, PersistentVolumeClaim, ClusterIP Service and NGINX Ingress.

## Student Information

- Student Name: Panyapat Sungrung
- Student ID: 68130589
- Project: Kubernetes Web Application Deployment

## Applications

| Application | Deployment | Description |
|---|---|---|
| Student Portal | portal-589 | Student profile and profile editing |
| Research | app-research | Research summary and editing |
| API Service | api-589 | Displays API message |
| Admin Dashboard | admin-589 | Links to Portal and Research editing |

## System Architecture

The project consists of four independent Flask applications running as Kubernetes Deployments.

- Portal and Research use persistent storage.
- ConfigMaps provide application code and HTML templates.
- ClusterIP Services expose applications inside the cluster.
- NGINX Ingress routes HTTP requests based on hostname and path.

See [Architecture](docs/architecture.md).

## Project Structure

```text
.
├── apps/
│   ├── portal/
│   ├── research/
│   ├── api/
│   └── admin/
├── k8s/
│   ├── 00-namespace.yaml
│   ├── 01-storage.yaml
│   ├── 02-portal-configmap.yaml
│   ├── 02-portal-templates.yaml
│   ├── 02-portal.yaml
│   ├── 03-research-configmap.yaml
│   ├── 03-research-templates.yaml
│   ├── 03-research.yaml
│   ├── 04-api-configmap.yaml
│   ├── 04-api.yaml
│   ├── 05-admin-configmap.yaml
│   ├── 05-admin-templates.yaml
│   ├── 05-admin.yaml
│   └── 06-ingress.yaml
├── scripts/
│   ├── deploy.sh
│   └── verify.sh
├── docs/
│   ├── architecture.md
│   └── deployment-guide.md
├── evidence/
│   └── screenshots/
├── .gitignore
└── README.md
```

## Prerequisites

- Kubernetes cluster
- kubectl configured with cluster access
- NGINX Ingress Controller with ingressClass `nginx`
- Worker node named `k8s-worker1`
- Static hostPath storage directories on the designated worker node
- Network access to pull container images and install Python dependencies

### Storage Requirements

The current manifests use static PersistentVolumes with hostPath.

The following directories must be prepared on `k8s-worker1`:

```bash
sudo mkdir -p /var/lib/k8s-exam/portal
sudo mkdir -p /var/lib/k8s-exam/research
```

The Portal and Research workloads are tied to the storage node. This design is intended for the lab environment and is not a highly available shared-storage architecture.

## Deployment

Clone the repository:

```bash
git clone https://github.com/Panyapatkia/K8s-Lab-Exam-.git
cd K8s-Lab-Exam-
```

Check cluster prerequisites:

```bash
kubectl get nodes
kubectl get ingressclass
```

Deploy:

```bash
chmod +x scripts/*.sh
./scripts/deploy.sh
```

Verify:

```bash
./scripts/verify.sh
```

See [Deployment Guide](docs/deployment-guide.md) for detailed instructions.

## Application URLs

Configure DNS or the client hosts file to point the following domains to the Ingress entry point:

| URL | Application |
|---|---|
| http://www.iam-589.com/ | Student Portal |
| http://www.iam-589.com/edit | Edit Student Profile |
| http://www.iam-589.com/research | Research Summary |
| http://www.iam-589.com/research/edit | Edit Research |
| http://www.iam-589.com/api-589/Hello-Kubernetes-589 | API Service |
| http://admin.iam-589.com/ | Admin Dashboard |

The Ingress Controller and external Load Balancer or NodePort access must be configured separately according to the target environment.

## Verification Commands

```bash
kubectl get pods -n exam-589 -o wide
kubectl get svc -n exam-589
kubectl get pvc -n exam-589
kubectl get pv
kubectl get ingress -n exam-589
```

## Notes and Limitations

- The manifests are designed for the lab environment.
- The namespace is `exam-589`.
- Storage uses static hostPath PersistentVolumes.
- Portal and Research require the designated storage node.
- NGINX Ingress Controller is a prerequisite and is not installed by the deployment script.
- Domain resolution and external Load Balancer configuration are environment-specific.
- Review and adjust storage paths, node affinity, domains and networking before deploying to another cluster.

## Repository

https://github.com/Panyapatkia/K8s-Lab-Exam-
