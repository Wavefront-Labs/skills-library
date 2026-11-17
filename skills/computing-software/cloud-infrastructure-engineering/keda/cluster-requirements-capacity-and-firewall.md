---
id: computing-software.cloud-infrastructure-engineering.keda.cluster-requirements-capacity-and-firewall
name: cluster-requirements-capacity-and-firewall
category: computing-software
field: cloud-infrastructure-engineering
product: keda
tags: [kubernetes-compatibility, n-2, resource-requests, firewall-ports, port-6443, metrics-api]
level: intro
status: docs-checked
description: "Check KEDA 2.17 Kubernetes version support, per-component CPU and memory defaults and the ports the API server needs to reach."
sources:
  - https://keda.sh/docs/2.17/operate/cluster/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Kubernetes compatibility follows an N-2 approach: each KEDA release is generally tested against at least N-2 Kubernetes minor versions, and maintainers may extend that without a guarantee. Examples from the matrix: KEDA v2.17 against Kubernetes v1.30 to v1.32, v2.16 against v1.29 to v1.31, v2.15 against v1.28 to v1.30, v2.9 against v1.23 to v1.25.

Production capacity, applied by default when deploying through YAML, is the same for the three deployments (Admission Webhooks, Metrics Server, Operator): CPU limit 1 and request 100m, memory limit 1000Mi and request 100Mi.

Firewall: KEDA must be reachable inside the cluster so the API server can fetch metrics.
- Port `443`: control plane to port 443 on the Service IP range; required on all platforms except Google Cloud.
- Port `6443`: control plane to port 6443 on the Pod IP range; required only on Google Cloud.

Restrictive network policies on GKE therefore need the 6443 rule, while other platforms need the 443 rule.

Check the matrix before upgrading Kubernetes or KEDA so both stay inside the tested window.

## Checked

2026-11-03. Confirmed on the 2.17 Operate Cluster page: N-2 policy, compatibility matrix rows, capacity table, ports 443 and 6443.

Method: documentation only; no commands were run.
