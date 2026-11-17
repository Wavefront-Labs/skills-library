---
id: computing-software.database-administration.clickhouse.replacingmergetree-upserts-and-final
name: replacingmergetree-upserts-and-final
category: computing-software
field: database-administration
product: clickhouse
tags: [database-administration, clickhouse, replacingmergetree, final, version-column, is-deleted]
level: practitioner
status: docs-checked
description: "Model upserts and deletes with ReplacingMergeTree using a version and deleted column, read with FINAL, and use CLEANUP carefully."
sources:
  - https://github.com/ClickHouse/clickhouse-docs/blob/main/docs/guides/developer/replacing-merge-tree.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# replacingmergetree upserts and final
ReplacingMergeTree removes duplicates, rows with the same sorting key (ORDER BY), during background merges, keeping the row with the highest version. Because merging is asynchronous and incomplete, duplicates exist until merged, so read with `FINAL` (or an argMax pattern) when you need the latest state.

```sql
CREATE TABLE posts_updateable
(
  Version UInt32, Deleted UInt8, Id Int32, Title String, Score Int32
)
ENGINE = ReplacingMergeTree(Version, Deleted)
ORDER BY Id;

SELECT * FROM posts_updateable FINAL WHERE Id = 42;
```
Insert an update as a new row with a larger Version. A delete is a row with the same key, a greater version and `Deleted = 1`. Deleted rows are not removed at merge time; `OPTIMIZE TABLE t FINAL CLEANUP` can remove them but needs the experimental setting `allow_experimental_replacing_merge_with_cleanup=1`.

Only run CLEANUP when: no rows with older versions of those keys will be inserted afterwards (they would be retained incorrectly), and all replicas are in sync (`SYSTEM SYNC REPLICA table`), ideally pausing inserts. The docs recommend using deletes this way only for low to moderate delete volumes (under 10%), or on partitions that no longer change.

Key point: the ORDER BY columns must uniquely identify a row across changes. If migrating from Postgres, include the original primary key in the ORDER BY.

Gotchas: queries without FINAL can return duplicate keys until merges happen. Partitioning lets deduplication run at partition level in parallel, so a partition key that varies for the same ORDER BY key stops those rows from collapsing together.

## Checked
2026-11-03. Confirmed against the ClickHouse docs guide "Replacing merge tree": version and deleted columns, FINAL reads, the experimental `allow_experimental_replacing_merge_with_cleanup=1` setting for `OPTIMIZE ... FINAL CLEANUP`, its conditions, the under 10% delete guidance, and partition-level deduplication. Removed: the unsupported FINAL performance and version claims and the untested Verify step.
Method: documentation only; no commands were run.
