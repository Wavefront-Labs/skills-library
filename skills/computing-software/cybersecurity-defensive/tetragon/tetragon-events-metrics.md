---
id: computing-software.cybersecurity-defensive.tetragon.tetragon-events-metrics
name: tetragon-events-metrics
category: computing-software
field: cybersecurity-defensive
product: tetragon
tags: [metrics-events]
level: practitioner
status: docs-checked
description: "Reference for the three Tetragon events metrics, tetragon_events_total, tetragon_policy_events_total and tetragon_syscalls_total, and their labels."
sources:
  - "https://tetragon.io/docs/reference/metrics/"
  - "https://tetragon.io/docs/installation/metrics/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Tetragon events metrics

Goal: count the activity of processes Tetragon observes. There are three metrics in this group.

## `tetragon_events_total`

The total number of Tetragon events. Labels: `binary`, `event_type`, `namespace`, `node_name`, `pod`, `workload`. The `event_type` values are `PROCESS_EXEC, PROCESS_EXIT, PROCESS_KPROBE, PROCESS_LOADER, PROCESS_LSM, PROCESS_THROTTLE, PROCESS_TRACEPOINT, PROCESS_UPROBE, PROCESS_USDT, RATE_LIMIT_INFO`.

## `tetragon_policy_events_total`

Policy events calls observed. Labels: `binary`, `hook`, `namespace`, `node_name`, `pod`, `policy`, `workload`.

## `tetragon_syscalls_total`

System calls observed. Labels: `binary`, `namespace`, `node_name`, `pod`, `syscall`, `workload`.

## Controlling cardinality

Per the metrics setup page, these events metrics may have very high cardinality, especially on Kubernetes where each pod creates a separate timeseries. The Helm value `tetragon.prometheus.metricsLabelFilter` (or the `--metrics-label-filter` flag) takes a comma-separated list of enabled labels, for example:

```yaml
tetragon:
  prometheus:
    metricsLabelFilter: "namespace,workload,binary" # "pod" label is disabled
```

On Kubernetes the agent serves metrics at `/metrics` on port `2112` by default. Event metrics can be switched off while keeping health metrics with `--enable-event-metrics=false`.

## Checked

Date: 2026-11-07

Cited page read in full; every claim matched to page text.

Method: documentation only; no commands were run.
