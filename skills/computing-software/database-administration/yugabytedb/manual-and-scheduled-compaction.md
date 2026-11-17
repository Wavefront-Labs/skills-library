---
id: computing-software.database-administration.yugabytedb.manual-and-scheduled-compaction
name: manual-and-scheduled-compaction
category: computing-software
field: database-administration
product: yugabytedb
tags: [compaction, compact-table, yb-admin, yb-ts-cli, scheduled-full-compaction, auto-compact, disk-space]
level: advanced
status: docs-checked
description: "Run manual compaction with yb-admin compact_table or yb-ts-cli, and configure automatic and scheduled full compactions to reclaim space after bulk deletes."
sources: ["https://github.com/yugabyte/yugabyte-db/blob/master/docs/content/stable/admin/yb-admin.md", "https://github.com/yugabyte/yugabyte-db/blob/master/docs/content/stable/admin/yb-ts-cli.md", "https://github.com/yugabyte/yugabyte-db/blob/master/docs/content/stable/reference/configuration/yb-tserver.md", "https://github.com/yugabyte/yugabyte-db/blob/master/docs/content/stable/troubleshoot/nodes/disk-full.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Manual and scheduled compaction

Compaction merges SST files and drops deleted or overwritten data. After a bulk load or mass delete it can lag, leaving disk use high.

Manual:
```
yb-admin --master_addresses <masters> compact_table <db-type>.<namespace> <table> [timeout-in-seconds] [ADD_INDEXES]
yb-ts-cli --server_address=<tserver>:9100 compact_tablet <tablet_id>
yb-ts-cli --server_address=<tserver>:9100 compact_all_tablets
```
`timeout-in-seconds` is how long yb-admin waits for compaction to end (default 20). `ADD_INDEXES` compacts the table's secondary indexes and applies to YCQL only. Flush first with `flush_tablet` or `flush_all_tablets` if you need the memtable on disk.

Automatic triggers (tserver flags):
- `auto_compact_stat_window_seconds` sets the window for gathering statistics
- `auto_compact_percent_obsolete` is the share of obsolete keys that triggers compaction
- `auto_compact_min_obsolete_keys_found` is the minimum count before it triggers

Scheduled full compaction:
- `scheduled_full_compaction_frequency_hours` sets how often every tablet is fully compacted
- `scheduled_full_compaction_jitter_factor_percentage` spreads the start times so tablets do not all compact together

When dropping tables on a database with PITR enabled, tables go to a HIDDEN state and space is not freed until the schedules expire, so compaction alone will not help there.

## Checked

2026-11-04. Confirmed against yb-admin, yb-ts-cli, yb-tserver reference and the disk-full page. Fixed: compact_table takes <db-type>.<namespace>, the timeout default is 20 seconds, and ADD_INDEXES is YCQL only (the draft implied it works with ysql). Removed the generic load warning.

Method: documentation only; no commands were run.
