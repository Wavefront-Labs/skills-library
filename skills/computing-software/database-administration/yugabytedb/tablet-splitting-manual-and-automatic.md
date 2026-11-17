---
id: computing-software.database-administration.yugabytedb.tablet-splitting-manual-and-automatic
name: tablet-splitting-manual-and-automatic
category: computing-software
field: database-administration
product: yugabytedb
tags: [tablet-splitting, automatic-tablet-splitting, yb-admin, split-tablet, post-split-compaction, outstanding-tablet-split-limit]
level: advanced
status: docs-checked
description: "Split tablets manually with flush_tablet and split_tablet, or tune automatic splitting thresholds (128 MiB, 10 GiB, 100 GiB) and the post-split compaction limits."
sources: ["https://github.com/yugabyte/yugabyte-db/blob/master/docs/content/stable/architecture/docdb-sharding/tablet-splitting.md", "https://github.com/yugabyte/yugabyte-db/blob/master/docs/content/stable/reference/configuration/yb-master.md", "https://github.com/yugabyte/yugabyte-db/blob/master/docs/content/stable/reference/configuration/yb-tserver.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Manual and automatic tablet splitting

**Manual split:** a small amount of data can sit only in memory buffers, so flush the tablet to put SST files on disk, then split it into two (find tablet ids with `yb-admin list_tablets ysql.<db> <table>`). The original tablet id no longer exists afterward. Misuse, such as splitting low-traffic tablets, can leave many tablets of different sizes that cannot easily be fixed because tablet merging is not currently supported.
```
yb-ts-cli --server_address=<tserver>:9100 flush_tablet <tablet_id>
yb-admin --master_addresses <masters> split_tablet <tablet_id>
```

**Automatic split** is on by default from v2.18 per the architecture page (`--enable_automatic_tablet_splitting`). The yb-tserver reference lists default true, while the yb-master reference lists an auto flag with initial false and target true that behaves as true after promotion. It works in three phases chosen by shard count per node:
- Low phase, fewer than `tablet_split_low_phase_shard_count_per_node` shards (1): split tablets larger than `tablet_split_low_phase_size_threshold_bytes` (128 MiB).
- High phase, fewer than `tablet_split_high_phase_shard_count_per_node` shards (24): split above `tablet_split_high_phase_size_threshold_bytes` (10 GiB).
- Final phase: split above `tablet_force_split_threshold_bytes` (100 GiB). The total is still bounded by `max_create_tablets_per_ts` (default 50).

Each split creates two tablets that each need a full compaction to remove unneeded data. This can raise CPU and disk use, so the number of simultaneous splits is conservative by default and these flags tune it:
- master: `outstanding_tablet_split_limit` (the architecture page says default 1, but the yb-master reference says default 0, which disables the limit) and `outstanding_tablet_split_limit_per_tserver` (default -1, which the architecture page says derives 1 for up to 4 cores and 2 otherwise). Both limits count tablets doing post-split compactions.
- tserver: `full_compaction_pool_max_threads` (default -1, derived from CPU count; raising it may finish splits faster but needs more CPU and disk) and `automatic_compaction_extra_priority` (default 50, suggested 0 to 50; keeps small compactions from being starved by post-split ones)

Watch progress at `<master>:7000/tablet-servers` and `<tserver>:9000/tablets`. The page points to these flags for tuning if performance suffers because of automatic splitting.

## Checked

2026-11-04. Confirmed against the Tablet splitting page (manual flush_tablet and split_tablet walkthrough, three phases and thresholds, post-split compaction flags and defaults, monitoring URLs) and the yb-master and yb-tserver references (threshold defaults 1, 128 MiB, 24, 10 GiB, 100 GiB, max_create_tablets_per_ts 50, compaction flag defaults). Conflicts recorded in the skill: outstanding_tablet_split_limit default is 1 on the architecture page but 0 on the yb-master reference; the automatic-splitting default differs between the yb-tserver (true) and yb-master (auto flag, initial false, target true) references. Removed the advice to lower the outstanding limits before disabling the feature, which the page does not give.

Method: documentation only; no commands were run.
