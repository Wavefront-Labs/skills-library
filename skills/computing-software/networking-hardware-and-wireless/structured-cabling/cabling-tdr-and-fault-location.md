---
id: computing-software.networking-hardware-and-wireless.structured-cabling.cabling-tdr-and-fault-location
name: cabling-tdr-and-fault-location
category: computing-software
field: networking-hardware-and-wireless
product: structured-cabling
tags: [cabling-tdr, tone-and-probe, cable-fault-location]
level: practitioner
status: draft
description: "Use TDR and tone/probe to find opens, shorts, split pairs and cross-connected ports quickly during install and fault finding."
sources:
  - https://tiaonline.org/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Fault location

- TDR sends a pulse and reads reflections: distance to the open/short is time-of-flight times NVP. Set NVP correctly.
- Split pairs pass a basic continuity test but fail NEXT; a wiremap that shows split pairs needs re-termination.
- Tone generator plus inductive probe traces unlabeled cables in bundles; tracing works best with the far end open.
- Link-and-port identification via a testers' switch-port discovery (LLDP/CDP/PoE detect) maps a wall jack to a switch port.
- A switch interface that flaps or shows CRC errors with a good wiremap is often a marginal link; certify it.

## Verify
- [ ] The located fault distance matches a physical inspection or a re-termination clears it.
