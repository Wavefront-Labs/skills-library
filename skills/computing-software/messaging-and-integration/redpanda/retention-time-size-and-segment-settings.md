---
id: computing-software.messaging-and-integration.redpanda.retention-time-size-and-segment-settings
name: retention-time-size-and-segment-settings
category: computing-software
field: messaging-and-integration
product: redpanda
tags: [retention, retention-ms, retention-bytes, segments, segment-ms, log-rolling, timestamps]
level: practitioner
status: docs-checked
description: "Set time and size retention at cluster and topic level, closed-segment eligibility, segment size and rolling, and v25.3 timestamp validation."
sources:
  - https://docs.redpanda.com/streaming/current/manage/cluster-maintenance/disk-utilization/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Retention applies to each partition independently, and only closed segments are deleted or compacted. For a time-based policy every message in the segment must exceed the limit. Size and time policies apply simultaneously and whichever removes more segments wins.

| Purpose | Cluster property (default) | Topic property |
|---|---|---|
| Time | `log_retention_ms` (604800000) | `retention.ms` |
| Size | `retention_bytes` (none) | `retention.bytes` |
| Local time, Tiered Storage | `retention_local_target_ms_default` (86400000) | `retention.local.target.ms` |
| Local size, Tiered Storage | `retention_local_target_bytes_default` (null) | `retention.local.target.bytes` |
| Segment lifetime | `log_segment_ms` (1209600000) | `segment.ms` |
| Segment size | `log_segment_size` (134217728) | `segment.bytes` |

```bash
rpk topic alter-config <topic> --set retention.ms=<retention_time>
rpk topic alter-config <topic> --set retention.bytes=<retention_size>
rpk cluster config set retention_bytes <retention_size>
```
The page suggests one day (`86400000`) to reduce out-of-disk risk, and sizing `retention_bytes` as a fraction of disk divided by partitions per topic (80% of disk for one partition, 80% divided by 10 for ten). Do not set `log_retention_ms` to `-1` unless Tiered Storage remote write uploads segments.

**Timestamps.** From v25.3 Redpanda validates batch timestamps using `log_message_timestamp_before_max_ms` and `log_message_timestamp_after_max_ms`. Older clusters use the broker timestamp; opt in with `curl --request PUT http://localhost:9644/v1/features/validated_batch_timestamps -d '{"state":"active"}'`. Destination clusters of MirrorMaker2 or Shadowing should enable it.

**Segments.** Segments close at `log_segment_size` or when the roll timeout (`segment.ms` / `log_segment_ms`, bounded by `log_segment_ms_min` and `log_segment_ms_max`) elapses. Compacted topics use `compacted_log_segment_size`. Very large segments delay compaction; very small ones add processing.

## Checked

2026-11-08. Read the whole Disk Utilization page. Confirmed: retention table and defaults, closed-segment and simultaneous policy rules, rpk commands, one-day and 80% sizing guidance, log_retention_ms -1 warning, v25.3 timestamp validation and Admin API opt-in, segment rolling and compacted-topic rules. Nothing removed.

Method: documentation only; no commands were run.
