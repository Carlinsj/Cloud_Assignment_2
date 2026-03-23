# Cloud Assignment 2

Flask To-Do application with MongoDB, containerized with Docker, deployed on Kubernetes (Minikube and AWS EKS), and documented end to end from local development to cloud teardown.

## Project Summary

This repository implements a simple task-tracking web app with the following goals:

1. Build a working Flask + MongoDB application.
2. Containerize it with Docker.
3. Run the stack locally with Docker Compose.
4. Deploy it on Kubernetes (Minikube).
5. Deploy it on AWS EKS with external access.
6. Validate deployment behavior (rolling updates, probes, self-healing, persistence).
7. Implement extra-credit monitoring and alerting.
8. Tear down cloud resources to avoid cost.

## Architecture

1. Frontend/UI: Server-rendered HTML template (`templates/index.html`).
2. Backend: Flask app (`app.py`) with routes for viewing, adding, and deleting tasks.
3. Database: MongoDB collection (`tododb.todos`).
4. Container runtime: Docker image for Flask app.
5. Orchestration:
   - Local: Docker Compose.
   - Kubernetes local: Minikube (`NodePort` exposure).
   - Kubernetes cloud: AWS EKS (`LoadBalancer` exposure).
6. Observability/alerting: Prometheus + Slack notifications (extra credit).

Data flow:

1. User accesses Flask endpoint (`/`).
2. Flask reads/writes tasks from MongoDB via `MONGO_URI`.
3. Updated task list is rendered back in the browser.

## Repository Structure

1. `app.py` - Flask application and MongoDB integration.
2. `templates/index.html` - To-Do UI (`v2` title/header).
3. `requirements.txt` - Python dependencies (`flask`, `pymongo`).
4. `Dockerfile` - Flask image build definition.
5. `docker-compose.yml` - Local multi-container setup (Flask + MongoDB volume).
6. `k8s/mongo.yaml` - MongoDB Deployment, Service, and PVC (`mongo-pvc`, `gp2`, `1Gi`).
7. `k8s/flask.yaml` - Flask Deployment + NodePort Service for Minikube.
8. `k8s/flask-eks.yaml` - Flask Deployment + LoadBalancer Service for EKS.
9. `eks-cluster.yaml` - Final EKS cluster specification.

## Application Details

### Flask Routes

1. `GET /` - Fetch all tasks from MongoDB and render list.
2. `POST /add` - Insert a new task.
3. `GET /delete/<id>` - Delete a task by MongoDB ObjectId.

### Environment Variable

1. `MONGO_URI`
   - Local default in code: `mongodb://localhost:27017/`
   - Docker Compose / Kubernetes: set to service-based URI (`mongodb://mongo:27017/tododb`)

## Local Setup (Python)

### Prerequisites

1. Python 3.11+ (recommended)
2. pip

### Steps

```bash
python -m venv .venv
# Windows PowerShell
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python app.py
```

Application URL: `http://localhost:5000`

Note: Running the app this way expects a MongoDB instance reachable at the configured `MONGO_URI`.

## Docker

### Build Image

```bash
docker build -t as21153/flask-todo:v1 .
```

### Run with Docker Compose

```bash
docker compose up --build
```

This starts:

1. `web` (Flask app on port `5000`)
2. `mongo` (MongoDB with persistent named volume `mongo_data`)

Application URL: `http://localhost:5000`

### Stop Compose

```bash
docker compose down
```

## Kubernetes (Minikube)

### Prerequisites

1. Minikube
2. kubectl
3. Docker image available to Minikube (or pushed to registry)

### Deploy

```bash
kubectl apply -f k8s/mongo.yaml
kubectl apply -f k8s/flask.yaml
```

### Verify

```bash
kubectl get pods
kubectl get svc
kubectl get pvc
```

### Access App

```bash
minikube service flask-todo-service
```

### Operational Checks

Use these checks to validate assignment requirements:

```bash
# Rolling update example
kubectl set image deployment/flask-todo flask=as21153/flask-todo:v2
kubectl rollout status deployment/flask-todo

# Self-heal check
kubectl delete pod -l app=flask-todo
kubectl get pods -w

# Describe probes/events
kubectl describe deployment flask-todo
```

## AWS EKS Deployment

### Final Cluster Spec (Used)

From `eks-cluster.yaml`:

1. Cluster: `todo-cluster`
2. Region: `us-east-1`
3. Kubernetes version: `1.31`
4. Node group: `workers`
5. Instance type: `t3.small`
6. Capacity: min `2`, desired `2`, max `2`
7. Add-ons: `vpc-cni`, `kube-proxy`, `coredns`, `aws-ebs-csi-driver`

### Create Cluster

```bash
eksctl create cluster -f eks-cluster.yaml
```

### Deploy Workloads

```bash
kubectl apply -f k8s/mongo.yaml
kubectl apply -f k8s/flask-eks.yaml
```

### Verify and Access

```bash
kubectl get pods
kubectl get svc
```

Wait for `flask-todo-service` to get an external address (`EXTERNAL-IP`), then open:

```text
http://<EXTERNAL-IP>:5000
```

## Teardown (Cost Control)

Delete workloads first, then the cluster:

```bash
kubectl delete -f k8s/flask-eks.yaml
kubectl delete -f k8s/mongo.yaml
eksctl delete cluster --name todo-cluster --region us-east-1
```

This is required to prevent ongoing AWS charges.

## Docker Images

1. `as21153/flask-todo:v1`
2. `as21153/flask-todo:v2`

## Validation Checklist

1. App CRUD works in browser (add/delete tasks).
2. Docker Compose stack runs successfully.
3. Minikube pods/services/PVC are healthy.
4. Rolling update completes without downtime errors.
5. Pod deletion triggers automatic recovery.
6. Readiness/liveness probes report healthy behavior.
7. EKS service exposes app externally.
8. Prometheus + Slack alerting is configured and tested.
9. EKS and related resources are deleted after validation.

## Extra Credit (Implemented)

Prometheus-based monitoring and Slack alerting were implemented and validated.
