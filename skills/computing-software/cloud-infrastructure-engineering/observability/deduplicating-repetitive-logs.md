---
id: computing-software.cloud-infrastructure-engineering.observability.deduplicating-repetitive-logs
name: deduplicating-repetitive-logs
category: computing-software
field: cloud-infrastructure-engineering
product: observability
tags: [log-deduplication, repetitive-log-suppression, structured-logging, log-volume-reduction, rate-limited-logging]
level: practitioner
status: docs-checked
description: "Suppress repetitive log lines: zap sampling in the app, the OTel log dedup processor with a count attribute, and Grafana Explore dedup modes."
sources: ["https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/processor/logdedupprocessor", "https://pkg.go.dev/go.uber.org/zap#SamplingConfig", "https://grafana.com/docs/grafana/latest/explore/logs-integration/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Deduplicating and suppressing repetitive logs

A failing dependency can emit the same error thousands of times per second. Suppress repeats but keep the count.

## In the app (zap, Go)
`SamplingConfig` has Initial, Thereafter and an optional Hook, and its values are per second. Its purpose is to limit CPU and I/O load while keeping a representative subset. The production config enables sampling at 100:100 by default, meaning after the first 100 entries with the same level and message in a second, only every 100th is logged. A nil SamplingConfig disables sampling.

## In the collector (log dedup processor, alpha)
```yaml
processors:
  log_dedup:            # old name logdedup still works with a deprecation warning
    interval: 10s
    log_count_attribute: log_count
    timezone: UTC
    timestamp_mode: aggregated   # or preserved
    exclude_fields: [attributes.request_id]
    conditions: ['severity_number >= SEVERITY_NUMBER_WARN']
```
- Logs are identical when body, resource attributes, severity and log attributes match. One log is emitted per interval (default 10s) with a count (default attribute log_count) plus first_observed_timestamp and last_observed_timestamp.
- Without conditions every log is eligible; logs matching no condition pass through unchanged. Condition paths should carry a context prefix such as log. or resource.
- include_fields and exclude_fields are mutually exclusive; the whole body cannot be excluded. metadata_keys partitions aggregation by client metadata, with metadata_cardinality_limit (0 = unlimited).
- The README recommends preserved timestamp mode when accurate time analysis or alerting matters.

## At query time (Grafana Explore)
Dedup options are None, Exact (whole line minus dates), Numbers (strips numbers such as durations and IPs) and Signature (the most aggressive; keeps only whitespace and punctuation). This is a display option and does not reduce stored volume.

## Rules
- Keep the count of suppressed logs, or log-based error rates will be wrong.
- Avoid deduplicating compliance-critical or audit logs (stated in the processor README).
- Prefer fixing the source: one error log plus a counter, with backoff on the failing call (advice, not on the pages).

## Verify
- [ ] A burst of identical logs yields one record per interval with log_count set
- [ ] Logs that differ in an excluded field still dedup
- [ ] Audit logs bypass the processor

## Checked

2026-11-08. Confirmed: processor README (how it works, options, defaults, output attributes, timestamp modes, conditions, rename to log_dedup), zap SamplingConfig fields and per-second wording and the 100:100 production default, Grafana dedup modes. The zap doc excerpt did not state the "level and message" keying within SamplingConfig itself; that detail comes from the Config documentation text. Removed as unsupported by these pages: Logback DuplicateMessageFilter, Log4j2 BurstFilter, the Python filter recipe, and the LogQL query.
Method: documentation only; no commands were run.
