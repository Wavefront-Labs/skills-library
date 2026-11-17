---
id: engineering-technology.aerospace-engineering.aircraft-structures.mmpds-material-allowables
name: mmpds-material-allowables
category: engineering-technology
field: aerospace-engineering
product: aircraft-structures
tags: [aircraft-structures, aerospace-materials, materials-allowables, mmpds, a-basis, b-basis, grain-direction, mil-hdbk-5, design-allowables]
level: practitioner
status: draft
description: "Use MMPDS metallic allowables correctly: A-basis versus B-basis, temperature and thickness effects, grain direction, and when test data is needed instead."
sources:
  - "MMPDS Handbook (Metallic Materials Properties Development and Standardization)"
  - "FAA and EASA guidance on material allowables"
  - "Niu, Airframe Structural Design"
licence: Apache-2.0
version: 2
updated: 2026-11-17
aliases: []
---

# MMPDS metallic allowables

**Goal:** the right allowable for each failure mode and location.

## Facts
- MMPDS is the successor to MIL-HDBK-5; it publishes statistically derived mechanical properties of metallic materials for aerospace structure.
- **A-basis:** value above which at least 99% of the population is expected to fall with 95% confidence. **B-basis:** 90% population at 95% confidence. A-basis is typically used for single-load-path structure, B-basis for redundant structure; the choice comes from the certification criteria.

## Using the tables
1. Identify alloy, temper, product form (sheet, plate, extrusion, forging), thickness range, grain direction (L, LT, ST) and specification.
2. Take the property (Ftu, Fty, Fcy, Fsu, Fbru, Fbry, modulus, fatigue data) at the temperature of the design condition; apply temperature factors and exposure effects.
3. For fatigue, use S-N and crack-growth data in the handbook with the appropriate stress ratio.
4. When your material or process is not covered (new alloy, different thickness or processing), derive allowables by test per the statistical procedures (Chapter 9 of the handbook) in agreement with the authority.

## Gotchas
- Short-transverse (ST) properties and fracture toughness are much lower than L; thick forgings need them.
- Using typical values instead of design (A or B) values is a frequent error.
- Handbook values apply to material meeting the specification; process control must support them.

## Verify
- [ ] Every allowable in the stress report names basis, temper, thickness, direction, temperature and handbook edition.
