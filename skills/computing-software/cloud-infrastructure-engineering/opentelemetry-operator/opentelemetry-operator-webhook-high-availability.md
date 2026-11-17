---
id: computing-software.cloud-infrastructure-engineering.opentelemetry-operator.opentelemetry-operator-webhook-high-availability
name: opentelemetry-operator-webhook-high-availability
category: computing-software
field: cloud-infrastructure-engineering
product: opentelemetry-operator
tags: [opentelemetry-operator, webhook-high-availability, webhook-server, pod-mutation, poddisruptionbudget-webhook, anti-affinity]
level: sme
status: docs-checked
description: "Understand the RFC that runs the operator webhooks as a separate multi-replica deployment using the webhook-server subcommand, with a PDB and soft anti-affinity."
sources: ["https://github.com/open-telemetry/opentelemetry-operator/blob/main/docs/rfcs/webhook-high-availability.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Webhook high availability design

Why: the operator hosts pod mutation (`/mutate-v1-pod`, used for auto-instrumentation and sidecar injection), CR defaulting for Instrumentation, OpenTelemetryCollector, OpAMPBridge and TargetAllocator, validation for all CR types, and conversion for OpenTelemetryCollector. If webhooks are slow or down, pod creation and CR operations cluster-wide suffer. With them inside the leader-elected controller deployment, scaling webhooks means scaling the whole operator.

Design: the operator binary gains a `webhook-server` subcommand that registers every webhook handler but starts no controllers and no leader election, so a separate Deployment (2+ replicas) can serve them. The default `opentelemetry-operator` command stays backward compatible. The controller-manager still registers webhooks unless `ENABLE_WEBHOOKS=false`; the kustomize overlay patches the webhook Service selector to send traffic to the dedicated deployment.

Reliability details: a PodDisruptionBudget with `maxUnavailable: 1` (preferred over `minAvailable: 1` because a single replica can still be drained) and `preferredDuringScheduling` pod anti-affinity on `kubernetes.io/hostname` (soft, so small dev clusters still schedule). HPA integration is a non-goal. Certificates come from cert-manager on vanilla Kubernetes (shared by both deployments) and from OLM on OpenShift.

Rejected alternative: operator-managed webhook deployment, because of garbage-collection complexity across scopes and extra RBAC.

## Checked

Method: docs-checked 2026-11-09 against the webhook-high-availability RFC (read in full). The kustomize overlay named in the RFC is the OpenShift one.
