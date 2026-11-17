---
id: computing-software.database-administration.yugabytedb.cluster-move-to-new-nodes
name: cluster-move-to-new-nodes
category: computing-software
field: database-administration
product: yugabytedb
tags: [cluster-move, change-cluster-config, change-master-config, blacklist, migration, get-load-move-completion, yb-admin]
level: advanced
status: docs-checked
description: "Move a whole YugabyteDB cluster to new machines online: start new masters in standby, blacklist old tservers, wait for 100 percent, then swap the master config."
sources: ["https://github.com/yugabyte/yugabyte-db/blob/master/docs/content/stable/manage/change-cluster-config.md", "https://github.com/yugabyte/yugabyte-db/blob/master/docs/content/stable/admin/yb-admin.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Moving a cluster to new nodes

Planned moves (for example machine type A to B) can be done online.

1. Start new masters without `--master_addresses` so they are standbys and do not join the old quorum.
2. Start new tservers with `--tserver_master_addrs` listing the old masters together with the new ones, then check on the master UI `/tablet-servers` page that old and new tservers are all ALIVE.
3. Blacklist every old tserver so the balancer drains it:
```
yb-admin --master_addresses <masters> change_blacklist ADD <old-ip>:9100 <old-ip2>:9100
```
4. Poll `yb-admin get_load_move_completion` until it reports 100.
5. Move the master quorum one server at a time:
```
yb-admin --master_addresses <masters> change_master_config ADD_SERVER <new-ip> 7100
yb-admin --master_addresses <masters> change_master_config REMOVE_SERVER <old-ip> 7100
yb-admin --master_addresses <masters> list_all_masters
```
Alternate one add and one remove until only new masters remain, checking the master UI after every step, then run `list_all_masters` and confirm the leader is a new master.
6. Set `--tserver_master_addrs` on the new tservers to the three new masters so restarts use the final list, then shut down the old nodes.
7. After the old tservers are terminated, clean up with `change_blacklist REMOVE` and check that `get_universe_config` shows no `server_blacklist` entries.

Change masters one at a time. Stopping old nodes before `get_load_move_completion` reaches 100 risks under-replication. DEAD tservers can stay listed for 24 hours by default (`hide_dead_node_threshold_mins`); `master_leader_stepdown` refreshes the cache.

## Checked

2026-11-04. Confirmed against the Change cluster configuration page (new masters started without master_addresses, tserver_master_addrs including old and new masters, change_blacklist ADD, get_load_move_completion until 100, alternating ADD_SERVER and REMOVE_SERVER, list_all_masters, final tserver_master_addrs, blacklist cleanup, 24 hour dead-node cache) and the yb-admin reference. Removed the unsupported 'same placement flags' step and the are_nodes_safe_to_take_down advice (that command is documented only for 2024.2.8.0 and later, 2025.1.4.0 and later, and 2025.2). Replaced the dead troubleshoot/cluster/recover/server.md source (404).

Method: documentation only; no commands were run.
