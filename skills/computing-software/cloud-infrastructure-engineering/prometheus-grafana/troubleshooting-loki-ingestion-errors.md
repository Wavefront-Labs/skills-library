---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.troubleshooting-loki-ingestion-errors
name: troubleshooting-loki-ingestion-errors
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [loki-ingestion-errors, loki-429, loki-limits-config, ingestion-rate-limits, stream-limit-tuning]
level: practitioner
status: verified
description: "Map Loki push errors (429 rate_limited, per_stream_rate_limit, stream_limit, line_too_long, too_far_behind, greater_than_max_sample_age) to limits and fixes."
sources: ["https://grafana.com/docs/loki/latest/operations/request-validation-rate-limits/", "https://grafana.com/docs/loki/latest/configure/#limits_config", "https://grafana.com/docs/loki/latest/operations/automatic-stream-sharding/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Troubleshooting Loki ingestion errors

Discarded data is counted in `loki_discarded_samples_total{reason, tenant}` and `loki_discarded_bytes_total`; clients see 4xx/429 with the reason in the body.

| reason | Meaning | Limit (limits_config) | Fix |
|---|---|---|---|
| `rate_limited` (429) | tenant over ingestion rate | `ingestion_rate_mb`, `ingestion_burst_size_mb` | raise per tenant or reduce volume |
| `per_stream_rate_limit` (429) | one stream too hot | `per_stream_rate_limit` (default 3MB/s), `per_stream_rate_limit_burst` (15MB) | keep `shard_streams` on (it is the default), or add a label to split the stream |
| `stream_limit` (429) | too many active streams | `max_global_streams_per_user` (default 5000) | reduce label cardinality |
| `line_too_long` | line > `max_line_size` | `max_line_size`, or `max_line_size_truncate: true` | truncate in agent/limit |
| `greater_than_max_sample_age` | timestamp too old | `reject_old_samples`, `reject_old_samples_max_age` | fix clock/replay; raise age |
| `too_far_behind` / out of order | older than the stream's accepted window | out-of-order window tied to `max_chunk_age` | avoid one stream from many unsynced sources |
| `invalid_labels` / `missing_labels` | bad label names, no labels (a push with no labels is accepted in Loki 3: it gets `service_name="unknown_service"`) | | fix agent config |
| `max_label_names_per_series`, `label_name_too_long`, `label_value_too_long` (400) | too many labels (limit 15), over-long names or values | `max_label_names_per_series`, `max_label_name_length`, `max_label_value_length` | drop labels at the agent |
| `structured_metadata_too_many`, `structured_metadata_too_large`, `disallowed_structured_metadata` (400) | more than 128 entries (default), over 64KB per line, or structured metadata not allowed | `max_structured_metadata_entries_count`, `max_structured_metadata_size`, `allow_structured_metadata` | trim attributes |

## Queries
```promql
sum by (reason, tenant) (rate(loki_discarded_samples_total[5m]))
sum by (tenant) (rate(loki_distributor_bytes_received_total[5m]))
```
Agent side: Alloy `loki_write_dropped_entries_total`, `loki_write_batch_retries_total` and retry logs.

## Per-tenant overrides (runtime config)
```yaml
overrides:
  tenant-a:
    ingestion_rate_mb: 40
    ingestion_burst_size_mb: 80
    max_global_streams_per_user: 20000
```
Runtime config reloads without restart.

## Gotchas
- Agents retry 429s with backoff; sustained throttling fills agent buffers and then drops.
- Raising limits without capacity planning moves the problem to ingester memory.

## Verify
- [ ] `loki_discarded_samples_total` rate is 0 or explained; alert on any non-zero rate per tenant.

## Checked
Ran Loki 3.7.9 and provoked each error: tenant rate (`ingestion rate limit exceeded for user fake (limit: 4194304 bytes/sec)`, HTTP 429), `stream_limit` (`maximum active stream limit exceeded when trying to create stream`, 429, with `max_global_streams_per_user: 3`), `per_stream_rate_limit` (`Per stream rate limit exceeded (limit: 1MB/sec)`, 429, with sharding disabled), too far behind (400), `greater_than_max_sample_age` (400), line too long (400 `max entry size '262144' bytes exceeded`), 16 labels (400 `has 16 label names; limit 15`), label value too long, 129 structured-metadata entries (400, limit 128), invalid label name. `loki_discarded_samples_total{reason=...,tenant=...}` and `loki_discarded_bytes_total` showed those reasons; `loki_distributor_bytes_received_total` exists. A push with no labels was accepted. The per-tenant `overrides:` runtime-config block loaded with `-verify-config`. Reason names, HTTP codes and defaults also read from operations/request-validation-rate-limits (v3.7.9 docs source); Alloy metric names from the loki.write reference (v1.21.1).
