---
id: computing-software.cloud-infrastructure-engineering.prometheus-operator.prometheus-operator-compatibility-and-requirements
name: prometheus-operator-compatibility-and-requirements
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-operator
tags: [compatibility, kubernetes-version, cel, prometheus-version, alertmanager-version, thanos-version, client-go]
level: intro
status: docs-checked
description: "Check which Kubernetes, Prometheus, Alertmanager and Thanos versions Prometheus Operator supports, including the v0.84.0 CEL requirement."
sources:
  - https://prometheus-operator.dev/docs/getting-started/compatibility/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Use component versions identical or close to those the operator end-to-end suite uses.

## Kubernetes
Because the CRDs use Common Expression Language (CEL) validation, operator v0.84.0 and later requires Kubernetes 1.25 or newer (1.23 with the `CustomResourceValidationExpressions` feature gate). Releases before v0.84.0 need Kubernetes 1.16 or newer. The operator talks to the API through the Go `client-go` library, so the client-go compatibility matrix applies; anything beyond it is best effort.

## Prometheus
All Prometheus versions from v2.0.0 are supported. The e2e tests deploy a long list of v2.45 through v3.x releases, and run mostly against the default version baked into the operator release.

## Alertmanager and Thanos
Alertmanager v0.15 and above; Thanos v0.10 and above. Each operator release tests mostly against one default Alertmanager and one default Thanos version.

## Practical use
Before upgrading the operator on an older cluster, check the Kubernetes floor first.

## Checked

2026-11-08. Read the compatibility page in full. Version floors (Kubernetes 1.25, or 1.23 with the feature gate, from v0.84.0; 1.16 before; Prometheus 2.0.0; Alertmanager 0.15; Thanos 0.10) match. Removed unsourced advice about pinning images and diagnosing CRD failures.

Method: documentation only; no commands were run.
