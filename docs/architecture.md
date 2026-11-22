# System Architecture

## Overview

The Kubernetes Lab Exam project provides four web applications.

1. Student Portal
2. Research Summary
3. API Service
4. Admin Dashboard

Each application runs as a Kubernetes Deployment and is exposed internally through a ClusterIP Service.

## Request Flow

Client Browser
    |
    v
DNS / Hosts File
    |
    v
External Load Balancer or NodePort
    |
    v
NGINX Ingress Controller
    |
    +---- www.iam-589.com/ ------------> svc-portal
    |
    +---- www.iam-589.com/research ----> svc-research
    |
    +---- www.iam-589.com/api-589 -----> svc-api
    |
    +---- admin.iam-589.com/ ----------> svc-admin

## Kubernetes Components

| Component | Purpose |
|---|---|
| Namespace | Isolates project resources in exam-589 |
| Deployment | Manages application Pods |
| ConfigMap | Provides application code and templates |
| Service | Exposes applications inside the cluster |
| PersistentVolume | Provides persistent storage |
| PersistentVolumeClaim | Requests storage for applications |
| Ingress | Routes HTTP requests by host and path |

## Storage Design

Portal and Research use static PersistentVolumes backed by hostPath directories.

- Portal: /var/lib/k8s-exam/portal
- Research: /var/lib/k8s-exam/research

The storage configuration uses node affinity to the designated worker node.

This is a lab design. It does not provide shared storage or automatic storage failover.

## Application Routing

| Host | Path | Service |
|---|---|---|
| www.iam-589.com | /research | svc-research |
| www.iam-589.com | /api-589 | svc-api |
| www.iam-589.com | / | svc-portal |
| admin.iam-589.com | / | svc-admin |
