---
id: computing-software.cloud-infrastructure-engineering.google-cloud.kubernetes-events-and-gke-audit-logs
name: kubernetes-events-and-gke-audit-logs
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, gke, kubernetes-events-logging, gke-audit-logs, k8s-audit, event-exporter, cloud-logging]
level: practitioner
status: docs-checked
description: "Query Kubernetes events and GKE audit logs in Cloud Logging: who deleted or changed an object, OOMKilled and scheduling events, retention beyond one hour, and useful filters."
sources: ["https://cloud.google.com/kubernetes-engine/docs/how-to/audit-logging", "https://cloud.google.com/kubernetes-engine/docs/how-to/view-logs#events", "https://cloud.google.com/kubernetes-engine/docs/concepts/about-logs"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Kubernetes events and GKE audit logs

## Events
GKE exports Kubernetes Events to Cloud Logging as part of system logging; the resource types are `k8s_cluster` and `k8s_pod`. See "Kubernetes Event logs" in the GKE logs pages for the exact filters.

## Audit logs (Kubernetes API)
- Admin Activity (always on): create/update/patch/delete of objects.
- Admin Activity audit logs cannot be disabled.
- Data Access audit logs are separate and configurable; if they push you over your log allotments, create sinks that exclude them.
```
resource.type="k8s_cluster" log_id("cloudaudit.googleapis.com/activity")
```
Entries carry `protoPayload.authenticationInfo.principalEmail` for the caller. Kubernetes method names are of the form `io.k8s.<api group>.<version>.<resource>.<verb>` (for example `io.k8s.authorization.rbac.v1.roles...`); read an entry to see the exact name before filtering on it.

GKE cluster operations appear under `resource.type="gke_cluster"`.

## Gotchas
- Route audit logs to the central security project via aggregated sink.

## Verify
- [ ] Deleting a test pod shows the audit entry with your identity within a minute.

## Checked

2026-10-27. Confirmed in the GKE audit logging, view logs (events) and about logs pages: `k8s_cluster` and `k8s_pod` resource types, Events exported to Cloud Logging, Admin Activity audit logs cannot be disabled, Data Access logs can be excluded by sinks, `gke_cluster` resource type, `principalEmail` field, `io.k8s.authorization.rbac.v1...` method-name style, aggregated sinks. Removed: etcd one-hour retention, `log_id("events")` and `jsonPayload.reason` filters, `gcloud logging read` example, DATA_READ/WRITE config detail, specific method names and recipes (scale, exec, secrets get), `google.container.v1.ClusterManager` names, best-effort and Config Sync principal gotchas. Read end to end.

Method: documentation only; no commands were run.
