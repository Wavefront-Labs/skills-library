---
id: computing-software.database-administration.replication-high-availability.failover-drills-and-measured-rto
name: failover-drills-and-measured-rto
category: computing-software
field: database-administration
product: replication-high-availability
tags: [database-administration, high-availability, failover, failover-drill, rto-measurement, switchover-test, game-day, chaos-testing, rpo-verification]
level: advanced
status: draft
description: "Run scheduled database failover drills that measure real RTO and RPO end to end (detection, promotion, routing, app recovery) instead of trusting the HA design."
sources:
  - https://sre.google/sre-book/testing-reliability/
  - https://patroni.readthedocs.io/en/latest/patronictl.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Failover drills with measured RTO

**Goal:** a number, measured last quarter, for "how long are writes down when the
primary dies", and confidence that it still works after every infra change.

## What to measure (timeline per drill)
| Mark | Source |
|---|---|
| T0 failure injected | drill script log |
| T1 failure detected | HA manager log (Patroni/Orchestrator/AG/Data Guard broker) |
| T2 new primary promoted | DB log (`selected new timeline`, AG role change) |
| T3 routing updated | proxy/DNS/VIP log, health check flips |
| T4 app writes succeed again | synthetic writer: inserts a row every 100 ms with a timestamp |
RTO = T4 − T0. RPO = last row written before T0 that is missing after failover
(the synthetic writer's sequence numbers show gaps).

## Drill types (increasing realism)
1. **Planned switchover** (`patronictl switchover`, `ALTER AVAILABILITY GROUP ... FAILOVER`,
   `dgmgrl switchover to`): monthly, low risk.
2. **Process kill** on the primary (`kill -9` postmaster/mysqld): tests detection and fencing.
3. **Host loss / network partition** (power off VM, iptables drop between primary and others):
   tests quorum and split-brain protection; check the isolated old primary
   stops accepting writes.
4. **Zone or region loss** (game day): includes DNS, credentials, runbooks, people.

## Procedure
- Announce, pick a low-traffic window, have rollback (switch back) ready.
- Start the synthetic writer and reader against the production entry point.
- Inject failure, record timestamps, do not intervene unless thresholds are breached.
- Afterwards: rejoin old primary as replica, verify replication healthy.
- Write up: measured RTO/RPO vs targets, surprises (connection pools not
  reconnecting, cached DNS, cron jobs pinned to a host, monitoring alerts missing).

## Common findings
- App connection pools keep dead connections: need validation/timeouts (`socketTimeout`, `tcp_keepalives_*`).
- RTO dominated by DNS TTL or client retry backoff, not the database.
- Old primary came back writable (no fencing): fix before the next real incident.

## Verify
Drill records exist for each critical cluster within the last quarter, each with
measured RTO/RPO within targets or a tracked fix.
