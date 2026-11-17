---
id: computing-software.database-administration.patroni.patroni-dcs-loss-recovery
name: patroni-dcs-loss-recovery
category: computing-software
field: database-administration
product: patroni
tags: [patroni, dcs, outage, recovery, patroni-dynamic-json]
level: advanced
status: docs-checked
description: "What happens when the DCS is lost or loses majority, and how Patroni rebuilds state afterward."
sources:
  - https://patroni.readthedocs.io/en/latest/faq.html
  - https://patroni.readthedocs.io/en/latest/dcs_failsafe_mode.html
  - https://patroni.readthedocs.io/en/latest/rest_api.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: predict and recover from DCS failures.

Effects:
- Losing the DCS or its majority makes it unresponsive. Patroni demotes the current read/write node and all clusters depending on it go read-only, unless DCS failsafe mode is enabled.
- `patronictl list` is built from DCS data; a member that vanishes from it is probably not running or cannot reach the DCS, and its data expires. Data can lag by up to `loop_wait` seconds.

Recovery outcomes:
1. DCS fully recovered: nothing to do.
2. DCS re-created in place with the same endpoints: no changes.
3. New DCS with different endpoints: update the endpoints in the Patroni configuration of every node.

In cases 2 and 3 Patroni recreates status information from the current cluster state and recreates dynamic configuration from `patroni.dynamic.json`, stored in each member's data directory.

If all members are lost while the DCS is down, Patroni can be configured to create a new replica from backup even without a leader, but a member not present in the `/failsafe` key cannot take the leader lock.

Metrics `patroni_cluster_unlocked` and `patroni_dcs_last_seen` expose lock and contact state. Keys created by the same `namespace` and `scope` for a different system identifier make the second cluster abort management.

## Checked

2026-11-08. Confirmed against the Patroni FAQ (DCS section, patronictl list questions), the DCS failsafe mode page (FAQ on losing all members) and the REST API page (`/metrics` metric names). Pages read in full.

Method: documentation only; no commands were run.
