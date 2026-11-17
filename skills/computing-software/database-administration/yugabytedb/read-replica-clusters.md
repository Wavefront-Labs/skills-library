---
id: computing-software.database-administration.yugabytedb.read-replica-clusters
name: read-replica-clusters
category: computing-software
field: database-administration
product: yugabytedb
tags: [read-replicas, observer, add-read-replica-placement-info, placement-uuid, modify-placement-info, follower-reads, multi-region]
level: advanced
status: docs-checked
description: "Add an asynchronous read replica cluster for low-latency remote reads: placement uuid, add_read_replica_placement_info, tserver flags, and the heartbeat setting."
sources: ["https://github.com/yugabyte/yugabyte-db/blob/master/docs/content/stable/architecture/docdb-replication/read-replicas.md", "https://github.com/yugabyte/yugabyte-db/blob/master/docs/content/stable/deploy/multi-dc/read-replica-clusters.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Read replica clusters

Read replicas are observers: they do not participate in writes or in Raft consensus, and get a timeline-consistent copy of the data through asynchronous replication, so they do not add to write latency. Applications read from them using follower reads; writes sent there are redirected to the primary, and schema changes are applied to them transparently (no separate DDL). A read replica cluster has its own RF, which may be even because it does not take part in consensus.

Manual setup:
1. Start the primary masters and let them form a quorum, then set the primary placement policy with an optional placement uuid (any meaningful string):
```
yb-admin --master_addresses <masters> modify_placement_info <cloud.region.zone,...> <rf> <primary_uuid>
```
2. Define the replica placement (the zones must differ from the primary's zones; the page suggests a suffix such as `c1.r1.z1_rr:2` to reuse the same cloud, region and zone, and the RF is the total number of read replicas):
```
yb-admin --master_addresses <masters> add_read_replica_placement_info cloud.region.zone:1,cloud.region2.zone:1 <replica_rf> <replica_uuid>
```
3. Start the primary yb-tservers with `--placement_cloud`, `--placement_region`, `--placement_zone` and `--placement_uuid=<primary_uuid>` matching step 1 (the placement flags are not needed on the masters).
4. Start the read-replica yb-tservers with the same flags, using `--placement_uuid=<replica_uuid>` and values matching step 2. The primary then begins asynchronous replication to the read replica cluster.

With yugabyted add nodes with `yugabyted start --join=<primary_host> --read_replica --cloud_location=<cloud.region.zone>` (for a secure cluster, first generate node certificates with `yugabyted cert generate_server_certs --hostnames=<ip,...>` and copy them to the replica nodes).

A read from a replica must be a follower read: with follower reads off, the read goes to the tablet leader in the primary cluster. In YSQL set `yb_read_from_followers` and mark the transaction read only; in YCQL use consistency level ONE and set the application's local data center to the replica's region.

## Checked

2026-11-04. Confirmed against the Read replicas architecture page (observers, async replication, timeline consistency, independent RF including even values, write redirection, transparent schema changes) and the Deploy read replica clusters page (modify_placement_info and add_read_replica_placement_info syntax with optional placement_uuid, distinct zones and the _rr suffix tip, tserver placement flags, yugabyted --join --read_replica, cert generation, follower read requirements). Removed: `--tserver_master_addrs` for replica tservers and `leader_failure_max_missed_heartbeat_periods=10` (the latter appears only on the 3DC page, not on either cited page), 'set a staleness larger than the typical replica lag' (not stated), and the cluster-config check. Corrected the placement uuid placement flags to tservers only.

Method: documentation only; no commands were run.
