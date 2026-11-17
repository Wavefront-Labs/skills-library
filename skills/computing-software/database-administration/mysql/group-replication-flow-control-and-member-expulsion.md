---
id: computing-software.database-administration.mysql.group-replication-flow-control-and-member-expulsion
name: group-replication-flow-control-and-member-expulsion
category: computing-software
field: database-administration
product: mysql
tags: [database-administration, mysql, group-replication-flow-control, group-replication, certifier-queue, applier-queue, member-expel-timeout, autorejoin-tries, exit-state-action, unreachable-majority-timeout]
level: practitioner
status: docs-checked
description: "Tune MySQL Group Replication flow control and failure detection: applier/certifier queue thresholds, expel timeouts, auto-rejoin and exit state actions."
sources:
  - https://dev.mysql.com/doc/refman/8.4/en/group-replication-flow-control.html
  - https://dev.mysql.com/doc/refman/8.4/en/group-replication-responses-failure-expel.html
  - https://dev.mysql.com/doc/refman/8.4/en/group-replication-responses-failure-rejoin.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Group Replication flow control and member expulsion

**Goal:** keep slow members from lagging unboundedly or being ejected by transient network blips, without stalling the whole group.

## Flow control
Each member reports its certifier and applier queue sizes. When any member's queue exceeds the threshold, writers throttle to the capacity of the slowest member.
```ini
group_replication_flow_control_mode = QUOTA          # or DISABLED
group_replication_flow_control_applier_threshold = 25000
group_replication_flow_control_certifier_threshold = 25000
group_replication_flow_control_min_quota = 0
group_replication_flow_control_period = 1
```
Monitor:
```sql
SELECT MEMBER_ID, COUNT_TRANSACTIONS_IN_QUEUE AS cert_queue, COUNT_TRANSACTIONS_REMOTE_IN_APPLIER_QUEUE AS applier_queue
FROM performance_schema.replication_group_member_stats;
```
Write throughput collapsing while one member's applier queue sits at the threshold: that member is slow (disk, CPU, single-threaded apply). Fix it (parallel applier: `replica_parallel_workers`, WRITESET) rather than disable flow control; disabling lets it fall arbitrarily behind and failovers then wait for it.

## Failure detection and expulsion
- A member silent for 5 s is suspected; after `group_replication_member_expel_timeout` more seconds (default 5) it is expelled.
- Raise to 10-30 s on networks with GC pauses / VM stalls / cloud blips. Longer means slower failover for real failures.
- `group_replication_autorejoin_tries` (default 3, 5 min apart): expelled members try to rejoin automatically.
- `group_replication_exit_state_action` (default `OFFLINE_MODE`; alternatives `READ_ONLY` and `ABORT_SERVER`): what a member does after leaving involuntarily; `OFFLINE_MODE` disconnects clients so they do not read stale data. `ABORT_SERVER` shuts mysqld down.
- `group_replication_unreachable_majority_timeout`: a minority partition leaves the group after N seconds instead of blocking forever.

## Large transactions
`group_replication_transaction_size_limit` (default 150000000 bytes, about 143 MB) rejects bigger transactions; huge transactions stall the group communication layer and can cause expulsions. Batch bulk operations; `group_replication_communication_max_message_size` fragments messages (10 MiB default).

## Verify
Throttle one member's disk in staging: flow control engages (writer TPS drops, queues capped), and an `iptables` drop of 3 s does not expel a member with a 10 s expel timeout.

## Checked

2026-10-31: confirmed on dev.mysql.com 8.4 pages: flow-control mode QUOTA/DISABLED (default QUOTA), applier and certifier thresholds default 25000, flow_control_min_quota default 0, flow_control_period default 1 s; the initial 5-second detection period and member_expel_timeout default 5 (responses-failure-expel); autorejoin tries default 3 with 5 minutes between attempts (responses-failure-rejoin); exit_state_action default OFFLINE_MODE with READ_ONLY and ABORT_SERVER (group-replication-system-variables); transaction_size_limit default 150000000 bytes (~143 MB, limitations page); communication_max_message_size default 10485760 bytes (10 MiB); the replication_group_member_stats queue columns. Corrected the 150 MB figure and removed the unconfirmed 8.0.21+/8.0.18+ version notes.
Method: documentation only; no commands were run.
