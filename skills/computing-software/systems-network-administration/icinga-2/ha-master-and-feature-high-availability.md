---
id: computing-software.systems-network-administration.icinga-2.ha-master-and-feature-high-availability
name: ha-master-and-feature-high-availability
category: computing-software
field: systems-network-administration
product: icinga-2
tags: [systems-network-administration, icinga-2, high-availability, secondary-master, enable-ha, checker, notification, ido, failover-timeout]
level: advanced
status: docs-checked
description: "Build an HA Icinga 2 master zone with two endpoints and understand feature HA, enable_ha and failover_timeout."
sources:
  - https://icinga.com/docs/icinga-2/latest/doc/06-distributed-monitoring/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# HA master and feature high availability
You can start with one master and add a secondary later; that needs an extra initial sync step to clone runtime state.

HA master: put two endpoints in the `master` zone. On master1: `Endpoint "icinga2-master2.localdomain" { host = ... }` (actively connects) and a zone listing both. The secondary does not set `host` for master1 because the first master already connects. Agents only need the parent zone and its endpoint members; if the master endpoints have a `host` attribute the agent connects actively.

Consequences of two nodes in one zone:
- Checks and notifications are balanced between them, so plugins and notification scripts must exist on both.
- The `checker` feature must be enabled on all instances in the zone (`icinga2 feature enable checker`); if one stops, the others take over its checks.
- `notification` must be enabled on all; notifications are load-balanced by default. `enable_ha = false` in the NotificationComponent makes nodes notify independently, which duplicates notifications unless handled.
- DB IDO runs active on one node only; others disable their connection at runtime, and the active node is not necessarily the zone master. Use a shared database, or set `enable_ha = false` on the IDO object on all nodes to write local databases. If the active node dies a new one is elected; `failover_timeout` cannot be lower than 60 seconds. Check which endpoint writes with `SELECT status_update_time, endpoint_name FROM icinga_programstatus;`.

## Checked

Method: docs-only read of cited pages, 2026-11-08

Read the full page https://icinga.com/docs/icinga-2/latest/doc/06-distributed-monitoring/. No commands were run.
