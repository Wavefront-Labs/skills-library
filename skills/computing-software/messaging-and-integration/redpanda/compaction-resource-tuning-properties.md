---
id: computing-software.messaging-and-integration.redpanda.compaction-resource-tuning-properties
name: compaction-resource-tuning-properties
category: computing-software
field: messaging-and-integration
product: redpanda
tags: [compaction, tuning, backlog-controller, key-map, segment-size, properties]
level: advanced
status: docs-checked
description: "Compaction resource properties: controller shares and backlog size, per-shard index and key map memory, and compacted segment size limits, with documented defaults."
sources:
  - https://docs.redpanda.com/streaming/current/manage/cluster-maintenance/compaction-settings/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The Compaction Settings page lists these cluster properties that bound the resources and shape of compaction. Defaults are as printed there.

| Property | Meaning | Default |
|---|---|---|
| `log_compaction_interval` | Compaction frequency in ms (the dirty-ratio table names it `log_compaction_interval_ms`) | 10,000 ms |
| `min_cleanable_dirty_ratio` | Minimum dirty ratio for eligibility | not stated |
| `compaction_ctrl_backlog_size` | Backlog size of the compaction backlog controller | 10% of disk capacity |
| `compaction_ctrl_min_shares` | Minimum I/O and CPU shares for compaction | 10 |
| `compaction_ctrl_max_shares` | Maximum I/O and CPU shares for compaction | 1,000 |
| `storage_compaction_index_memory` | Per-shard memory for the compaction index | 128 MiB |
| `storage_compaction_key_map_memory` | Per-shard memory for the key map used to de-dupe keys | 128 MiB |
| `compacted_log_segment_size` | Base size of a compacted segment | 268435456 (256 MiB) |
| `max_compacted_log_segment_size` | Maximum size after consolidation | 5368709120 (5 GiB) |

Additional controller coefficients (`compaction_ctrl_p_coeff`, `compaction_ctrl_i_coeff`, `compaction_ctrl_d_coeff`, `compaction_ctrl_update_interval_ms`) exist but should be changed only on guidance from Redpanda support.

## Checked

2026-11-04. The property list, meanings, defaults and the support-only note were confirmed on the Compaction Settings page. An unsupported usage paragraph was removed.

Method: documentation only; no commands were run.
