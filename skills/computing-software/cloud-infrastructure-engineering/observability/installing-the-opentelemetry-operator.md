---
id: computing-software.cloud-infrastructure-engineering.observability.installing-the-opentelemetry-operator
name: installing-the-opentelemetry-operator
category: computing-software
field: cloud-infrastructure-engineering
product: observability
tags: [otel-operator-install, operator-cert-manager, opentelemetry-operator, otel-operator, helm]
level: practitioner
status: docs-checked
description: "Install the OpenTelemetry Operator with manifests or Helm, handle its admission webhook certificates (cert-manager or self-generated) and verify CRDs."
sources: ["https://opentelemetry.io/docs/platforms/kubernetes/operator/", "https://github.com/open-telemetry/opentelemetry-operator", "https://github.com/open-telemetry/opentelemetry-helm-charts/tree/main/charts/opentelemetry-operator"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Installing the OpenTelemetry Operator

The operator manages `OpenTelemetryCollector`, `Instrumentation`, `OpAMPBridge` (and target allocator) resources via admission webhooks, which need TLS certificates.

## Manifests (needs cert-manager)
```bash
kubectl apply -f https://github.com/cert-manager/cert-manager/releases/latest/download/cert-manager.yaml
kubectl wait --for=condition=Available deploy --all -n cert-manager --timeout=180s
kubectl apply -f https://github.com/open-telemetry/opentelemetry-operator/releases/latest/download/opentelemetry-operator.yaml
```
Pin versions in production instead of `latest`.

## Helm
```bash
helm repo add open-telemetry https://open-telemetry.github.io/opentelemetry-helm-charts
helm install opentelemetry-operator open-telemetry/opentelemetry-operator -n opentelemetry-operator-system --create-namespace \
  --set manager.collectorImage.repository=ghcr.io/open-telemetry/opentelemetry-collector-releases/opentelemetry-collector-k8s \
  --set admissionWebhooks.certManager.enabled=false \
  --set admissionWebhooks.autoGenerateCert.enabled=true
```
Without cert-manager, the chart can generate a self-signed cert (`autoGenerateCert`). The chart docs set `manager.collectorImage.repository` explicitly.

## Verify install
```bash
kubectl get crd | grep opentelemetry.io      # opentelemetrycollectors, instrumentations, opampbridges
kubectl -n opentelemetry-operator-system get pods
kubectl get validatingwebhookconfiguration,mutatingwebhookconfiguration | grep opentelemetry
```

## Gotchas
- The admission webhook listens on target port 9443; if the API server cannot reach it (NetworkPolicy, private-cluster firewall rules), CR creation can fail.
- Read the operator release notes before upgrading; the CRDs have both `v1alpha1` and `v1beta1` versions.
- Image registry restrictions: mirror the operator, collector and auto-instrumentation images.

## Verify
- [ ] A minimal `OpenTelemetryCollector` CR becomes a running Deployment, and a test pod with an injection annotation gets the init container.

## Checked
- 2026-10-28. Checked against the OpenTelemetry Operator README and manifests, and the Helm chart README for the operator (main, 2026-10).
- Confirmed: CRDs (`OpenTelemetryCollector`, `Instrumentation`, `OpAMPBridge`), cert-manager default, `admissionWebhooks.certManager.enabled` and `admissionWebhooks.autoGenerateCert.enabled`, `manager.collectorImage.repository`, webhook target port 9443, `opentelemetry-operator-controller-manager` deployment, `v1beta1` apiVersion.
- Fixed: collector image repository now the one the chart docs show. Removed (unconfirmed): GKE-specific firewall claim, CR conversion-on-upgrade claim.
Method: documentation only; no commands were run.
