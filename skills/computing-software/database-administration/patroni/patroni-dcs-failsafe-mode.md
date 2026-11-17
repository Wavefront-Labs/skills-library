---
id: computing-software.database-administration.patroni.patroni-dcs-failsafe-mode
name: patroni-dcs-failsafe-mode
category: computing-software
field: database-administration
product: patroni
tags: [patroni, failsafe-mode, dcs, split-brain, availability]
level: advanced
status: docs-checked
description: "Enable failsafe_mode so the primary survives a DCS outage if it can reach all members through the REST API."
sources:
  - https://patroni.readthedocs.io/en/latest/dcs_failsafe_mode.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: avoid demoting the primary when only the DCS is down.

Normally, if the leader lock cannot be updated, Postgres is demoted and started read-only, because a single node cannot tell network partitioning from a DCS outage. Failsafe mode lets the primary keep running when the lock update fails for reasons other than a version/value/index mismatch, provided it can access all known cluster members via the Patroni REST API.

Enable it only through the global dynamic configuration stored in the DCS `/config` key:

```
patronictl edit-config -s failsafe_mode=true
```

or `PATCH /config`. Make sure all members run an up-to-date Patroni version first.

Implementation:
- A permanent `/failsafe` key in DCS holds all known members and is maintained by the current leader. A member can join the leader race only if it is in this key; a single-node cluster lists one member.
- During an outage the primary calls `POST /failsafe` on every member and may continue as primary only if all acknowledge. If one does not respond, it is demoted.
- Replicas treat these requests as proof the primary is alive, cached for `ttl` seconds, so they do not start a leader race even if the lock expired.
- The check runs every `loop_wait` seconds, so if a node is terminated during the outage Postgres is demoted to read-only until the DCS returns.
- Quorum is not used because Patroni nodes need not be evenly spread across zones, unlike DCS nodes.

## Checked

2026-11-08. Confirmed against the Patroni DCS failsafe mode page (read in full). Removed the "default false" note, which the page does not state.

Method: documentation only; no commands were run.
