# Cloud Assignment 2 - Flask + MongoDB on Docker and Kubernetes

## 1. Overview
This project implements a Flask To-Do application with MongoDB and covers the full assignment lifecycle: local app, Docker, Kubernetes (Minikube), AWS EKS deployment, validation screenshots, and final teardown.

## 2. Final Status

### Completed
1. Flask + MongoDB application implemented and validated.
2. Docker image and Docker Compose workflow completed.
3. Minikube deployment completed (pods, services, PVC, rollout, self-heal, probe checks).
4. EKS deployment completed with external access through LoadBalancer.
5. Report screenshots captured for terminal output, AWS Console resources, browser validation, and teardown evidence.
6. EKS resources deleted after validation to prevent ongoing cost.

### Optional (Not Implemented)
1. Extra credit alerting stack (Prometheus + Slack).

## 3. Key Files
1. `app.py`: Flask routes and MongoDB integration.
2. `templates/index.html`: UI for add/delete to-do operations.
3. `Dockerfile`: Flask container build.
4. `docker-compose.yml`: Local multi-container setup (Flask + Mongo).
5. `k8s/mongo.yaml`: Mongo deployment + service + PVC (`mongo-pvc`, `gp2`, 1Gi).
6. `k8s/flask.yaml`: Minikube deployment + NodePort service.
7. `k8s/flask-eks.yaml`: EKS deployment + LoadBalancer service.
8. `eks-cluster.yaml`: Cost-controlled EKS cluster spec used for final successful run.

## 4. EKS Spec Used (Final)
1. Cluster name: `todo-cluster`
2. Region: `us-east-1`
3. Nodegroup: `workers`
4. Node type: `t3.small`
5. Capacity: min 2, desired 2, max 2
6. Add-ons: `vpc-cni`, `kube-proxy`, `coredns`, `aws-ebs-csi-driver`

## 5. Docker Images
1. `as21153/flask-todo:v1`
2. `as21153/flask-todo:v2`

## 6. Submission Notes
1. Use `t3.small` consistently in report text (final validated configuration).
2. Include both deployment and deletion evidence to demonstrate cost-aware lifecycle management.