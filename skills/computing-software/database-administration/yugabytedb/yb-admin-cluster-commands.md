---
id: computing-software.database-administration.yugabytedb.yb-admin-cluster-commands
name: yb-admin-cluster-commands
category: computing-software
field: database-administration
product: yugabytedb
tags: [yb-admin, cli, list-tablets, list-all-masters, change-config, are-nodes-safe-to-take-down, ysql-catalog-version, leader-stepdown]
level: practitioner
status: docs-checked
description: "Reference for the yb-admin commands used in day-to-day cluster operations: syntax, listing, config changes, safety checks, and the commands to avoid casually."
sources: ["https://github.com/yugabyte/yugabyte-db/blob/master/docs/content/stable/admin/yb-admin.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# yb-admin cluster commands

Syntax:
```
yb-admin --master_addresses <ip1:7100,ip2:7100,ip3:7100> [--timeout_ms 60000] [--certs_dir_name <dir>] <command> [args]
```
`--master_addresses` is a comma-separated list of YB-Master host:port pairs (default `localhost:7100`). `--timeout_ms` is the RPC timeout, default 60000 (0 means do not wait, -1 means wait indefinitely). Pass `--certs_dir_name` with the root certificate directory when TLS is on. Running `yb-admin` with no arguments lists all operations.

Inspect:
- `list_all_masters`, `list_all_tablet_servers`
- `list_tablets <ysql|ycql>.<keyspace> <table> [<max-tablets>]` shows replica locations and the leader; default max is 10, 0 returns all
- `ysql_catalog_version` prints the current YSQL catalog version
- `get_auto_flags_config`

Change configuration:
- `change_config <tablet-id> ADD_SERVER|REMOVE_SERVER <peer-uuid> [PRE_VOTER|PRE_OBSERVER]` changes one tablet's configuration; the role is required with ADD_SERVER. A node down under 15 minutes catches up by RPC when it returns and needs no REMOVE_SERVER; offline longer than 15 minutes it goes through remote bootstrap. For a node that will not return, remove it (REMOVE_SERVER) and add a new one.
- `change_master_config ADD_SERVER|REMOVE_SERVER <ip> <port> [<uuid>]` changes the master configuration; afterwards check the master UI or `dump_masters_state`.
- `modify_placement_info`, `modify_table_placement_info <keyspace> <table> <placement-info> <replication-factor> [<placement-id>]`, `set_preferred_zones` (leader affinity; run `modify_placement_info` first, since preferred zones must match existing placement blocks). Use `modify_table_placement_info` only for YCQL tables or transaction status tables; for YSQL tables use CREATE TABLESPACE.
- `change_blacklist ADD|REMOVE <ip:port> ...` (tservers, for example `node1:9100`), `change_leader_blacklist ADD|REMOVE <ip:port> ...`.
- `set_load_balancer_enabled 0|1` (enabled is the default), `get_load_balancer_state`.

Safety and data:
- `are_nodes_safe_to_take_down <uuid1,uuid2> [follower_lag_bound_ms]` checks that taking tablet servers or masters down will not lose quorum; bound default 1000 ms. Available in 2024.2.8.0 and later, 2025.1.4.0 and later, and 2025.2.
- `compact_table <ysql|ycql>.<namespace> <table> [timeout-in-seconds] [ADD_INDEXES] [ADD_VECTOR_INDEXES]`: timeout default 20 seconds, `ADD_INDEXES` is YCQL only.
- `split_tablet <tablet-id>` splits a hash-sharded tablet at the middle of its sharding range.

Leader moves: `leader_stepdown <tablet-id> <dest-ts-uuid>` and `master_leader_stepdown` should be used only if Yugabyte support recommends it; `leader_stepdown` carries a possibility of downtime.

Snapshot, PITR, xCluster, encryption and CDC stream commands have their own sections on the yb-admin page.

## Checked

2026-11-09: syntax and defaults, the listed commands' arguments, the 15-minute catch-up rule, placement restrictions, compact_table defaults, are_nodes_safe_to_take_down and the stepdown warnings confirmed against the yb-admin reference page (yugabyte-db docs admin/yb-admin.md; the syntax section and each cited command section were read). Removed the unsourced advice to list every master so the leader is found and the unsourced claim about misusing change_config for masters; added the required PRE_VOTER/PRE_OBSERVER note and defaults from the page.

Method: docs-checked 2026-11-09 against yugabyte-db docs admin/yb-admin.md (command sections read, not the whole page)
