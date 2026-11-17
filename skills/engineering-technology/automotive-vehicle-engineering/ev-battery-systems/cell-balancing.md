---
id: engineering-technology.automotive-vehicle-engineering.ev-battery-systems.cell-balancing
name: cell-balancing
category: engineering-technology
field: automotive-vehicle-engineering
product: ev-battery-systems
tags: [cell-balancing, passive-balancing, active-balancing, bleed-resistor, voltage-balancing, soc-balancing, bms-requirements]
level: practitioner
status: gated
description: "Choose and tune passive or active cell balancing: algorithm timing, bleed current and thermal limits, balancing target and verification of cell spread."
sources:
  - "Plett, Battery Management Systems Vol. 1"
  - "Warner, Lithium-Ion Battery Chemistries and Pack Design"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# Cell balancing

1. Why: cells drift in SOC from capacity, resistance and self-discharge differences; the weakest cell limits pack charge and discharge.
2. **Passive:** a resistor across the cell dumps energy as heat; currents of tens to a few hundred mA (gated: unconfirmed, source is paywalled or blocked); simple and cheap; heat limits duty; slow (balancing 5% of 100 Ah takes 50 hours at 100 mA, computed).
3. **Active:** transfers charge by capacitors, inductors or transformers between cells; amps possible; efficiency 80-90% (gated: unconfirmed, source is paywalled or blocked); higher cost and complexity, useful for large imbalance or large format packs.
4. Algorithm: balance on **SOC** (from OCV after rest or model) rather than terminal voltage, because voltage under load or in the flat region misleads; typical strategies balance at end of charge or during rest.
5. Thresholds: start when spread exceeds a set value, stop at a smaller value (hysteresis); limit by temperature and by the thermal budget of the board.
6. Diagnostics: detect failed bleed paths, open balancing wire, abnormal self-discharge as a safety indicator.
7. Verify with a deliberately imbalanced pack and log spread over time.

**Gotchas:** balancing while charging with the measurement still showing IR drop; poor voltage accuracy.

## Verify
- [ ] Spread reduces to the target within the stated time on an imbalanced pack.
- [ ] Balancing resistor temperatures stay in limits.
