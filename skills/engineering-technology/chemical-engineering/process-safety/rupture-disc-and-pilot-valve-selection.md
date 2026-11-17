---
id: engineering-technology.chemical-engineering.process-safety.rupture-disc-and-pilot-valve-selection
name: rupture-disc-and-pilot-valve-selection
category: engineering-technology
field: chemical-engineering
product: process-safety
tags: [chemical-engineering, process-safety, ps-relief-sizing, rupture-disc-and-pilot-valve-selection, rupture-disc, pilot-operated-relief-valve, balanced-bellows, conventional-prv, burst-pressure, operating-ratio, relief-device-selection, combination-device]
level: advanced
status: gated
description: "Select between spring-loaded, balanced bellows, pilot-operated relief valves and rupture discs: back pressure, tightness, fouling, operating ratio and combination devices."
sources:
  - "CCPS Guidelines for Hazard Evaluation Procedures, CCPS Layer of Protection Analysis, API Standards 520 521 526 and 2000, IEC 61511, OSHA 29 CFR 1910.119, EU Seveso III Directive 2012/18/EU, Crowl and Louvar Chemical Process Safety, Lees Loss Prevention in the Process Industries"
  - "https://www.aiche.org"
  - "https://www.osha.gov"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Rupture disc and pilot valve selection

**Goal:** choose the relief device type that suits the service. Selection and installation are subject to the applicable code and the manufacturer's data; a qualified engineer must approve them.

## Device types
Percentage limits below are typical vendor and API 520 figures (gated: unconfirmed, source is paywalled or blocked); take the actual limits from the manufacturer's data and the current code.
- **Conventional spring-loaded**: simple and robust; set point affected by back pressure; recommended back pressure typically limited to about 10% of the set pressure.
- **Balanced bellows**: compensates for variable back pressure (typically up to about 30 to 50% of set pressure per vendor); bellows needs a vent to atmosphere (a hazard if the fluid is toxic or flammable) and has a fatigue limit.
- **Pilot-operated**: a pilot controls a main valve; allows operation at a higher ratio of operating to set pressure (up to about 90 to 95% against about 85 to 90% for spring valves), high back pressure tolerance, tight shut-off; sensitive to dirt, polymerisation, and requires clean service or a filtered pilot.
- **Rupture (bursting) disc**: a non-reclosing, leak-tight device that fails at a burst pressure; quick-opening, large areas, handles viscous, fouling or corrosive fluids; one-shot.
- **Combination** (rupture disc upstream of a relief valve): protects the valve from corrosion and gives leak tightness; the space between must be monitored (pressure gauge, tell-tale), and the capacity derating factor (K_c) applied.

## Selection factors
1. **Operating ratio** (operating pressure divided by set or burst pressure): for conventional discs about 70% (higher for composite or reverse-buckling discs per manufacturer); leave margin for pressure cycles and temperature.
2. **Service**: fouling, polymerising, corrosive, two-phase.
3. **Back pressure** and relief header design.
4. **Tightness needs** (toxic or expensive fluid) and **fugitive emission** limits.
5. **Reseating** requirement (a rupture disc cannot reseat, so inventory loss).
6. **Burst tolerance and manufacturing range**, temperature rating, vacuum support.

## Gotchas
- A rupture disc fragments can damage downstream equipment; use non-fragmenting designs where required.
- Disc and valve combination must have certified data for the capacity factor.
- A pilot valve's sense line must be located at a stable pressure point.

## Verify
- [ ] Selection table with the justification and the operating ratio computed.
- [ ] Manufacturer data sheet and certification attached.
