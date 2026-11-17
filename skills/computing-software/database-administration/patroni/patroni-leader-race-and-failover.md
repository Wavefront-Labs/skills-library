---
id: computing-software.database-administration.patroni.patroni-leader-race-and-failover
name: patroni-leader-race-and-failover
category: computing-software
field: database-administration
product: patroni
tags: [patroni, ha, failover, leader-lock, dcs]
level: intro
status: docs-checked
description: "How Patroni uses a TTL leader lock in the DCS to run leader races and automatic failover, and what the DCS holds."
sources:
  - https://patroni.readthedocs.io/en/latest/faq.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: understand why Patroni promotes a node and what state it trusts.

Patroni relies on the DCS (Distributed Configuration Store) as the source of truth, unlike tools such as repmgr where nodes talk to each other to decide actions.

Failover flow:
- The cluster state includes a leader lock holding the name of the current leader member. The lock has a time-to-live.
- If the leader fails to renew the lease within `ttl`, the key expires and a leader race starts.
- All nodes check whether they are the best candidate; some checks call the REST API of the other members.
- Every member that finds itself best attempts to take the lock. The first to get it promotes itself (or becomes standby leader); the others are configured to follow it.

Related facts from the FAQ:
- Patroni also self-heals: a failed former primary is rejoined as a replica of the new primary, and failed replicas are rejoined.
- Patroni runs Postgres through binaries such as pg_ctl and postgres, so disable other managers such as the postgresql systemd unit. A unit that restarts a failed primary can cause split-brain.
- Do not restart Postgres directly; bouncing it without Patroni can cause failovers.
- Patroni does not require a minimum number of Postgres nodes.
- Two clusters may share one DCS if their `namespace` and `scope` differ; a clash with a different system identifier makes the second cluster abort management.

## Checked

2026-11-08. Confirmed every statement against the Patroni FAQ (read in full): comparison with other HA solutions, DCS, Postgres management and automatic failover sections. Reworded the node-count line to the FAQ's own claim.

Method: documentation only; no commands were run.
