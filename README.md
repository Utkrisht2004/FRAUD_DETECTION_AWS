# SecureGuard: Cloud-Native MLOps Fraud Detection 🛡️

## 📌 Overview

**SecureGuard** is an enterprise-grade, fully automated Machine Learning Operations (MLOps) pipeline built for real-time transaction fraud mitigation.

This project bypasses managed ML platforms (e.g., SageMaker) to prevent vendor lock-in. Instead, it serves a pre-trained XGBoost classification model via a containerized FastAPI backend. The entire infrastructure is codified using Terraform, orchestrated on Amazon EKS, and achieves sub-100ms inference latency to meet production-level financial compliance standards.

---

## 🏗️ System Architecture

> *(Optional: Add your architecture diagram below)*

```markdown
![Architecture](link-to-image.png)
```

The system utilizes a strictly decoupled microservices topology:

### Frontend (Gradio)

Captures user transaction inputs and transmits JSON payloads to the backend.

### Backend (FastAPI)

Ingests transaction payloads, dynamically loads the XGBoost artifact from Amazon S3 using IRSA, and executes fraud prediction inference.

### Infrastructure (Terraform)

Automates provisioning of a secure AWS environment, including:

* VPC
* Public & Private Subnets
* NAT Gateways
* Multi-AZ Amazon EKS Cluster

### CI/CD (GitHub Actions)

Automates building and pushing immutable Docker images to Amazon ECR.

---

## 🚀 Key Features

### 🔹 Decoupled Model Serving

Architected a system that retrieves serialized `.ubj` ML artifacts directly from Amazon S3 into pod memory during startup, isolating model weights from API routing logic.

### 🔹 Infrastructure as Code (IaC)

Engineered a fully automated AWS environment using Terraform, eliminating manual configuration drift.

### 🔹 Dynamic Auto-Scaling

Implemented Kubernetes Horizontal Pod Autoscalers (HPA) to seamlessly scale inference pods from 1 to 10+ replicas during transaction volume spikes.

### 🔹 Zero-Trust Security

Enforced least-privilege access using IAM Roles for Service Accounts (IRSA), enabling pods to securely access AWS resources without hardcoded credentials.

---

## 🛠️ Technology Stack

### Machine Learning

* Python
* XGBoost
* Scikit-learn
* Pandas

### Microservices

* FastAPI
* Uvicorn
* Pydantic
* Gradio

### Cloud & DevOps

* AWS

  * EKS
  * ECR
  * S3
  * VPC
  * ALB
* Terraform
* Docker
* Kubernetes
* kubectl

### CI/CD

* GitHub Actions

---

## 📂 Repository Structure

```plaintext
FRAUD_DETECTION_AWS/
├── app/
│   ├── api/                  # FastAPI backend and inference logic
│   ├── ui/                   # Gradio frontend dashboard
│   ├── requirements.txt      # Python dependencies
│   └── Dockerfile            # Containerization instructions
│
├── terraform/
│   ├── main.tf               # AWS provider and VPC configuration
│   ├── eks.tf                # EKS cluster provisioning
│   └── s3.tf                 # ML artifact storage configuration
│
├── k8s/
│   ├── deployment.yaml       # Kubernetes deployment configuration
│   └── service.yaml          # Load balancer and service routing
│
├── .github/
│   └── workflows/
│       └── deploy-api.yml    # Docker build & ECR push pipeline
│
└── README.md
```

---

## ⚙️ Quick Start Guide

### 1️⃣ Prerequisites

Ensure the following tools are installed:

* Docker Desktop
* AWS CLI (`aws configure`)
* Terraform
* kubectl

---

### 2️⃣ Provision Infrastructure

Navigate to the Terraform directory and initialize the AWS environment:

```bash
cd terraform
terraform init
terraform plan
terraform apply --auto-approve
```

---

### 3️⃣ Update Kubeconfig

Connect your local Kubernetes client to the newly provisioned EKS cluster:

```bash
aws eks --region ap-south-1 update-kubeconfig --name fraud-detection-eks
```

---

### 4️⃣ Deploy Microservices

Apply the Kubernetes manifests:

```bash
cd ../k8s

kubectl apply -f deployment.yaml
kubectl apply -f service.yaml
```

---

### 5️⃣ Access the Application

Retrieve the external endpoint:

```bash
kubectl get svc
```

Locate the `EXTERNAL-IP` or Load Balancer DNS and open it in your browser to access the SecureGuard dashboard.

---

## 🔄 CI/CD Workflow

The deployment pipeline automatically:

1. Detects code changes pushed to GitHub.
2. Builds a new Docker image.
3. Pushes the image to Amazon ECR.
4. Makes the updated image available for Kubernetes deployments.

This ensures consistent, repeatable, and immutable application releases.

---

## 🔐 Security Highlights

* IAM Roles for Service Accounts (IRSA)
* No hardcoded AWS credentials
* Private subnet deployment for worker nodes
* Principle of Least Privilege (PoLP)
* Infrastructure fully managed through Terraform

---

## 📈 Scalability

SecureGuard is designed for production-scale workloads:

* Kubernetes Horizontal Pod Autoscaling (HPA)
* Multi-AZ EKS deployment
* Containerized microservices
* Stateless API architecture
* Sub-100ms inference latency

---

## 🧹 Clean Up

To avoid unnecessary AWS charges, destroy all provisioned resources after testing:

```bash
cd terraform
terraform destroy --auto-approve
```

---

