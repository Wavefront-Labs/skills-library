---
id: engineering-technology.chemical-engineering.aspen.column-sizing-and-rating-in-simulator
name: column-sizing-and-rating-in-simulator
category: engineering-technology
field: chemical-engineering
product: aspen
tags: [chemical-engineering, aspen, aspen-column-simulation, column-sizing-and-rating-in-simulator, tray-sizing, tray-rating, pack-rating, column-internals, radfrac, aspen-plus, flooding, pressure-drop]
level: practitioner
status: gated
description: "Size and rate trays and packing inside RadFrac (Tray Sizing, Tray Rating, Pack Sizing, Pack Rating) and use the results to correct pressure drop and efficiency."
sources:
  - "Aspen Plus and Aspen HYSYS user guides and help (AspenTech), Seider et al. Product and Process Design Principles"
  - "https://www.aiche.org"
  - "AspenTech Aspen Plus certification study guide AT-05198 (learning objectives, aspentech.com)"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Tray and packing sizing and rating in the simulator

**Goal:** use the hydraulics built into the simulator to confirm diameter, flooding margin and pressure drop, then feed the actual pressure drop back into the model.

## Steps
1. Converge the column at theoretical stages first.
2. Open **Column Internals** on the RadFrac block (AspenTech's study guide confirms interactive Sizing and Rating of trays and packing, but not this menu name (gated: unconfirmed, source is paywalled or blocked)); add a section (stage range) and choose Tray or Packed, then **Sizing** (the program finds diameter) or **Rating** (you enter diameter, tray spacing, hole size or packing type and height).
3. Enter tray type (sieve, valve, bubble cap) or packing (type, size, vendor) as needed.
4. Run and read the report: diameter, percent flood, downcomer backup, weeping and entrainment indicators, and pressure drop per section.
5. Adjust: design for typical flooding targets (about 70 to 85% of flood for new designs; confirm the company standard) (gated: unconfirmed, source is paywalled or blocked) and keep downcomer backup under about 50% of tray spacing plus weir height as a first check (gated: unconfirmed, source is paywalled or blocked).
6. **Back-feed** the pressure drop: put the computed section pressure drop into the Pressure form and rerun. Check how the reboiler temperature and reflux change.
7. Apply realistic efficiencies; the simulator's hydraulics do not set efficiency.

## Packed columns
Check pressure drop per metre (typically 20 to 50 mm water per metre for conventional design (gated: unconfirmed, source is paywalled or blocked)), liquid load and the minimum wetting rate; limit packed height per bed with redistribution.

## Gotchas
- Designing diameter at the top-tray loading only; check the highest-loaded stage in each section, often the bottom or near the feed.
- A single diameter for the whole column may be wasteful when loads vary greatly; use sections.
- The built-in methods are vendor- or correlation-specific; confirm for final designs with vendor software.

## Verify
- [ ] Flood, downcomer and weep checks pass in every section.
- [ ] Pressure drop fed back and the column reconverged.
