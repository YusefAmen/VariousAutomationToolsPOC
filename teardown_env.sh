#!/bin/bash

set -e

APP_NAME="mock-app"
NAMESPACE="monitoring"

echo "🗑️  Deleting ${APP_NAME} app deployment..."
kubectl delete -f ./app/deployment.yaml || echo "App deployment already gone."

echo "🧹 Uninstalling Prometheus via Helm..."
helm uninstall prometheus -n ${NAMESPACE} || echo "Prometheus not installed or already removed."

echo "🧼 Cleaning up namespace (optional)..."
kubectl delete namespace ${NAMESPACE} --ignore-not-found

echo "🛑 Stopping any port-forward processes..."
pkill -f "kubectl port-forward svc/mock-app-service" || echo "No port-forward running."

echo "🧯 Optionally stop Minikube? (y/n)"
read STOP_MINIKUBE
if [[ "$STOP_MINIKUBE" == "y" ]]; then
    echo "⛔ Stopping Minikube..."
    minikube stop
fi

echo "✅ Teardown complete."

