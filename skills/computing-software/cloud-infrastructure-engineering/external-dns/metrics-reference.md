---
id: computing-software.cloud-infrastructure-engineering.external-dns.metrics-reference
name: metrics-reference
category: computing-software
field: cloud-infrastructure-engineering
product: external-dns
tags: [external-dns, prometheus-metrics, metrics-endpoint, last-sync-timestamp, skipped-records-owner-mismatch, webhook-provider-metrics]
level: practitioner
status: docs-checked
description: "ExternalDNS Prometheus metrics: /metrics endpoint on 7979, naming scheme, controller, registry, source and webhook_provider series, and what each gauge means."
sources:
  - https://raw.githubusercontent.com/kubernetes-sigs/external-dns/master/docs/monitoring/metrics.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ExternalDNS metrics

All metrics are on the `/metrics` endpoint in Prometheus format; the docs show `curl https://localhost:7979/metrics`. Names are `external_dns_<subsystem>_<name>`.

**controller**
- `consecutive_soft_errors` (gauge): consecutive soft errors in the reconcile loop.
- `last_reconcile_timestamp_seconds`: last attempted sync.
- `last_sync_timestamp_seconds`: last successful sync.
- `no_op_runs_total` (counter): loops with no provider changes.
- `verified_records` (label `record_type`): records present in both source and registry.

**provider (cache)**
- `cache_apply_changes_calls`, `cache_records_calls` (label `from_cache`).

**registry**
- `endpoints_total`, `errors_total`, `records` (by `record_type`).
- `skipped_records_owner_mismatch_per_sync` (labels `record_type`, `owner`, `foreign_owner`, `domain`).

**source**
- `endpoints_total`, `errors_total`, `records`.
- `invalid_endpoints` (labels `record_type`, `source_type`): rejected for invalid configuration.
- `deduplicated_endpoints`: removed as duplicates.

**webhook_provider:** `adjustendpoints_`, `applychanges_` and `records_` pairs of `requests_total` and `errors_total`.

Also `build_info` (version, revision, go_version, os, arch labels), `request_duration_seconds` (HTTP summary), and Go runtime and process metrics, which are OS dependent and may change.

## Checked

2026-11-04. Read the metrics page (Supported Metrics table and Go runtime metrics). Confirmed the endpoint, port 7979, the naming scheme, every controller, provider, registry, source and webhook_provider metric with its labels, build_info and request_duration_seconds. Removed the alert idea, which the page does not state.

Method: documentation only; no commands were run.
