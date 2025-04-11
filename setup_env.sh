#!/bin/bash

set -e  # Exit on error

APP_NAME="mock-app"
NAMESPACE="monitoring"
IMAGE_NAME="${APP_NAME}:latest"

echo "🚀 Starting Minikube (if not already running)..."
minikube status &>/dev/null || minikube start

echo "📦 Building Docker image inside Minikube..."
eval $(minikube docker-env)
docker build -t ${IMAGE_NAME} ./app

echo "📡 Deploying ${APP_NAME} to Kubernetes..."
kubectl apply -f ./app/deployment.yaml

echo "📊 Installing Prometheus (if not already installed)..."
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts 2>/dev/null || true
helm repo update
helm upgrade --install prometheus prometheus-community/prometheus \
  --namespace ${NAMESPACE} --create-namespace \
  -f ./prometheus/values.yaml

echo "⏳ Waiting for pods to be ready..."
kubectl wait --for=condition=ready pod -l app=${APP_NAME} --timeout=90s

echo "✅ Environment is ready. Testing service endpoint..."
kubectl port-forward svc/mock-app-service 8080:80 &>/dev/null &

echo "📍 You can now curl http://localhost:8080/metrics"
echo "📍 Prometheus should be scraping metrics from mock-app-service"

echo "🧪 Run your log parser or metrics alert scripts anytime now!"

