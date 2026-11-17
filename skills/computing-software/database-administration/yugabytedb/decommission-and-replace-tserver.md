---
id: computing-software.database-administration.yugabytedb.decommission-and-replace-tserver
name: decommission-and-replace-tserver
category: computing-software
field: database-administration
product: yugabytedb
tags: [blacklist, change-blacklist, decommission, replace-tserver, get-load-move-completion, scale-in, yb-admin]
level: practitioner
status: docs-checked
description: "Drain a YB-TServer with change_blacklist, track get_load_move_completion to 100 percent, then stop the node and remove it from the blacklist."
sources: ["https://github.com/yugabyte/yugabyte-db/blob/master/docs/content/stable/admin/yb-admin.md", "https://github.com/yugabyte/yugabyte-db/blob/master/docs/content/stable/manage/change-cluster-config.md", "https://github.com/yugabyte/yugabyte-db/blob/master/docs/content/stable/architecture/docdb-sharding/cluster-balancing.md", "https://github.com/yugabyte/yugabyte-db/blob/master/docs/content/stable/troubleshoot/cluster/replace_tserver.md", "https://github.com/yugabyte/yugabyte-db/blob/master/docs/content/stable/troubleshoot/cluster/recover_server.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Decommission and replace a tserver

Use this to retire a node or swap a failed one.

1. Install and start the replacement YB-TServer, in the same placement group as the one you are replacing. Loading and rebalancing complete only if data from the old server has somewhere to go: start the new server first, or make sure the remaining servers have enough capacity and are in the correct placement zones.
2. Blacklist the old node:
```
yb-admin --master_addresses $MASTERS change_blacklist ADD $OLD_IP:9100
```
3. Wait for data to move off. Poll until it reports 100 percent:
```
yb-admin --master_addresses $MASTERS get_load_move_completion
```
4. When the move reaches 100 percent, stop the yb-tserver process or terminate the VM. The master leader marks the server DEAD after it has not responded for one minute (`tserver_unresponsive_timeout_ms`, default 60000); check `$MASTER_LEADER_IP:7000/tablet-servers`. Dead servers can stay listed for 24 hours by default (`hide_dead_node_threshold_mins`), and `yb-admin master_leader_stepdown` refreshes the cache.
5. Once the old tserver is terminated, remove its address from the blacklist (this helps if the IP address is recycled):
```
yb-admin --master_addresses $MASTERS change_blacklist REMOVE $OLD_IP:9100
```

If a tserver fails permanently without draining, the cluster balancer starts creating new replicas elsewhere once the node has been down for `follower_unavailable_considered_failed_sec` (15 minutes by default). `yb-admin are_nodes_safe_to_take_down <server-uuids> [follower_lag_bound_ms]` (default bound 1000 ms) checks that taking nodes down will not lose quorum; the reference lists it for 2024.2.8.0 and later, 2025.1.4.0 and later, and 2025.2. Get UUIDs from `list_all_tablet_servers` and `list_all_masters`.

Set up cron or systemd so yb-master and yb-tserver restart after transient failures such as a reboot or crash; `sudo systemctl list-units --type=service | grep yb` lists the unit names. For a permanent node failure, start another YB-TServer on a new node and the cluster balancer rebalances tablets to it.

## Checked

2026-11-04. Confirmed against the yb-admin reference (`change_blacklist ADD|REMOVE ip:port`, `get_load_move_completion` until 100, `are_nodes_safe_to_take_down` syntax, default 1000 ms and version gates), the Change cluster configuration page (blacklist then wait for the move, DEAD status of old tservers, blacklist cleanup for recycled IPs, 24 hour dead-node cache) and the cluster balancing page (15 minute delay before re-replication). The Replace a failed YB-TServer page (read from raw GitHub; the originally cited URL used a wrong path) confirms the same-placement-group requirement, the one-minute DEAD timeout, and the blacklist cleanup; the Recover failed YB-TServer and YB-Master page confirms cron or systemd monitoring and the unit listing command. Corrected the two source URLs to the live paths (replace_tserver.md and recover_server.md).

Method: documentation only; no commands were run.
