---
id: computing-software.cloud-infrastructure-engineering.minio.healthcheck-api
name: healthcheck-api
category: computing-software
field: cloud-infrastructure-engineering
product: minio
tags: [minio, healthcheck-api, health-live, health-cluster, write-quorum, read-quorum, maintenance-check, load-balancer-probe]
level: practitioner
status: docs-checked
description: "Probe MinIO liveness, write quorum, read quorum and maintenance safety with the unauthenticated /minio/health endpoints and know what the 200, 503 and 412 codes mean."
sources: ["https://github.com/minio/docs/blob/main/source/operations/monitoring/healthcheck-probe.rst"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# MinIO healthcheck API

MinIO exposes unauthenticated endpoints that return only an HTTP status code. They carry no other data.

| Probe | Request | Meaning |
|---|---|---|
| Node liveness | `curl -I https://HOST:9000/minio/health/live` | `200 OK` means the server is online and functional. Other codes mean the caller cannot reach it (network issue or downtime). |
| Write quorum | `.../minio/health/cluster` | `200` means enough servers are online for write quorum; `503 Service Unavailable` means not. |
| Read quorum | `.../minio/health/cluster/read` | `200` read quorum met; `503` not. |
| Maintenance | `.../minio/health/cluster?maintenance=true` | `200` means write quorum survives taking that server down; `412 Precondition Failed` means quorum would be lost. |

For cluster probes use any node, or the load balancer hostname when one fronts the cluster.

## Limits of probes
A probe cannot prove a server is offline or processing I/O correctly. It shows only whether the caller reaches the server, or whether enough servers are up to meet quorum under the configured erasure-code parity (`computing-software.cloud-infrastructure-engineering.minio.erasure-parity`). Add Prometheus alerts for the gap:
- `minio_cluster_nodes_offline_total` (v2) or `minio_cluster_health_nodes_offline_count` (v3) for offline nodes.
- `minio_node_drive_free_bytes` for low free space.

Metrics are in `computing-software.cloud-infrastructure-engineering.minio.prometheus-metrics`.

## Checked
2026-11-03. Confirmed against the MinIO docs source: Healthcheck API page (healthcheck-probe.rst). Removed: the unsourced advice on using the maintenance check before rolling restarts.
Method: documentation only; no commands were run.
