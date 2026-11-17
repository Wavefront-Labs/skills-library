---
id: computing-software.cloud-infrastructure-engineering.grafana-alloy.grafana-alloy-estimate-resource-usage
name: grafana-alloy-estimate-resource-usage
category: computing-software
field: cloud-infrastructure-engineering
product: grafana-alloy
tags: [resource-usage, sizing, capacity-planning, active-series, daemonset-logs]
level: practitioner
status: docs-checked
description: "Rules of thumb for sizing Alloy CPU, memory and bandwidth per million active series, per MiB/s of logs, and per 100 profiles per second."
sources: ["https://github.com/grafana/alloy/blob/main/docs/sources/set-up/estimate-resource-usage.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Estimating Alloy resource usage

These are starting points drawn from maintainers' operational experience. Real usage depends on workload, hardware and configuration.

## Prometheus metrics
Driven by the number of active series and the scrape interval. Per 1 million active series at the default scrape interval expect roughly:
- 0.4 CPU cores
- 11 GiB of memory
- 1.5 MiB/s of total network bandwidth (send and receive)

The figures come from clustered deployments but broadly apply to other modes.

## Loki logs
Driven by log volume. Per 1 MiB/second ingested expect about:
- 1 CPU core
- 120 MiB of memory

Based on Kubernetes DaemonSets on clusters with few nodes and heavy per-node volume. With many small nodes the cost per MiB/s is higher because of the constant per-node overhead. Label count, file count and average line length also matter.

## Pyroscope profiles
Per 100 profiles/second expect about 1 CPU core and 10 GiB of memory. Profile size and fetch frequency also affect usage.

## Checked

2026-11-08. Read in full the raw Alloy docs page behind the cited URL (docs/sources/set-up/estimate-resource-usage.md): every figure for metrics, logs and profiles and the caveats. Removed the closing advice about choosing replicas versus vertical sizing, which the page does not state.

Method: documentation only; no commands were run.
