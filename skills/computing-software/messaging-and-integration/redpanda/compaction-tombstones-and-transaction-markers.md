---
id: computing-software.messaging-and-integration.redpanda.compaction-tombstones-and-transaction-markers
name: compaction-tombstones-and-transaction-markers
category: computing-software
field: messaging-and-integration
product: redpanda
tags: [compaction, tombstones, delete-retention-ms, tombstone-retention-ms, transactions, control-batches]
level: advanced
status: docs-checked
description: "Control tombstone removal with tombstone_retention_ms and delete.retention.ms, know the Tiered Storage v1 restrictions, and remove transactional control batches during compaction."
sources:
  - https://docs.redpanda.com/streaming/current/manage/cluster-maintenance/compaction-settings/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
A tombstone is a record with a key and a null value; compaction uses it to delete earlier records for that key. Retention is set with the cluster property `tombstone_retention_ms` and the topic property `delete.retention.ms`; the topic value wins.

```bash
rpk cluster config set tombstone_retention_ms=100
rpk topic alter-config <topic-name> --set delete.retention.ms=5
rpk topic alter-config <topic-name> --delete delete.retention.ms
rpk topic alter-config <topic-name> --set delete.retention.ms=-1
```
The last disables tombstone removal for that topic; `--delete` returns it to the cluster value.

**Removal rules**
- `compact` only: tombstones go once past the retention limit, which is also the window consumers have to see a complete log including tombstones. Set it long enough for slow readers.
- `compact,delete`: both tombstone retention and normal garbage collection can remove them.
- Removal is coordinated across replicas, so it may be delayed if a replica is stopped or lagging.
- For faster cleanup the page cites the typical default of 24 hours (86400000 ms).

**Tiered Storage.** Tombstones are not removed on Tiered Storage v1 topics. You cannot enable `tombstone_retention_ms` while `cloud_storage_enabled`, `cloud_storage_enable_remote_read` or `cloud_storage_enable_remote_write` is on, and on a topic you cannot enable `delete.retention.ms` with `redpanda.remote.read` and `redpanda.remote.write`. Tiered Storage v2 (v26.2 onward) supports removal via `delete.retention.ms`.

**Transaction markers.** Commit and abort control batches are kept forever by default. To remove them during compaction:

```bash
rpk cluster config set log_compaction_tx_batch_removal_enabled=true
```
`delete.retention.ms` then applies to them. For `compact`-only topics you must set `delete.retention.ms` explicitly. Useful when transactional compacted topics show disk growth from markers.

## Checked

2026-11-04. The commands, removal rules, restrictions and the transaction marker setting were confirmed on the Compaction Settings page.

Method: documentation only; no commands were run.
