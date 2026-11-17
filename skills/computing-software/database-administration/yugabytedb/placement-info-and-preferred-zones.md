---
id: computing-software.database-administration.yugabytedb.placement-info-and-preferred-zones
name: placement-info-and-preferred-zones
category: computing-software
field: database-administration
product: yugabytedb
tags: [placement, modify-placement-info, preferred-zones, leader-affinity, cluster-config, yb-admin, multi-zone]
level: advanced
status: docs-checked
description: "Set replica placement with yb-admin modify_placement_info and steer leaders with set_preferred_zones, then verify through cluster-config."
sources: ["https://github.com/yugabyte/yugabyte-db/blob/master/docs/content/stable/deploy/multi-dc/3dc-deployment.md", "https://github.com/yugabyte/yugabyte-db/blob/master/docs/content/stable/admin/yb-admin.md", "https://github.com/yugabyte/yugabyte-db/blob/master/docs/content/stable/architecture/docdb-sharding/cluster-balancing.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Placement info and preferred zones

Placement controls which cloud, region and zone hold replicas. Each node declares its location with `--placement_cloud`, `--placement_region` and `--placement_zone`, but the default policy when a universe is created treats all nodes as equal regardless of those flags, so you must set the policy explicitly.

Set the policy:
```
yb-admin --master_addresses m1:7100,m2:7100,m3:7100 modify_placement_info aws.us-west.us-west-2a,aws.us-west.us-west-2b,aws.us-west.us-west-2c 3
```
The trailing number is the replication factor. Each entry is `cloud.region.zone[:min[:max]]`: the minimum (default 1) is how many replicas of each tablet must go in that block, and the optional maximum is a hard cap, allowed only when every block is fully qualified (no wildcards). The RF must be at least the sum of the minimums and at most the sum of the maximums. `*` wildcards are allowed, for example `aws.*.*:5 5` or `aws.us-east-1.*:3 3`. Verify with `curl -s http://<any-master-ip>:7000/cluster-config`, where `min_num_replicas` reflects the setting.

For YCQL tables and transaction status tables use `modify_table_placement_info`; for YSQL tables use `CREATE TABLESPACE` instead. Table placement is not supported on clusters with read replicas or leader affinity policies, and tablespaces do not inherit cluster-level placement, leader preference or read replica configuration.

Leader affinity: `yb-admin set_preferred_zones aws.us-west.us-west-2a` makes the cluster balancer place tablet leaders on healthy replicas in those zones, which reduces network hops for transactional writes. Run `modify_placement_info` first; preferred zones must match existing placement blocks. Zones take an optional rank (`zone:<preference>`, contiguous integers from 1, default 1): rank 2 is used when no healthy replica exists in rank 1. Zones you omit are used only after every ranked zone is exhausted. The list is stored as `multi_affinitized_leaders` in the cluster config (older clusters may show `affinitized_leaders`). The command does not change replica placement, and by default transaction status tablet leaders ignore preferred zones. With a smart driver set the topology keys to target the preferred zones.

`change_leader_blacklist ADD|REMOVE <ip_addr>:<port>` adds or removes a server from the leader blacklist; leader-blacklisted nodes host no leaders regardless of preference, and `get_leader_blacklist_completion` reports the move completion percentage.

To change the policy later, rerun `modify_placement_info` with the new list and RF. The cluster balancer works toward the new policy (its `tablets_in_wrong_placement` metric counts peers on servers outside the policy), and `get_load_move_completion` reports the data move as a percentage; rerun it until it reaches 100.0. If a placement policy cannot be satisfied, for example because no tservers exist in the requested zone, the cluster balancer reports a warning.

## Checked

2026-11-04. Confirmed against the yb-admin reference (modify_placement_info syntax with min and max, wildcards, cluster-config check; set_preferred_zones ranks and notes; modify_table_placement_info YCQL-only note; change_leader_blacklist and get_leader_blacklist_completion; get_load_move_completion), the 3DC deployment page (default policy ignores placement flags, modify_placement_info, multi_affinitized_leaders appears after set_preferred_zones) and the cluster balancing page (placement policy overview, tablets_in_wrong_placement, unsatisfied-policy warning). Removed: 'useful before maintenance' and 'without moving its data' for the leader blacklist (not stated); 'the balancer move leaders' wording was tightened to what the reference says.

Method: documentation only; no commands were run.
