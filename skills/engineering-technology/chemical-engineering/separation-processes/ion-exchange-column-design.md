---
id: engineering-technology.chemical-engineering.separation-processes.ion-exchange-column-design
name: ion-exchange-column-design
category: engineering-technology
field: chemical-engineering
product: separation-processes
tags: [chemical-engineering, separation-processes, sep-adsorption-and-ion-exchange, ion-exchange-column-design, ion-exchange, ion-exchange-column, resin-capacity]
level: practitioner
status: draft
description: "Size an ion exchange column: capacity, breakthrough volume, service flow rate, regeneration level and rinse."
sources:
  - "Seader Henley and Roper Separation Process Principles, Perry Chemical Engineers Handbook, Kister Distillation Design, Treybal Mass-Transfer Operations"
  - "https://www.aiche.org"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Ion exchange column design

**Goal:** Size an ion exchange column: capacity, breakthrough volume, service flow rate, regeneration level and rinse.

## Steps
1. Determine the ion load per cycle (concentration times volume) and the resin operating capacity (eq/L), which is lower than the total capacity; use the vendor data.
2. Resin volume = ion load per cycle / operating capacity.
3. Choose service flow in bed volumes per hour from the vendor range, and set the bed depth to meet the minimum depth and pressure drop limits.
4. Regenerate with acid, caustic or brine at the recommended level; plan the rinse and the waste neutralisation.
5. Select the resin type (strong or weak, cation or anion) from the target ions and the selectivity.

## Gotchas
- Selectivity and leakage depend on the water composition and the regeneration level.
- Organic fouling of the anion resin reduces capacity over time.

## Verify
- [ ] Equivalent balance closes for each cycle.
- [ ] Pressure drop and flow are within vendor limits.
