---
id: computing-software.cloud-infrastructure-engineering.minio.prometheus-metrics
name: prometheus-metrics
category: computing-software
field: cloud-infrastructure-engineering
product: minio
tags: [minio, prometheus-metrics, mc-admin-prometheus-generate, scrape-config, alert-rules, bearer-token, metrics-v2, drive-metrics]
level: practitioner
status: docs-checked
description: "Scrape MinIO v2 metrics with Prometheus via mc admin prometheus generate for cluster, node, bucket and resource paths, with recommended drive metrics and baseline alert rules."
sources: ["https://github.com/minio/docs/blob/main/source/operations/monitoring/collect-minio-metrics-using-prometheus.rst"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# MinIO Prometheus metrics and alerts

MinIO publishes cluster, node, bucket and resource metrics in the Prometheus data model. The procedure uses version 2 metrics and needs an existing Prometheus with Alert Manager, network access from MinIO to Prometheus, and an `mc` alias.

## 1. Generate the scrape config
```
mc admin prometheus generate ALIAS            # cluster
mc admin prometheus generate ALIAS node       # per node
mc admin prometheus generate ALIAS bucket
mc admin prometheus generate ALIAS resource   # since RELEASE.2023-10-07T15-07-38Z
```
Output is a `scrape_configs` job with a `bearer_token` and a `metrics_path` of `/minio/v2/metrics/cluster`, `/node`, `/bucket` or `/resource`, plus `scheme` and `targets`.

Tuning:
- `scrape_interval` of 60s is recommended; lengthen it for deployments with many metrics so each scrape ends before the next. Choose the longest interval that meets your needs.
- Give `job_name` a value unique to this deployment.
- Deployments started with `MINIO_PROMETHEUS_AUTH_TYPE` set to `"public"` can omit `bearer_token`.
- Use `scheme: http` when not using TLS.
- `targets` can be any one node or a load balancer. Node metrics need every node listed.

## 2. Run and query
Append the generated job to the Prometheus config and start with `prometheus --config.file=prometheus.yaml`. Example queries use a range selector such as `minio_node_drive_free_bytes{job="minio-job"}[5m]`.

## Recommended basic metrics
`minio_node_drive_free_bytes`, `_free_inodes`, `_latency_us`, `_offline_total`, `_online_total`, `_total`, `_total_bytes`, `_used_bytes`, `_errors_timeout`, `_errors_availability`, `_io_waiting`.

## 3. Alert rules
The docs' baseline rules, in a rule file listed under `rule_files`, are `NodesOffline` (`avg_over_time(minio_cluster_nodes_offline_total{job="minio-job"}[5m]) > 0`, `for: 10m`) and `DisksOffline` (same with `minio_cluster_drive_offline_total`). Firing alerts go to Alert Manager. Use these alongside the probes in `computing-software.cloud-infrastructure-engineering.minio.healthcheck-api`.

## Checked

2026-11-03. Confirmed against the MinIO docs source: the Prometheus metrics pages: endpoints, authentication and metric names read. Removed or fixed: nothing.

Method: documentation only; no commands were run.
