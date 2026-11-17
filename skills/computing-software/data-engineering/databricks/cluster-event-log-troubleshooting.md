---
id: computing-software.data-engineering.databricks.cluster-event-log-troubleshooting
name: cluster-event-log-troubleshooting
category: computing-software
field: data-engineering
product: databricks
tags: [databricks, cluster-event-log, cluster-startup-failure, init-script-failure, cloud-provider-launch-failure, driver-not-responding, compute-troubleshooting]
level: practitioner
status: docs-checked
description: "Diagnose Databricks cluster start and stability issues from the event log: cloud launch failures, init script errors, unresponsive drivers, spot loss and autoscaling."
sources:
  - https://docs.databricks.com/en/compute/clusters-manage.html#view-compute-event-log
  - https://docs.databricks.com/en/init-scripts/logs.html
  - https://docs.databricks.com/api/workspace/clusters/events
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Cluster event log troubleshooting

**Goal:** turn "my job cluster failed to start" or "driver died" into a concrete cause and fix.

## Where to look
- Compute UI -> cluster -> **Event log** tab.
- API/CLI: `databricks clusters events <cluster-id> -o json | jq '.events[] | [.timestamp, .type] | @tsv'`

## Event types and what they mean
| Event / termination reason | Typical cause | Fix |
|---|---|---|
| `CLOUD_PROVIDER_LAUNCH_FAILURE`, `INSTANCE_UNREACHABLE` | VM quota, subnet IP exhaustion, capacity in AZ, security group/NSG rules | raise quota, larger subnet, fleet/other instance types, check networking |
| `SPOT_INSTANCE_TERMINATION` / nodes lost | spot reclaimed | on-demand driver, `first_on_demand`, fallback to on-demand, fewer spot workers |
| `INIT_SCRIPT_FAILURE` | init script non-zero exit | read init script logs, fix script, use workspace files/volumes paths |
| `DRIVER_NOT_RESPONDING` / `DRIVER_UNREACHABLE` | driver OOM or long GC, collect() of big data, too many notebooks attached | bigger driver, avoid collect, restart, split workloads |
| `DBFS_COMPONENT_UNHEALTHY`, `METASTORE_COMPONENT_UNHEALTHY` | control plane/metastore connectivity | check status page, network egress to metastore |
| `UPSIZE_COMPLETED`, `RESIZING`, `NODES_LOST` | autoscaling activity | expected; correlate with slowness |
| `INACTIVITY` (terminated) | auto-termination | expected |

## Init script logs
Configure cluster log delivery (`cluster_log_conf` to a volume or cloud storage). Init script stdout/stderr land in `<log-path>/<cluster-id>/init_scripts/<cluster-id>_<container-ip>/`. Common failures: package mirror unreachable (no egress).

## Driver logs
Spark driver logs: compute UI -> Driver logs (stdout, stderr, log4j). Look for `java.lang.OutOfMemoryError`, `GC overhead limit exceeded`, or Python `MemoryError` before the driver became unresponsive.

## Prevent repeats
- Cluster policies fix instance types/runtime, enforce log delivery and spot settings.
- For jobs, set task `max_retries` with `retry_on_timeout` to ride out transient launch failures.

## Verify
- [ ] Root cause recorded with the event type and termination code.
- [ ] Cluster log delivery configured on all job clusters (policy-enforced).

## Checked
2026-10-28. Confirmed against the Clusters events API reference (event type names such as CLOUD_PROVIDER_LAUNCH_FAILURE, INIT_SCRIPT_FAILURE, DRIVER_NOT_RESPONDING, UPSIZE_COMPLETED, INACTIVITY; first_on_demand, cluster_log_conf with a Volumes destination), the init script logs page (init_scripts/<cluster-id>_<container-ip> path) and the Jobs API (max_retries, retry_on_timeout). Removed: system table names, job run page link, DBFS root init script and apt remarks, pools and serverless claims, the details.reason.code jq field.
Method: documentation only; no commands were run.
