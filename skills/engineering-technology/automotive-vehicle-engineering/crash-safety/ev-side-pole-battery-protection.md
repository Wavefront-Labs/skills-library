---
id: engineering-technology.automotive-vehicle-engineering.crash-safety.ev-side-pole-battery-protection
name: ev-side-pole-battery-protection
category: engineering-technology
field: automotive-vehicle-engineering
product: crash-safety
tags: [pole-impact, side-pole, battery-protection, sill-extrusion, pack-intrusion, ev-crash]
level: practitioner
status: verified
description: "Protect an EV battery in a side pole impact: sill and crossmember strategy, intrusion limits to the pack, energy absorption and post-test HV checks."
sources:
  - "https://www.ecfr.gov/current/title-49/part-571/section-571.305a"
  - "UN Regulations 100 and 135, FMVSS 305, Euro NCAP side pole protocol; confirm current texts"
  - "Kramer, Passive Safety of Vehicles"
  - "https://www.law.cornell.edu/cfr/text/49/571.305"
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---

# EV side-pole battery protection

1. Risk: a narrow pole pushes through the sill and compresses the battery pack edge, which can short cells; a battery enclosure breach after a crash is a thermal-event hazard.
2. Strategy: absorb pole energy in the sill (multi-cell aluminium extrusions or high-strength steel profiles), and tie into floor cross-members and seat cross-beams so load spreads across the vehicle floor.
3. Pack protection: crush zones next to the pack (between the sill outer and pack), side frame members within the pack, structural cross-members inside the pack edge to resist intrusion; keep a clear clearance to cells.
4. Intrusion criteria: measure maximum intrusion into the pack envelope; many OEMs set a no-contact or limited-contact target at the defined pole speed.
5. Post-crash checks: isolation resistance, voltage, no fire, no electrolyte leakage, and no thermal event during an observation period (observation period per the regulation or consumer test (gated: unconfirmed, source is paywalled or blocked)).
6. CAE: model the pole with a detailed battery pack representation, including cells' failure thresholds; correlate with component pole/crush tests of the pack.
7. Include other load cases: side MDB, rear impact, underbody strike.

**Gotchas:** sill-to-floor joint stiffness; pole-hit location along the sill.

## Verify
- [ ] Pack intrusion below the target at the pole speed in CAE and test.
- [ ] Post-test isolation and thermal observation criteria pass.
