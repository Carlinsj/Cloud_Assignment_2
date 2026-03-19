# Cloud Assignment 2 - Flask + MongoDB on Docker and Kubernetes

## 1. Project Overview
This project is a To-Do web application built with Flask and MongoDB for Cloud Computing and Big Data Systems (Spring 2026, Assignment 2).

The assignment flow is:
1. Build the application.
2. Containerize it with Docker.
3. Deploy and validate on Minikube/Kubernetes.
4. Deploy to AWS EKS.
5. Optionally complete extra credit (alerting).

## 2. Current Project Status
Status as of this README update:

### Completed
1. Application built and working (add/delete todo).
2. Docker containerization completed.
3. Docker Compose integration (Flask + Mongo) completed.
4. Docker image pushed to DockerHub.
5. Kubernetes manifests updated for assignment requirements.
6. Minikube deployment completed and validated.
7. ReplicaSet self-healing test completed.
8. Rolling update test completed.
9. Health monitoring (liveness/readiness) test completed, including induced failure and recovery.
10. Required Minikube screenshot sets captured.

### Pending
1. AWS EKS deployment (Part 4).
2. Final submission document assembly (if not yet compiled).
3. Extra credit alerting (Prometheus + Slack), if attempted.

## 3. Implemented Files and Changes

### App and Local Runtime
1. app.py
- Flask routes for:
  - / (list todos)
  - /add (create todo)
  - /delete/<id> (delete todo)
- Mongo connection via MONGO_URI.

2. templates/index.html
- Basic UI for add/delete todo operations.
- Title/header updated to v2 for rollout verification screenshots.

3. requirements.txt
- flask
- pymongo

### Docker
1. Dockerfile
- Base image: python:3.11-slim
- Installs dependencies from requirements.txt
- Runs Flask app on port 5000

2. docker-compose.yml
- web service (Flask)
- mongo service (MongoDB)
- Persistent volume for Mongo data in local Docker

### Kubernetes
1. k8s/mongo.yaml
- Deployment for MongoDB
- Service: mongo on port 27017
- PersistentVolumeClaim: mongo-pvc (1Gi, RWO)
- Volume mount at /data/db

2. k8s/flask.yaml
- Deployment: flask-todo
- Replicas: 2
- RollingUpdate strategy:
  - maxUnavailable: 1
  - maxSurge: 1
- Probes:
  - readinessProbe on /
  - livenessProbe on /
- Service: flask-todo-service (NodePort)
- Env var: MONGO_URI=mongodb://mongo:27017/tododb
- Image: as21153/flask-todo:v1 (v2 used during rolling update validation)

## 4. Environment and Dependencies

### OS and Shell
- Windows
- PowerShell

### Tooling snapshot
1. Docker: 25.0.2
2. kubectl client: v1.29.1
3. AWS CLI: 2.33.22
4. eksctl: 0.224.0
5. Minikube: v1.38.1

### Python runtime used for local app validation
- Local virtual environment in .venv
- Python interpreter in environment used successfully for dependency and smoke testing

### Python dependencies
- flask
- pymongo

## 5. Current Kubernetes Runtime Snapshot
At the time of update:
1. Node:
- minikube Ready (control-plane)

2. Running pods:
- flask-todo (2 replicas running)
- mongo (1 replica running)

3. Services:
- flask-todo-service (NodePort)
- mongo (ClusterIP)

4. Storage:
- mongo-pvc Bound (1Gi, RWO)

## 6. Docker Images
Published images:
1. as21153/flask-todo:v1
2. as21153/flask-todo:v2

## 7. How to Run Locally

### Option A: Docker Compose
1. docker compose up --build
2. Open http://localhost:5000
3. Use app (add/delete)
4. Stop with Ctrl+C, then docker compose down

### Option B: Kubernetes (Minikube)
1. Start Minikube (if needed):
- C:\Program Files\Kubernetes\Minikube\minikube.exe start

2. Apply manifests:
- kubectl apply -f k8s/mongo.yaml
- kubectl apply -f k8s/flask.yaml

3. Check health:
- kubectl get pods
- kubectl get svc
- kubectl get pvc

4. Open service URL:
- C:\Program Files\Kubernetes\Minikube\minikube.exe service flask-todo-service --url

Important on Windows with Docker driver:
- Keep the service/tunnel terminal open while using the generated URL.

## 8. Assignment Validation Already Performed
1. Cluster state screenshots captured:
- nodes, pods, rs, svc, pvc

2. Browser app screenshots captured:
- app page
- add todo
- delete todo

3. ReplicaSet self-heal captured:
- pod deletion and automatic recreation

4. Rolling update captured:
- kubectl set image
- kubectl rollout status
- kubectl rollout history

5. Health monitoring captured:
- induced liveness failure (/__fail)
- events showing probe failure and container restart
- rollback/recovery to healthy state

## 9. What Is Left to Finish the Assignment

### Part 4 (AWS EKS)
1. Create EKS cluster.
2. Configure kubectl context to EKS.
3. Deploy manifests to EKS.
4. Expose app externally (LoadBalancer).
5. Capture required EKS screenshots.
6. Delete EKS cluster/resources to avoid cost.

### Documentation
1. Compile final report with all screenshots and brief explanation per part.
2. Include command evidence and outcomes.

### Extra Credit (Optional)
1. Install/deploy Prometheus stack.
2. Configure alerts for failures.
3. Integrate Slack notifications.
4. Trigger alert and capture evidence.

## 10. Notes
1. The repository currently reflects a Minikube-ready state.
2. Kubernetes manifests are configured to meet assignment expectations for persistence, rollout strategy, and health probes.
3. Service access on Windows + Minikube Docker driver may require keeping the Minikube service command terminal open.