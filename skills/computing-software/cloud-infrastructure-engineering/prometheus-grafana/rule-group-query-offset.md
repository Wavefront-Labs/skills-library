---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.rule-group-query-offset
name: rule-group-query-offset
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [rule-query-offset, evaluation-delay, recording-rules, remote-write-receiver, rule-groups, prometheus]
level: advanced
status: verified
description: "Delay rule evaluation with query_offset (per group) or rule_query_offset (global) so rules over remote-written or late data see complete samples."
sources: ["https://prometheus.io/docs/prometheus/latest/configuration/recording_rules/#rule_group", "https://prometheus.io/docs/prometheus/latest/configuration/configuration/#configuration-file", "https://grafana.com/docs/mimir/latest/references/configuration-parameters/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Rule query offset

Rules evaluate at time T using data up to T. If samples arrive late (remote write from agents, OTLP, federation lag), the rule sees incomplete data and records too-low values that are never corrected.

## Config
```yaml
# prometheus.yml (global default)
global:
  rule_query_offset: 1m
# rule file (per group, overrides global)
groups:
  - name: edge-aggregates
    interval: 1m
    query_offset: 2m
    rules:
      - record: cluster:http_requests:rate5m
        expr: sum by (cluster) (rate(http_requests_total[5m]))
```
The group's evaluation timestamp is shifted into the past by the offset, so the query and the stored result refer to T - offset, by which time late samples have arrived. In a test with `query_offset: 30s` the newest stored sample of a recorded series was about 30 s old when read, against a few seconds or less for a group without offset.

## Choosing the offset
- Measure lateness: remote write lag on senders (`prometheus_remote_storage_highest_timestamp_in_seconds - prometheus_remote_storage_queue_highest_sent_timestamp_seconds`), p99 + margin.
- Data scraped directly by the same Prometheus is available at evaluation time; the offset is for received data.

## Equivalent in Mimir/Cortex
Mimir has a per-tenant `ruler_evaluation_delay_duration` limit (default 1m in its configuration reference); check its documentation for per-group settings.

## Gotchas
- Alerts using offset groups fire later by the offset: account for it in paging latency.
- Mixing groups with and without offset that depend on each other's outputs creates misaligned windows.

## Verify
- [ ] Recorded values no longer show a dip at the most recent points compared to the same query run later.

## Checked
Environment: Windows 11, Prometheus and promtool 3.15.1 (windows-amd64), client_golang 1.25.0 on Go 1.26.
- A rule file with `query_offset: 30s` on one group and none on another, evaluated every 2 s against scraped data: reading the recorded series back, the offset group's newest sample was 29-33 s old and the plain group's was 0-3 s old. `rule_query_offset: 1m` under `global` and `query_offset: 2m` on a group (the skill's YAML) pass `promtool check config` and `promtool check rules`; the defaults and semantics are on the 3.15 configuration and recording-rules pages.
- The two remote-write timestamp metrics exist on a 3.15.1 sender (`prometheus_remote_storage_highest_timestamp_in_seconds` and `prometheus_remote_storage_queue_highest_sent_timestamp_seconds`, equal to the second in steady state).
- Mimir `ruler_evaluation_delay_duration`: Mimir configuration reference (default 1m); the other Mimir names in the draft were removed as unconfirmed.
