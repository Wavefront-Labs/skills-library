---
id: engineering-technology.chemical-engineering.separation-processes.packed-column-hetp-and-pressure-drop
name: packed-column-hetp-and-pressure-drop
category: engineering-technology
field: chemical-engineering
product: separation-processes
tags: [chemical-engineering, separation-processes, sep-column-hydraulics, packed-column-hetp-and-pressure-drop, packed-column, hetp, random-packing, structured-packing, pressure-drop, flooding, liquid-distributor, bed-height, generalised-pressure-drop-correlation]
level: practitioner
status: draft
description: "Size packed columns from packing choice, flooding and pressure-drop targets, estimate HETP for random and structured packing, and set bed heights with redistributors."
sources:
  - "Seader Henley and Roper Separation Process Principles, Perry Chemical Engineers Handbook separations sections, Kister Distillation Design, Treybal Mass-Transfer Operations, McCabe Smith and Harriott Unit Operations"
  - "https://www.aiche.org"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Packed column HETP and pressure drop

**Goal:** diameter and packed height for a separation.

## Steps
1. **Packing choice**: random (rings, saddles; cheaper, tolerant of fouling) vs structured (lower pressure drop, higher efficiency; vacuum and high-purity service).
2. **Diameter**: from a generalised pressure-drop correlation (GPDC chart, or the packing vendor's program): choose a design pressure drop (typical 20 to 50 mm water per metre of packing for general service, lower for vacuum; confirm with vendor), read vapour capacity, compute the column area.
3. **Height** = N_theoretical x HETP. Rules of thumb (indicative only): structured packing HETP about 0.3 to 0.6 m; random packing about 0.5 to 1.0 m or more; for 25 to 50 mm random packings HETP is often near 0.5 to 1 m; vendor data refine this.
4. **Bed sections**: limit each bed (for random packing about 6 to 10 m, or a maximum height to diameter ratio around 10 for rings; structured packing usually less than 10 m) and use redistributors between beds.
5. **Distributors**: select by liquid rate and fouling; check minimum wetting rate and number of drip points per area.
6. **Hold-down plates, supports** and liquid collectors.

## Checks
Percent flood, minimum liquid load for wetting, turndown range, maldistribution risk (small diameters under about 0.3 m wall effects).

## Gotchas
- Published HETP values come from total-reflux tests; add margin for real operation (10 to 20%).
- Structured packing is sensitive to liquid distribution and feed introduction.
- Packing in fouling or polymerising service needs special consideration.

## Verify
- [ ] Flooding fraction and pressure drop printed per bed.
- [ ] HETP source cited; sensitivity of height to plus 25% HETP reviewed.
