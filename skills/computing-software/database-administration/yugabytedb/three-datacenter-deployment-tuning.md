---
id: computing-software.database-administration.yugabytedb.three-datacenter-deployment-tuning
name: three-datacenter-deployment-tuning
category: computing-software
field: database-administration
product: yugabytedb
tags: [multi-dc, three-dc, leader-failure-max-missed-heartbeat-periods, raft-heartbeat-interval-ms, multi-region, preferred-zones]
level: advanced
status: docs-checked
description: "Deploy a 3DC YugabyteDB universe with one replica per data center, raise the Raft missed-heartbeat setting to 10, and optionally set a preferred leader zone."
sources: ["https://github.com/yugabyte/yugabyte-db/blob/master/docs/content/stable/deploy/multi-dc/3dc-deployment.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Three-datacenter deployment

A 3DC deployment extends the three-AZ deployment: an equal number of nodes in each of three data centers, ideally multi-AZ inside each. Any odd number of AZs or data centers works; an even number is not recommended because writes need a majority quorum. The page's example is RF 3 with one node and one replica in each of aws us-west-2a, us-east-1a and ap-northeast-1a.

Steps:
1. On every node start a yb-master and a yb-tserver with `--placement_cloud`, `--placement_region` and `--placement_zone` set for that node, `--rpc_bind_addresses` set to the host's private IP, a list of all masters (`--master_addresses` for masters, `--tserver_master_addrs` for tservers), and `--leader_failure_max_missed_heartbeat_periods 10` on both.
2. Run `yb-admin modify_placement_info aws.us-west.us-west-2a,aws.us-east-1.us-east-1a,aws.ap-northeast-1.ap-northeast-1a 3` (a cloud.region.zone list, then the replication factor). Until you do, the default policy treats all nodes as equal regardless of the `--placement_*` flags.
3. Optionally choose a preferred location with `yb-admin set_preferred_zones aws.us-west.us-west-2a`. Colocating leaders in one zone or region reduces cross-region network hops for multi-row and multi-table transactions. Run `modify_placement_info` first, because preferred zones must match existing placement blocks.
4. Raise failure detection for the higher RPC latency between data centers: `--leader_failure_max_missed_heartbeat_periods 10` instead of the default 6. The failure timeout is `--raft_heartbeat_interval_ms` (default 500 ms) multiplied by that value, so 5 seconds.

The larger value lengthens the failure detection interval, which the page says suits higher-latency deployments; it follows that a real leader failure is also detected later. The yb-master reference says to set 10 on all yb-tserver and yb-master configurations for read replica clusters too.

Check the result with `curl -s http://<any-master-ip>:7000/cluster-config`: `num_replicas: 3` and a placement block per zone with `min_num_replicas: 1`; after `set_preferred_zones` a `multi_affinitized_leaders` entry appears. By default, transaction status tablet leaders do not respect preferred zones (yb-admin reference).

## Checked

2026-11-04. Confirmed against the 3DC deployment page (odd number of data centers, example scenario, placement flags, leader_failure_max_missed_heartbeat_periods 10 and the 5 second timeout, modify_placement_info, set_preferred_zones, cluster-config output) and the yb-master reference (default 6, 500 ms heartbeat default, value 10 for read replica clusters) and yb-admin reference (preferred zones must match existing placement and transaction status tablet leaders). Removed: the RF 5 suggestion and the claim that writes always cost an inter-DC round trip, which the page does not state; the WAN jitter explanation was reduced to what the page says.

Method: documentation only; no commands were run.
