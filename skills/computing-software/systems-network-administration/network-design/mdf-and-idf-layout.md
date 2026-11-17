---
id: computing-software.systems-network-administration.network-design.mdf-and-idf-layout
name: mdf-and-idf-layout
category: computing-software
field: systems-network-administration
product: network-design
tags: [network-design, mdf, idf, telecom-room, structured-cabling, tia-568, campus-design]
level: practitioner
status: draft
description: "Plan main and intermediate distribution frames: where they go, the 90 m horizontal limit, backbone fibre between them, rack layout, power, cooling and access control."
sources:
  - https://tiaonline.org/products-and-services/standards/
  - https://www.bicsi.org/standards
  - https://www.cisco.com/c/en/us/td/docs/solutions/Enterprise/Campus/campover.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# MDF and IDF layout

## Roles
- **MDF** (main distribution frame / equipment room): demarc for carriers, core/distribution
  switches, firewalls, often servers. One per building (campus MDF per site).
- **IDF** (telecom room / telecommunications enclosure): access switches and horizontal cabling
  for a floor or zone.

## Placement rules (TIA-568 / TIA-569)
- Horizontal copper channel max **100 m** (90 m permanent link + 10 m patch cords). Place IDFs so
  every outlet is within 90 m cable route (not straight line); plan with 10-15 % slack.
- At least one telecom room per floor; more if the floor exceeds about 1000 m2 or distances demand.
- Stack IDFs vertically where possible so backbone risers are short.
- Not in rooms with water pipes overhead, not beside electrical switchgear (EMI), lockable.

## Backbone
- Fibre between MDF and each IDF: OS2 single-mode for anything new (multi-mode OM4 within short
  buildings), at least 12 strands, two diverse paths for critical IDFs.
- Copper backbone only for legacy voice.

## Inside the room
- Racks: 42-48U, 800 mm wide for cable management, front/rear clearance >= 1 m.
- Order top to bottom: fibre panel, patch panels interleaved with switches (short patch leads),
  horizontal managers, UPS at the bottom.
- Power: dedicated circuits, UPS sized for PoE load, generator-backed where APs/phones/cameras must
  survive outages.
- Cooling: IDFs full of PoE switches can dissipate several kW; plan ventilation/AC and monitor
  temperature.
- Grounding/bonding bus per TIA-607.

## Verify
- [ ] Floor plan with IDF locations and measured 90 m radius, backbone fibre map with strand counts and paths, room checklist (power, cooling, lock, labels) signed off.
