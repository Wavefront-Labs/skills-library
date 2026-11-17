---
id: computing-software.database-administration.mysql.replica-promotion-and-orchestrator-failover
name: replica-promotion-and-orchestrator-failover
category: computing-software
field: database-administration
product: mysql
tags: [database-administration, mysql, orchestrator-mysql, failover, replica-promotion, orchestrator, gtid, read-only, topology-recovery]
level: practitioner
status: draft
description: "Promote a MySQL replica to source manually or with Orchestrator: choose the most advanced replica, repoint others via GTID, fence the old source, move traffic."
sources:
  - https://github.com/openark/orchestrator/tree/master/docs
  - https://dev.mysql.com/doc/refman/8.4/en/replication-solutions-switch.html
  - https://dev.mysql.com/doc/refman/8.4/en/server-system-variables.html#sysvar_super_read_only
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Switching sources during failover (Orchestrator / manual promotion)

For classic async/semisync topologies (not InnoDB Cluster/Group Replication, which elect automatically).

## Manual promotion with GTIDs
1. **Fence the old source** if it is still reachable: `SET GLOBAL super_read_only = ON;` or stop it / cut its network. Two writable sources = split brain.
2. Pick the replica with the most transactions:
   ```sql
   SELECT @@GLOBAL.gtid_executed;          -- on each candidate
   SELECT GTID_SUBSET('<set_A>', '<set_B>');   -- 1 = A contained in B
   ```
   Also prefer replicas with the same version/config and no replication filters.
3. Let it finish applying its relay log: `SHOW REPLICA STATUS\G` until `Retrieved_Gtid_Set` is contained in `Executed_Gtid_Set`.
4. Promote:
   ```sql
   STOP REPLICA; RESET REPLICA ALL;
   SET PERSIST super_read_only = OFF; SET PERSIST read_only = OFF;
   ```
5. Repoint the other replicas:
   ```sql
   STOP REPLICA;
   CHANGE REPLICATION SOURCE TO SOURCE_HOST='new-source', SOURCE_AUTO_POSITION=1;
   START REPLICA;
   ```
6. Move traffic: VIP, DNS, ProxySQL hostgroup, or Router/HAProxy config.
7. Old source later: rebuild it as a replica, or if it has **errant transactions** (GTIDs not on the new source), inspect and discard them before re-attaching (`gtid_executed` diff).

## Orchestrator
Discovers the topology from replicas' status and recovers automatically or on command.
```bash
orchestrator-client -c topology -i db1:3306
orchestrator-client -c graceful-master-takeover-auto -a cluster1      # planned switchover
orchestrator-client -c recover -i db1:3306                            # manual recovery of a dead primary
orchestrator-client -c relocate -i db3:3306 -d db2:3306               # move a replica
```
Config essentials (`orchestrator.conf.json`): `RecoverMasterClusterFilters` (enable automatic failover for listed clusters), `PreventCrossDataCenterMasterFailover`, `DetectClusterAliasQuery`, and hooks `PreFailoverProcesses` / `PostMasterFailoverProcesses` to fence the old primary and update VIP/ProxySQL. Run Orchestrator itself in raft mode (3 nodes) so it is not a single point of failure.

Orchestrator is archived upstream (openark); forks and alternatives exist (Percona's fork, MySQL InnoDB Cluster/ReplicaSet, Vitess VTOrc). Pick one that is maintained for new builds.

## Gotchas
- With async replication the newest replica may still miss the old source's last transactions; semisync (`rpl_semi_sync_source_wait_point = AFTER_SYNC`) reduces that to ~0.
- `read_only` alone does not stop accounts with `SUPER`/`CONNECTION_ADMIN`; use `super_read_only` on all replicas.
- Applications caching connections keep writing to the old source unless it is fenced; fencing is step 1 for a reason.
