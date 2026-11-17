---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.loki-out-of-order-writes-and-stream-sharding
name: loki-out-of-order-writes-and-stream-sharding
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [loki-out-of-order, automatic-stream-sharding, per-stream-rate-limit, loki-labels, ingester]
level: advanced
status: verified
description: "Understand Loki's out-of-order acceptance window per stream and enable automatic stream sharding for hot streams hitting per-stream rate limits."
sources: ["https://grafana.com/docs/loki/latest/configure/#accept-out-of-order-writes", "https://grafana.com/docs/loki/latest/operations/automatic-stream-sharding/", "https://grafana.com/docs/loki/latest/configure/#limits_config"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Out-of-order writes and stream sharding

## Out-of-order
A stream accepts entries out of order as long as they are not older than a window relative to the newest entry of that stream: `max_chunk_age / 2` (default `max_chunk_age` 2h, so ~1h; tested: 59 minutes behind was accepted, 61 minutes behind was rejected with HTTP 400 `entry too far behind`). `limits_config.unordered_writes` (default true) is marked deprecated in the 3.7.9 reference.
- Multiple agents writing the **same** stream (same label set) with skewed clocks cause rejections: add a distinguishing label (e.g. `agent`/`pod`) or fix time sync.
- `reject_old_samples` (default true) and `reject_old_samples_max_age` (default 1 week) are a separate absolute limit: an entry 8 days old was rejected with `has timestamp too old`.

## Automatic stream sharding
One very hot stream (e.g. a single ingress controller) is limited by `per_stream_rate_limit` (default 3MB/s) and stored on one ingester set. Automatic sharding splits it and is **on by default** in Loki 3.7.9 (`shard_streams.enabled` defaults to true; a test with no config pushed 25 MB of one stream and got shards `__stream_shard__` 0 to 3). Tune it:
```yaml
limits_config:
  shard_streams:
    enabled: true
    desired_rate: 1536KB     # target rate per shard
```
The distributor adds a `__stream_shard__` label so writes spread across ingesters. Queries are unaffected (`count_over_time({app="hot"}[1h])` summed all shards to 25000 lines). `time_sharding_enabled` (default false) instead adds a `__time_shard__` label so very old out-of-order logs can be backfilled.

## When to add labels instead
If the hot stream mixes logically different sources (several apps under one label set), proper labels (`app`) beat sharding.

## Gotchas
- Sharding increases stream count; check `max_global_streams_per_user`.

## Verify
- [ ] `loki_discarded_samples_total{reason="per_stream_rate_limit"}` and `too_far_behind` stay at 0 after changes.

## Checked
Ran Loki 3.7.9 locally: pushed a newest entry then entries 20, 29, 31, 45, 59, 61 and 90 minutes older into fresh streams (accepted up to 59, HTTP 400 `entry too far behind` at 61 and 90, message names the oldest acceptable timestamp); an 8-day-old entry with `reject_old_samples: true` gave `has timestamp too old`; 40 pushes of 1 MB to one stream with no `shard_streams` setting created `__stream_shard__` values 0 to 3 (`loki_rate_store_max_stream_shards 4`) and a sum over the stream returned all 25000 lines; with `shard_streams.enabled: false` and `per_stream_rate_limit: 1MB` a push returned 429 `Per stream rate limit exceeded (limit: 1MB/sec)`. Defaults (`max_chunk_age` 2h, `desired_rate` 1536KB, `unordered_writes` true) read from `-print-config-stderr` and the v3.7.9 configuration reference; the sharding doc (operations/automatic-stream-sharding) confirms the default and the `__stream_shard__` / `__time_shard__` labels.
