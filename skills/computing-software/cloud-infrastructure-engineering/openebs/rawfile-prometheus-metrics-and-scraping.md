---
id: computing-software.cloud-infrastructure-engineering.openebs.rawfile-prometheus-metrics-and-scraping
name: rawfile-prometheus-metrics-and-scraping
category: computing-software
field: cloud-infrastructure-engineering
product: openebs
tags: [local-pv, rawfile, prometheus, metrics, servicemonitor, monitoring, pool, capacity]
level: practitioner
status: docs-checked
description: "Scrape Local PV Rawfile metrics on port 9100 with a ServiceMonitor or manual job and know the node-level and pool-level metric names for capacity and thin-provisioning alerts."
sources:
  - https://openebs.io/docs/user-guides/local-storage-user-guide/local-pv-rawfile/advanced-operations/rawfile-monitoring
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Rawfile exposes Prometheus metrics from the node plugin on every node, at three levels: node, pool and volume. Metrics are **on by default** and listen on port **9100**, which is configurable.

Scraping options: enable the chart's ServiceMonitor for Prometheus Operator and apply the values, or add a manual scrape job to your Prometheus configuration.

Node level: `rawfile_remaining_capacity_bytes` (label `node`) is the free capacity for new volumes on the node, excluding reserved storage.

Pool level (labels `node` and `pool`):

- `rawfile_pool_capacity_bytes`: maximum usable pool capacity;
- `rawfile_pool_remaining_capacity_bytes`: free capacity left;
- `rawfile_pool_reserved_capacity_bytes`: reserved for non-pool use;
- `rawfile_pool_backing_fs_capacity_bytes`, `..._available_bytes`, `..._usage_bytes`: the backing filesystem;
- `rawfile_pool_volumes_physical_bytes` and `rawfile_pool_volumes_logical_bytes`: disk really used versus provisioned, whose ratio is your overcommit;
- `rawfile_pool_volume_count`;
- `rawfile_pool_info`, labels only, value always 1.

The page also lists per-volume metrics, which this skill does not reproduce; consult it for names. The page's example alerts are a volume over 90% full and a pool with under 10 GiB free.

## Checked

2026-11-04. Confirmed against the Local PV Rawfile Monitoring page: default-on metrics, port 9100, ServiceMonitor and manual scrape options, the node and pool metric names and labels, and the example alerts. Removed the unsupported attribution to the thin provisioning guide.

Method: documentation only; no commands were run.
