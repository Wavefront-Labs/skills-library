---
id: engineering-technology.automotive-vehicle-engineering.crash-safety.side-impact-test-protocols
name: side-impact-test-protocols
category: engineering-technology
field: automotive-vehicle-engineering
product: crash-safety
tags: [side-impact, fmvss-214, un-r95, un-r135, moving-deformable-barrier, side-pole, es-2]
level: practitioner
status: gated
description: "Map side-impact tests (MDB and pole) under FMVSS 214, UN R95/R135 and consumer programmes, with dummies, speeds and the structural implications."
sources:
  - "FMVSS 214 (nhtsa.gov), UN Regulations 95 and 135 (unece.org), Euro NCAP and IIHS side protocols; confirm current versions"
  - "https://www.law.cornell.edu/cfr/text/49/571.214"
licence: Apache-2.0
version: 5
updated: 2026-11-17
aliases: []
---

# Side impact test protocols

Confirm all speeds, barrier masses and dummies in the current protocols; they change with updates.

- **Moving deformable barrier (MDB) tests:** FMVSS 214 uses an MDB at 53 +/- 1 km/h, crabbed (barrier path 63 degrees to the vehicle centreline, wheels 27 degrees; 49 CFR 571.214 S7), with ES-2re (50th male) and SID-IIs (5th female) dummies; UN R95 uses an MDB at about 50 km/h perpendicular to the side (gated: unconfirmed, source is paywalled or blocked; unece.org returned 403). Consumer programmes use similar or higher-severity barrier tests with updated barrier face stiffness and mass.
- **Pole tests:** vehicle driven sideways into a narrow rigid pole at about 32 km/h (UN R135; gated: unconfirmed, unece.org returned 403). FMVSS 214 pole test: up to 32 km/h, 75 or 285 degrees (+/- 3) to the centreline, 254 mm rigid pole, dummy chosen by NHTSA to assess head and thorax protection at the pole location.
- Dummies and measures: head injury (HIC), chest deflection and rib viscous criterion (V*C), abdomen force, pelvis force, as defined per dummy (ES-2/ES-2re, SID-IIs, WorldSID depending on the protocol). FMVSS 214 limits: HIC36 <= 1000 both dummies; ES-2re rib deflection <= 44 mm, abdominal force sum <= 2,500 N, pubic symphysis <= 6,000 N; SID-IIs lower spine <= 82 g, pelvic force sum <= 5,525 N.
- Design implications: strong B-pillar and sills, door beams and cross-members, floor cross-members and seat cross-beam to share the load; side and curtain airbags with deployment within roughly ten ms of contact for pole impacts (design heuristic, gated: unconfirmed); door trim padding for chest and pelvis.
- EV: sills and battery enclosure must resist pole intrusion; avoid battery deformation.
- Procedure: CAE predicts intrusion and velocity, validated with sub-system and full-vehicle tests.

**Gotchas:** pole location varies by vehicle; test the worst-case alignment.

## Verify
- [ ] Intrusion velocity and displacement at the barrier/pole location within targets.
- [ ] Airbag timing sensing at the earliest-sensing configuration verified.
