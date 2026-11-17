---
id: computing-software.ai-ml-engineering.kserve.kserve-knative-serverless-install
name: kserve-knative-serverless-install
category: computing-software
field: ai-ml-engineering
product: kserve
tags: [knative, serverless, knative-serving, istio, contour, version-matrix, feature-flags, cert-manager]
level: practitioner
status: docs-checked
description: "Install KServe in Knative serverless mode: Kubernetes, Istio and Knative version matrix, networking layer choice, PodSpec feature flags, Helm or YAML install."
sources: ["https://github.com/kserve/website/blob/main/docs/admin-guide/serverless/serverless.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Knative (serverless) mode install

Knative mode gives request-based autoscaling, scale to and from zero, revisions and canary rollout. Recommended for predictive inference (short requests, CPU models); for GPU generative workloads prefer Standard mode. Kubernetes 1.32 is the minimum.

| Kubernetes | Istio | Knative |
|---|---|---|
| 1.32, 1.33 | 1.27, 1.28 | 1.19, 1.20 |
| 1.34 | 1.28 | 1.19, 1.20 |

Steps:
1. Install Knative Serving (YAML install guide from knative.dev).
2. Install a networking layer: Istio is recommended (best tested with KServe); Kourier or Contour also work.
3. Install cert-manager 1.15.0+ (or use the self-signed cert script).
4. Install KServe:

```bash
helm install kserve-crd oci://ghcr.io/kserve/charts/kserve-crd --version v0.20.0
helm install kserve oci://ghcr.io/kserve/charts/kserve-resources --version v0.20.0
# or
kubectl apply --server-side -f https://github.com/kserve/kserve/releases/download/v0.20.0/kserve.yaml
kubectl apply --server-side -f https://github.com/kserve/kserve/releases/download/v0.20.0/kserve-cluster-resources.yaml
```

Gotchas:
- `--server-side` is required because the InferenceService CRD is large.
- ClusterServingRuntimes (the second YAML) are required for built-in runtimes on v0.8.0+.
- To use PodSpec fields `nodeSelector`, `affinity`, `tolerations` in v1beta1, enable the matching Knative feature flags.
- Knative 1.13.1 needs Istio 1.20+; gRPC routing fails on older Istio.

## Checked
Confirmed against the KServe Knative mode installation guide: Kubernetes 1.32 minimum, the Istio and Knative version matrix, networking layer options, cert-manager 1.15.0 minimum, Helm and YAML commands, the server-side apply note, the ClusterServingRuntimes note and both warnings.

Method: docs-only read of cited pages, 2026-11-08
