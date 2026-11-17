---
id: computing-software.cloud-infrastructure-engineering.prometheus-operator.prometheus-operator-installation-methods
name: prometheus-operator-installation-methods
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-operator
tags: [installation, bundle-yaml, kube-prometheus, kube-prometheus-stack, helm, kustomize, install]
level: intro
status: docs-checked
description: "Install Prometheus Operator by bundle.yaml, kube-prometheus manifests or the kube-prometheus-stack Helm chart, including removal."
sources:
  - https://prometheus-operator.dev/docs/getting-started/installation/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Three supported routes.

## Plain YAML bundle
```bash
LATEST=$(curl -s https://api.github.com/repos/prometheus-operator/prometheus-operator/releases/latest | jq -cr .tag_name)
curl -sL https://github.com/prometheus-operator/prometheus-operator/releases/download/${LATEST}/bundle.yaml | kubectl create -f -
```
This installs the CRDs and the operator with its RBAC into the `default` namespace. For another namespace, download `kustomization.yaml` and `bundle.yaml` for the release tag into a temp directory, run `kustomize edit set namespace $NAMESPACE`, then `kubectl create -k "$TMPDIR"`. Wait for readiness with `kubectl wait --for=condition=Ready pods -l app.kubernetes.io/name=prometheus-operator`.

## kube-prometheus
Clone `prometheus-operator/kube-prometheus` (or download the zip) and run `kubectl create -f manifests/setup` first (namespace and CRDs), wait until `kubectl get servicemonitors --all-namespaces` succeeds, then `kubectl create -f manifests/`. Creating CRDs first avoids race conditions. It deploys the operator plus a Prometheus called `prometheus-k8s` with default alerts and rules. Tear down with `kubectl delete --ignore-not-found=true -f manifests/ -f manifests/setup`.

## Helm
The `kube-prometheus-stack` chart bundles manifests, Grafana dashboards and Prometheus rules. It is no longer part of Prometheus Operator and is maintained in prometheus-community/helm-charts.

If you are starting out, use the latest release; if your Kubernetes is old, upgrade Kubernetes before the operator.

## Checked

2026-11-08. Read the installation page in full. Bundle commands, kustomize steps, kube-prometheus order and teardown, and the Helm chart note match. Corrected apply to create for the kube-prometheus commands.

Method: documentation only; no commands were run.
