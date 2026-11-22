# Kubernetes Lab Exam

ระบบเว็บแอปพลิเคชันบน Kubernetes ประกอบด้วย 4 แอปพลิเคชัน พัฒนาด้วย Python Flask และบริหารจัดการผ่าน Kubernetes Deployment, Service, ConfigMap, PersistentVolume, PersistentVolumeClaim และ NGINX Ingress

## 1. ข้อมูลผู้จัดทำ

- ชื่อ-นามสกุล: Panyapat Sungrung
- รหัสนักศึกษา: 68130589
## 3. รายละเอียดระบบ

ประกอบด้วย 4 แอปพลิเคชัน ดังนี้

| แอปพลิเคชัน | Kubernetes Deployment | รายละเอียด |
|---|---|---|
| Student Portal | portal-589 | หน้าแสดงข้อมูลนักศึกษาและแก้ไขข้อมูลส่วนตัว |
| Research | app-research | หน้าแสดงบทสรุปงานวิจัยและแก้ไขข้อมูล |
| API Service | api-589 | บริการ API สำหรับแสดงข้อความตาม URL ที่เรียกใช้งาน |
| Admin Dashboard | admin-589 | หน้าสำหรับผู้ดูแลระบบ พร้อมลิงก์ไปยังหน้าแก้ไขข้อมูล |

ชื่อและหน้าที่ของแต่ละ Application
ลำดับ	URL / Path	ชื่อ Application	Deployment Name	หน้าที่
1	www.iam-589.com/	Student Portal	portal-589	แสดงรูปภาพ ชื่อ และรหัสนักศึกษา
2	www.iam-589.com/research	Research	app-research	แสดงบทสรุปงานวิจัย 300–500 คำ
3	www.iam-589.com/api-589/<ข้อความ>	API Service	api-589	แสดงข้อความที่ส่งผ่าน URL ด้วยตัวอักษรขนาดใหญ่ตรงกลางหน้าจอ
4	admin.iam-589.com/	Admin Dashboard	admin-589	แสดงปุ่มสำหรับเลือกแก้ไขข้อมูล Student Portal และ Research

## 4. โครงสร้าง Repository

```text
K8s-Lab-Exam-/
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

## 5. เทคโนโลยีที่ใช้

| เทคโนโลยี | หน้าที่ |
|---|---|
| Kubernetes | ระบบบริหารจัดการ Container |
| Python Flask | พัฒนาเว็บแอปพลิเคชัน |
| NGINX Ingress Controller | จัดการเส้นทางการเข้าถึงเว็บ |
| ConfigMap | จัดเก็บ Configuration และ Application Code |
| Deployment | บริหารจัดการ Pod และจำนวน Replicas |
| ClusterIP Service | เปิดให้บริการภายใน Kubernetes Cluster |
| PersistentVolume | จัดเตรียมพื้นที่จัดเก็บข้อมูล |
| PersistentVolumeClaim | ขอใช้พื้นที่จัดเก็บข้อมูล |
| GitHub | จัดเก็บ Source Code และไฟล์ติดตั้งระบบ |

### 6.1 การเตรียมพื้นที่จัดเก็บข้อมูล

โครงงานใช้ Static PersistentVolume แบบ hostPath โดยกำหนดพื้นที่จัดเก็บข้อมูลบน `k8s-worker1` ดังนี้

```bash
sudo mkdir -p /var/lib/k8s-exam/portal
sudo mkdir -p /var/lib/k8s-exam/research
```

หมายเหตุ: การใช้ hostPath เป็นรูปแบบการจัดเก็บข้อมูลสำหรับ Lab Environment โดยข้อมูลจะผูกกับ Node ที่กำหนด ไม่ใช่ระบบ Shared Storage หรือ High Availability Storage

## 7. ขั้นตอนการติดตั้งระบบ

### ขั้นตอนที่ 1 ดาวน์โหลดโครงการ

```bash
git clone https://github.com/Panyapatkia/K8s-Lab-Exam-.git

cd K8s-Lab-Exam-
```

### ขั้นตอนที่ 2 ตรวจสอบ Kubernetes Cluster

```bash
kubectl get nodes -o wide
kubectl get ingressclass
kubectl cluster-info
```

### ขั้นตอนที่ 3 กำหนดสิทธิ์การทำงานของ Script

```bash
chmod +x scripts/*.sh
```

### ขั้นตอนที่ 4 ติดตั้งระบบ

```bash
./scripts/deploy.sh
```

สคริปต์จะดำเนินการติดตั้งตามลำดับ ได้แก่

1. ตรวจสอบการเชื่อมต่อ Kubernetes Cluster
2. ตรวจสอบ Worker Node และ NGINX Ingress Class
3. สร้าง Namespace
4. สร้าง PersistentVolume และ PersistentVolumeClaim
5. ติดตั้ง ConfigMap และ Deployment ของ Student Portal
6. ติดตั้ง ConfigMap และ Deployment ของ Research
7. ติดตั้ง ConfigMap และ Deployment ของ API Service
8. ติดตั้ง ConfigMap และ Deployment ของ Admin Dashboard
9. สร้าง Ingress สำหรับกำหนดเส้นทางการเข้าถึง
10. ตรวจสอบสถานะ Deployment

### ขั้นตอนที่ 5 ตรวจสอบการทำงาน

```bash
./scripts/verify.sh
```

หรือใช้คำสั่งตรวจสอบแยกตามประเภท Resource

```bash
kubectl get pods -n exam-589 -o wide
kubectl get deployments -n exam-589
kubectl get services -n exam-589
kubectl get pvc -n exam-589
kubectl get pv
kubectl get ingress -n exam-589
```

## 8. การเข้าถึงระบบ

กำหนด DNS หรือ Hosts File ของเครื่อง Client ให้ชี้ไปยัง Ingress Entry Point ของระบบ

| URL | รายละเอียด |
|---|---|
| http://www.iam-589.com/ | หน้า Student Portal |
| http://www.iam-589.com/edit | หน้าแก้ไขข้อมูลนักศึกษา |
| http://www.iam-589.com/research | หน้าสรุปงานวิจัย |
| http://www.iam-589.com/research/edit | หน้าแก้ไขข้อมูลงานวิจัย |
| http://www.iam-589.com/api-589/Hello-Kubernetes-589 | หน้า API Service |
| http://admin.iam-589.com/ | หน้า Admin Dashboard |

หมายเหตุ: การกำหนด DNS, External Load Balancer และ NodePort ต้องดำเนินการให้สอดคล้องกับสภาพแวดล้อมของ Kubernetes Cluster

## 9. การตรวจสอบและแก้ไขปัญหา

ตรวจสอบสถานะ Pod:

```bash
kubectl get pods -n exam-589 -o wide
```

ตรวจสอบ Log ของแต่ละแอปพลิเคชัน:

```bash
kubectl logs deployment/portal-589 -n exam-589
kubectl logs deployment/app-research -n exam-589
kubectl logs deployment/api-589 -n exam-589
kubectl logs deployment/admin-589 -n exam-589
```

ตรวจสอบ Ingress:

```bash
kubectl describe ingress exam-ingress -n exam-589
```

ตรวจสอบ Storage:

```bash
kubectl get pv,pvc -n exam-589
```

## 11. GitHub Repository

Source Code และไฟล์ Configuration ของโครงงาน:

https://github.com/Panyapatkia/K8s-Lab-Exam-
