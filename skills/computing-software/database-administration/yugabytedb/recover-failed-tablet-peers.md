---
id: computing-software.database-administration.yugabytedb.recover-failed-tablet-peers
name: recover-failed-tablet-peers
category: computing-software
field: database-administration
product: yugabytedb
tags: [tablet-recovery, remote-bootstrap, delete-tablet, crash-loop, yb-ts-cli, tablet-replication, failed-tablets]
level: advanced
status: docs-checked
description: "Recover tablets whose Raft majority failed or a crash-looping tserver, using yb-ts-cli delete_tablet and remote_bootstrap, or by removing tablet files by UUID."
sources: ["https://github.com/yugabyte/yugabyte-db/blob/master/docs/content/stable/troubleshoot/cluster/replace_failed_peers.md", "https://github.com/yugabyte/yugabyte-db/blob/master/docs/content/stable/troubleshoot/cluster/failed_tablets.md", "https://github.com/yugabyte/yugabyte-db/blob/master/docs/content/stable/admin/yb-ts-cli.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Recover failed tablet peers

Normally a failed Raft peer is replaced by automatic remote bootstrap. Manual work is needed when a majority of a tablet's peers are bad. A list of tablets is available in the yb-master web UI at `<master-ip>:7000/tablet-replication`.

**Majority lost (RF 3 example):** one good peer NODE_GOOD, two bad NODE_BAD1 and NODE_BAD2, tablet TABLET1.
```
yb-ts-cli --server_address=NODE_BAD1 delete_tablet TABLET1
yb-ts-cli --server_address=NODE_BAD2 delete_tablet TABLET1
yb-ts-cli --server_address=NODE_BAD1 remote_bootstrap NODE_GOOD TABLET1
```
Delete from the broken peers only if necessary. The yb-ts-cli reference gives the syntax as `delete_tablet <tablet-id> "<reason-string>"`, which includes a reason string the recovery page's example omits, and `remote_bootstrap <source-host> <tablet-id>` (default server address localhost:9100). Once NODE_BAD1 has the data, the quorum has a healthy majority and NODE_BAD2 is removed automatically.

If you cannot use remote_bootstrap, do the equivalent by hand: on NODE_GOOD archive the WAL (Raft data), RocksDB, intents and snapshots directories for TABLET1; copy the archives to NODE_BAD1 on the same drive that holds its TABLET1 data; stop NODE_BAD1; remove its old WAL, RocksDB, intents and snapshots data for TABLET1; unpack the copy into those directories; restart NODE_BAD1, then restart NODE_GOOD so it observes the changed state. NODE_BAD2 is then removed from the quorum automatically.

**Tserver crash loop from tablet corruption:**
This is for crash loops the automatic remote bootstrap cannot fix (a CHECK or FATAL code path, or an unknown crash such as SIGSEGV that repeats on restart).
1. Stop the YB-TServer so it stops restarting (on YugabyteDB Anywhere, `yb-server-ctl tserver stop`).
2. Get the faulty tablet UUID from the logs.
3. Remove its files on every disk in `--fs_data_dirs`: `find /mnt/disk1 -name '*<UUID>*' | xargs rm -rf`
4. Start the tserver (`yb-server-ctl tserver start` on Anywhere). It should start, stay up and rejoin, while the load balancer re-replicates affected tablets.

A search by UUID across the `--fs_data_dirs` paths finds the tablet's WAL (`yb-data/tserver/wals/table-*/tablet-<UUID>`), `tablet-meta`, `consensus-meta`, and the RocksDB directory with its `.intents` and `.snapshots` siblings under `yb-data/tserver/data/rocksdb`.

## Checked

2026-11-04. Confirmed against the Manual remote bootstrap of failed peer page and the Recover YB-TServer from crash loop page (both read from raw GitHub because the originally cited URLs used wrong paths and returned 404), and the yb-ts-cli reference (delete_tablet and remote_bootstrap syntax, default port 9100). Added the manual-copy ordering and the tablet file layout from the page. Removed the claim that deleting other data risks loss, which these pages do not state. Source URLs corrected to replace_failed_peers.md and failed_tablets.md.

Method: documentation only; no commands were run.
