---
id: computing-software.cloud-infrastructure-engineering.observability.otel-kubernetes-and-cloud-resource-semantic-conventions
name: otel-kubernetes-and-cloud-resource-semantic-conventions
category: computing-software
field: cloud-infrastructure-engineering
product: observability
tags: [opentelemetry, k8s-resource-semconv, cloud-semconv, resource-attributes, k8sattributes-processor]
level: advanced
status: docs-checked
description: "Populate OpenTelemetry Kubernetes (k8s.*) and cloud (cloud.*) resource attributes with the k8sattributes and resourcedetection processors."
sources: ["https://opentelemetry.io/docs/specs/semconv/resource/k8s/", "https://opentelemetry.io/docs/specs/semconv/resource/cloud/", "https://opentelemetry.io/docs/kubernetes/collector/components/#kubernetes-attributes-processor", "https://opentelemetry.io/docs/specs/semconv/resource/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Kubernetes and cloud resource conventions

**Goal:** every span, metric and log carries where it ran, using standard names, so you can filter and join across signals.

## Kubernetes attributes
| Attribute | Example |
|---|---|
| `k8s.cluster.name` | `prod-weu-1` |
| `k8s.namespace.name` | `payments` |
| `k8s.pod.name`, `k8s.pod.uid` | `checkout-7d9f...` |
| `k8s.container.name` | `app` |
| `k8s.deployment.name` / `k8s.statefulset.name` / `k8s.daemonset.name` / `k8s.job.name` / `k8s.cronjob.name` | owner workload |
| `k8s.node.name` | `aks-np1-123` |
| `container.image.name`, `container.image.tag` | set by the k8sattributes processor when extracted |

## Cloud attributes
`cloud.provider` (for example `aws`, `azure`), `cloud.platform`, `cloud.region`, `cloud.availability_zone`, `cloud.account.id`, `cloud.resource_id`. The `cloud.platform` prefix should match `cloud.provider`. Well-known platform values include `aws_eks`, `aws_lambda`, `gcp_kubernetes_engine`, `azure.aks` and `azure.functions` (note the dot for Azure). When a well-known value applies it MUST be used; otherwise a custom value is allowed. These attributes are marked Development stability, so names can change.

## How to populate
1. **Collector `k8sattributes` processor**: associates telemetry with a pod and adds metadata:
```yaml
processors:
  k8sattributes:
    auth_type: serviceAccount
    passthrough: false
    extract:
      metadata: [k8s.namespace.name, k8s.pod.name, k8s.pod.uid, k8s.deployment.name, k8s.node.name, container.image.name]
      labels: [{ tag_name: app.team, key: team, from: pod }]
    pod_association:
      - sources: [{ from: resource_attribute, name: k8s.pod.ip }]
      - sources: [{ from: connection }]
```
   - With no `pod_association` rules the processor associates by the connection IP only. `connection` needs the processor to run before any batching or tail sampling, which remove that information.
   - `k8s.deployment.name` is derived from the ReplicaSet name by trimming the pod-template-hash; it must be listed under `extract.metadata`.
   - Extracting from Deployments, ReplicaSets, StatefulSets, DaemonSets, Jobs and CronJobs is disabled by default for labels and annotations and costs extra memory.
   - The processor's README gives ClusterRole rules with get, watch and list on pods, namespaces, nodes, replicasets and (for owner metadata) the apps and batch workload resources; copy the exact rules from the README for your extraction set.
2. **`resourcedetection` processor** for cloud and host data: detectors include `env`, `system`, `ec2`, `eks`, `azure`, `aks`, `gcp`, `azurefunctions`. The `eks` and `aks` detectors can emit `k8s.cluster.name` when enabled in their config.

## Gotchas
- A gateway collector behind a load balancer sees the agent's connection IP, not the pod. Do the `connection` association in the agent tier (the README's gateway example associates by resource attributes set by agents).
- Avoid copying every pod label (cardinality and cost).

## Verify
- [ ] Traces and metrics from one pod share identical `k8s.*` and `cloud.*` values; filtering by `k8s.deployment.name` works in all backends.

## Checked
Date: 2026-11-09. Confirmed in the semantic-conventions attribute registry (k8s and cloud pages: attribute names, platform and provider values, Azure values use a dot), the k8sattributes processor README (association, deployment derivation, extraction defaults, RBAC section, gateway example) and the resourcedetection processor README (detector names, cluster name for eks and aks). Removed: the downward API env var recipe and Operator injection claim (not on the cited pages), `host.*` attributes, `container.id` from the table, and the earlier azure_aks and azure_functions values (wrong).
Method: docs-checked 2026-11-09 against the semantic-conventions registry pages for k8s and cloud, the k8sattributes processor README, the resourcedetection processor README and the OpenTelemetry Kubernetes collector components page.
