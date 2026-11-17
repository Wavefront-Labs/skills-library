---
id: engineering-technology.automotive-vehicle-engineering.ev-battery-systems.second-life-and-recycling-planning
name: second-life-and-recycling-planning
category: engineering-technology
field: automotive-vehicle-engineering
product: ev-battery-systems
tags: [second-life, recycling, battery-recycling, repurposing, end-of-life, eu-battery-regulation, battery-passport, design-for-disassembly, hydrometallurgy, pyrometallurgy, direct-recycling]
level: practitioner
status: draft
description: "Plan end of first life for EV batteries: screen packs for reuse, design for disassembly, choose recycling routes, and track regulation (EU 2023/1542 and local rules)."
sources:
  - "Linden and Reddy, Handbook of Batteries (chapter list)"
  - "Warner, Lithium-Ion Battery Chemistries and Pack Design (chapter list)"
  - "Regulation (EU) 2023/1542 on batteries and waste batteries (confirm current applicability dates at https://eur-lex.europa.eu)"
licence: Apache-2.0
version: 2
updated: 2026-11-17
aliases: []
---

# Second life and recycling planning

Regulation and transport of used batteries vary by jurisdiction and change over time; confirm current law, applicable dates and dangerous-goods rules with qualified compliance staff before acting.

## 1. Decide the route per pack
1. **Remanufacture or repair** for the same vehicle (replace modules or cells).
2. **Second life** (stationary storage, low-demand mobility): needs adequate SoH, safe condition and economic value after testing.
3. **Recycling:** recovery of metals and materials.

## 2. Screening for reuse
Collect BMS history (SoH, peak temperatures, fault codes, charge events). Test capacity and resistance at pack and module level; inspect for damage, swelling and isolation faults; reject any pack with a thermal event. Grade by remaining capacity and impedance and match modules of similar state to avoid weak-cell limits.

## 3. Design for second life and disassembly (do this in the first design)
- Accessible fasteners rather than permanent adhesive where feasible; standardised data access and BMS unlock.
- Labelled chemistry and cell identification.
- Module-level swap capability.
- Pack data kept in a durable format; the EU Battery Regulation introduces a digital battery passport and information duties for certain batteries with phased dates (verify the current scope).

## 4. Recycling routes
- **Pyrometallurgy:** smelting recovers some metals (for example cobalt, nickel, copper); lithium recovery varies by process.
- **Hydrometallurgy:** leaching and precipitation recover several metals including lithium, typically after shredding to black mass.
- **Direct recycling:** research and early commercial; aims to recover cathode material with its structure intact.
Process choice depends on chemistry (LFP has lower-value metal content than NMC) and local facilities. EU law sets collection, recycled-content and recovery targets; verify the current values.

## 5. Handling and transport
Damaged or defective lithium batteries fall under special dangerous-goods provisions; use trained, certified handlers and approved packaging. Discharge and storage procedures belong to qualified personnel (HV hazard, fire).

## Verify
- [ ] Route decision documented per pack with SoH and safety criteria.
- [ ] Design supports module access and data retrieval.
- [ ] Legal requirements (passport, recycled content, take-back, transport) confirmed for the market.
