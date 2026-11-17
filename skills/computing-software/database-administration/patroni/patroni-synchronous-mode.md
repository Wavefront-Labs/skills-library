---
id: computing-software.database-administration.patroni.patroni-synchronous-mode
name: patroni-synchronous-mode
category: computing-software
field: database-administration
product: patroni
tags: [patroni, synchronous-mode, replication, durability, strict-mode]
level: practitioner
status: docs-checked
description: "Enable Patroni synchronous_mode and synchronous_mode_strict, and what each guarantees and costs."
sources:
  - https://patroni.readthedocs.io/en/latest/replication_modes.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: avoid losing committed transactions at failover.

Set `synchronous_mode: on` in dynamic configuration (via `patronictl edit-config` or REST). Patroni then manages `synchronous_standby_names` and will not promote a standby unless certain it holds every transaction that may have been acknowledged to a client. The cost is possible loss of write availability.

Behaviours:
- It does not guarantee multi-node durability in all cases. With no suitable standby, the primary still accepts writes without guaranteeing replication. If the primary then fails, no standby is promoted; when the old primary returns it is promoted automatically unless an administrator did a manual failover. This makes it usable with 2-node clusters.
- If a standby crashes, commits block until the next Patroni iteration switches the primary to standalone (worst case `ttl` seconds, average `loop_wait/2`).
- Manually stopping or restarting a standby does not interrupt commits; it signals the primary to release it before PostgreSQL shutdown.
- `synchronous_mode_strict` prevents Patroni from switching off synchronous replication when no candidates exist, blocking client writes until a synchronous replica returns.
- Even in strict mode, a cancelled backend waiting for acknowledgement can leave visible but unreplicated changes.

Use `nosync: true` (or `nostream`) tags on standbys over slow links. Plain PostgreSQL sync replication (`synchronous_commit: "on"`, `synchronous_standby_names: "*"`) needs at least three data nodes.

## Checked

2026-11-08. Confirmed against the Patroni replication modes page (synchronous mode, PostgreSQL synchronous replication, strict mode, nosync/nostream). Removed the claim about who may take part in a leader race, which the page does not state in those terms.

Method: documentation only; no commands were run.
