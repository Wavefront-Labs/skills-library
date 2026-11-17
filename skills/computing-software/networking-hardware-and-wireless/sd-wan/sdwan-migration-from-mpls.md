---
id: computing-software.networking-hardware-and-wireless.sd-wan.sdwan-migration-from-mpls
name: sdwan-migration-from-mpls
category: computing-software
field: networking-hardware-and-wireless
product: sd-wan
tags: [mpls-to-sdwan-migration, sdwan-coexistence, wan-cutover]
level: advanced
status: draft
description: "Plan an MPLS-to-SD-WAN migration: coexistence at hubs, pilot sites, route preference during cutover and rollback."
sources:
  - https://www.mef.net/
  - https://www.cisco.com/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# MPLS to SD-WAN migration

- Inventory sites, circuits, applications and QoS needs; decide which circuits stay (hybrid) and contract end dates.
- Coexistence: a hub or gateway site runs both MPLS and the SD-WAN overlay and redistributes routes; control route preference and avoid loops (tags, filters).
- Pilot with two or three sites; validate apps, voice and failover; then migrate in waves with a rollback path (keep MPLS handoff until stable).
- Order broadband circuits early; install lead time is the usual critical path.
- Update monitoring, runbooks, and change-control before the first wave.

## Verify
- [ ] Post-cutover tests show application performance equal to or better than baseline, and rollback was rehearsed.
