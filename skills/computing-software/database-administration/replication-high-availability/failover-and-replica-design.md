---
id: computing-software.database-administration.replication-high-availability.failover-and-replica-design
name: failover-and-replica-design
category: computing-software
field: database-administration
product: replication-high-availability
tags: [database-administration, replication-high-availability, high-availability, ha, failover, switchover, replication, synchronous-replication, asynchronous-replication, semi-synchronous, rpo, rto, split-brain, fencing, stonith, quorum, consensus, etcd, patroni, orchestrator, mysql-group-replication, innodb-cluster, always-on-availability-groups, data-guard, replica-lag, read-replicas, pgbouncer, proxysql, haproxy, connection-pooling, read-your-writes]
level: advanced
status: draft
description: "Design database HA: sync vs async replication against RPO/RTO, quorum and fencing to prevent split-brain, replica-lag-aware routing, pooling, with Patroni/Orchestrator/AG examples."
sources:
  - https://patroni.readthedocs.io/en/latest/
  - https://github.com/openark/orchestrator
  - https://learn.microsoft.com/en-us/sql/database-engine/availability-groups/windows/overview-of-always-on-availability-groups-sql-server
  - https://www.postgresql.org/docs/current/warm-standby.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Failover and replica design — decide the data-loss budget, then automate safely

**Goal:** an HA design whose data loss (RPO) and downtime (RTO) are stated numbers,
where failover cannot produce two primaries, and where applications follow the primary
and tolerate replica lag.

## 1. Start from RPO and RTO
| Mode | RPO | Write latency cost | Risk |
|---|---|---|---|
| Asynchronous | seconds of commits (whatever was unshipped) | none | lost writes on failover |
| Semi-sync (MySQL) | ~0 while a replica acks; falls back to async on timeout | +1 RTT | silent fallback (`rpl_semi_sync_source_timeout`) |
| Synchronous (Postgres `synchronous_standby_names`, AG synchronous-commit, Data Guard SYNC) | 0 for acknowledged commits | +1 RTT plus replica fsync | writes stall if sync replicas are lost |
Within one region (sub-ms RTT) synchronous to at least one replica is affordable. Across
regions, use async and accept an RPO, or a quorum of replicas
(`synchronous_standby_names = 'ANY 1 (r1, r2)'`) so one slow node doesn't stall writes.
Write the numbers down: "RPO 0 in-region, ≤ 30 s cross-region; RTO ≤ 60 s automatic".

Replication is not backup: a `DROP TABLE` replicates in milliseconds. See
computing-software.database-administration.database-backup-recovery.point-in-time-recovery-and-restore-testing.

## 2. Split-brain: quorum and fencing
Two nodes cannot safely decide who is primary; a network partition looks identical to a
dead peer. Rules:
- **Quorum:** the leader decision is held by a consensus store with an odd number of
  members (3 or 5) in at least 3 failure domains. Patroni uses etcd/Consul/ZooKeeper
  (or Kubernetes) leader keys with a TTL; Windows Server Failover Clustering gives AGs a
  quorum with a witness; MySQL Group Replication/InnoDB Cluster uses Paxos internally.
- **Fencing:** the old primary must stop accepting writes before the new one starts.
  Patroni demotes itself when it can't renew its leader key (and can use a watchdog to
  reboot a hung node). Elsewhere: STONITH, revoke the old primary's VIP/DNS, set it
  `read_only`/`super_read_only`, or block at the proxy.
- Two-datacentre setups without a third-site witness cannot fail over automatically
  without split-brain risk. Put the tiebreaker in a third location.

## 3. Automation examples
- **PostgreSQL + Patroni:** `patronictl -c <CONFIG> list`, `switchover`, `failover`.
  Key settings: `ttl: 30`, `loop_wait: 10`, `retry_timeout: 10`,
  `maximum_lag_on_failover` (bytes; don't promote a far-behind replica),
  `synchronous_mode: true` for RPO 0. Use `pg_rewind` (`use_pg_rewind: true`) so the
  old primary rejoins without a full rebuild.
- **MySQL + Orchestrator:** topology discovery and recovery with GTID-based
  repointing; pair with `super_read_only=ON` on replicas and a proxy (ProxySQL) for
  routing. Orchestrator is in maintenance mode upstream (check status and forks);
  MySQL InnoDB Cluster with MySQL Router is the vendor-integrated alternative.
- **SQL Server Always On AGs:** synchronous-commit replicas with automatic failover
  (limits on how many by version), plus asynchronous DR replicas; listener for routing;
  read-only routing for secondaries.

## 4. Routing and pooling
Applications should connect to a stable endpoint, never a node address:
- Postgres: libpq multi-host `host=<DB_HOST_1>,<DB_HOST_2> target_session_attrs=read-write`,
  HAProxy health-checking Patroni's REST API (`/primary`, `/replica?lag=10MB`), or a
  managed endpoint. PgBouncer in transaction mode in front to cap backend connections.
- MySQL: ProxySQL with hostgroups keyed on `read_only`; MySQL Router.
- Keep DNS TTLs low (≤ 30 s) if DNS is the switch, and know your driver caches DNS.
- Clients must retry on connection loss with backoff and be idempotent where possible.

## 5. Replica lag
Monitor: Postgres `pg_stat_replication.replay_lag` (on primary) or
`now() - pg_last_xact_replay_timestamp()` (on replica; misleading when idle); MySQL
`SHOW REPLICA STATUS` `Seconds_Behind_Source` (coarse; use a heartbeat table such as
`pt-heartbeat` for truth). Alert at a threshold tied to the RPO.
Read-your-writes: send a user's reads to the primary for a few seconds after they write,
or wait for the replica to reach the write's LSN/GTID
(`WAIT_FOR_EXECUTED_GTID_SET`). Long queries on Postgres replicas either get cancelled
or, with `hot_standby_feedback = on`, cause bloat on the primary; route analytics to a
dedicated replica.

## 6. Prove it
Run planned switchovers monthly and unplanned failover drills (kill the primary,
partition it) quarterly. Measure write-unavailability from the client side.

## Verify
- [ ] RPO/RTO are written down and the replication mode matches them.
- [ ] Leader election uses a 3+ member quorum across 3 failure domains.
- [ ] A partitioned old primary demonstrably stops accepting writes (fencing tested).
- [ ] Apps connect via a proxy/multi-host string and reconnect after failover without a deploy.
- [ ] Replica lag is graphed and alerted; failover refuses a replica beyond the lag limit.
- [ ] Last drill's measured RTO and data loss are recorded.
