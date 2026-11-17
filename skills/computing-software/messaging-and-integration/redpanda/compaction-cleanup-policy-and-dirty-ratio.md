---
id: computing-software.messaging-and-integration.redpanda.compaction-cleanup-policy-and-dirty-ratio
name: compaction-cleanup-policy-and-dirty-ratio
category: computing-software
field: messaging-and-integration
product: redpanda
tags: [compaction, cleanup-policy, dirty-ratio, min-cleanable-dirty-ratio, log-compaction-interval, tiered-storage]
level: advanced
status: docs-checked
description: "How Redpanda compaction works: cleanup policies, the dirty ratio formula, the min_cleanable_dirty_ratio and lag properties, scan order, and the Tiered Storage limitation."
sources:
  - https://docs.redpanda.com/streaming/current/manage/cluster-maintenance/compaction-settings/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Compaction is a best-effort background process that keeps the latest record per key. As in Kafka it does not guarantee perfect de-duplication and works on subsets of each partition. If an application needs every record for a key, use the `delete` policy.

**Policy** (`log_cleanup_policy` cluster-wide, `cleanup.policy` per topic, topic wins): `delete` (default, retention-based), `compact` (only removes superseded versions; a key's only record stays), or `compact,delete`.

**Tiered Storage.** Compaction operates on local storage. Once a segment is uploaded and removed locally it is not fetched back for compaction, so a key can appear in several segments.

**Dirty ratio** decides when a log is eligible:

```none
dirty_ratio = dirty_segment_bytes / total_closed_segment_bytes
```

Dirty segments are closed but uncompacted. Every `log_compaction_interval_ms` Redpanda scans, compacts only logs above the threshold, and processes them in descending dirty ratio.

| Property | Scope |
|---|---|
| `min_cleanable_dirty_ratio` / `min.cleanable.dirty.ratio` | cluster / topic: minimum ratio before compaction |
| `log_compaction_interval_ms` | cluster: scan frequency |
| `min_compaction_lag_ms` / `min.compaction.lag.ms` | minimum time a message stays uncompacted |
| `max_compaction_lag_ms` / `max.compaction.lag.ms` | maximum time before it must be eligible |

Lower the ratio for high-throughput topics with frequent key overwrites; raise it for topics with large segments or expensive I/O; override per topic with `min.cleanable.dirty.ratio`.

Topic properties apply immediately; do not change them on internal topics.

## Checked

2026-11-04. Policies, the Tiered Storage note, the ratio formula, the property table, scan behavior and tuning guidance were confirmed on the Compaction Settings page.

Method: documentation only; no commands were run.
