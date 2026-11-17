---
id: engineering-technology.automotive-vehicle-engineering.ev-battery-systems.battery-heat-generation-estimate
name: battery-heat-generation-estimate
category: engineering-technology
field: automotive-vehicle-engineering
product: ev-battery-systems
tags: [battery-heat-generation, heat-generation, joule-heating, entropic-heat, thermal-model, heat-capacity, battery-thermal]
level: practitioner
status: gated
description: "Estimate cell and pack heat generation from I^2R and entropic terms, compute temperature rise, and size thermal management for the duty cycle."
sources:
  - "Bernardi, Pawlikowski and Newman heat generation model (J. Electrochem. Soc. 1985)"
  - "Warner, Lithium-Ion Battery Chemistries and Pack Design"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# Heat generation estimate

1. Heat rate per cell: `Q = I^2*R + I*T*(dU/dT)` where R is the total DC resistance (including polarisation) and the second term is reversible/entropic heat (sign depends on SOC and current direction; often small compared with I^2 R at high rate).
2. Pack: `Q_pack = I_pack^2*R_pack`. Example: 250 A through 0.1 ohm pack resistance generates 6.25 kW (computed).
3. Temperature rise for adiabatic: `dT/dt = Q/(m*cp)` with cell cp about 0.9-1.1 kJ/(kg K) (gated: unconfirmed, source is paywalled or blocked) (take supplier data). Use time-step simulation over the drive/charge profile instead of a steady value.
4. Resistance depends strongly on temperature and SOC; use cold values for winter and aged values for end of life.
5. Add heat from busbars, contactors and fuses.
6. Compare with the cooling capability (see liquid cooling plate design) and decide cooling mode (air, liquid, immersion) for the worst duty (fast charge, climb, track).

**Gotchas:** using fresh DCIR only; cell-to-cell heat spread.

## Verify
- [ ] Cell surface temperature predicted vs measured on a test profile within a few K.
- [ ] Worst-case duty cycle defined and used for sizing.
