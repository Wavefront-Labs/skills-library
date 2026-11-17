---
id: engineering-technology.automotive-vehicle-engineering.ev-battery-systems.cylindrical-prismatic-pouch-cell-formats
name: cylindrical-prismatic-pouch-cell-formats
category: engineering-technology
field: automotive-vehicle-engineering
product: ev-battery-systems
tags: [cell-formats, cylindrical-cell, prismatic-cell, pouch-cell, 21700, 18650, cell-format]
level: practitioner
status: draft
description: "Compare cylindrical, prismatic and pouch cell formats on energy density, thermal behaviour, mechanical constraints, manufacturing and pack integration."
sources:
  - "Warner, Lithium-Ion Battery Chemistries and Pack Design"
  - "Linden and Reddy, Handbook of Batteries"
licence: Apache-2.0
version: 2
updated: 2026-11-17
aliases: []
---

# Cylindrical, prismatic and pouch formats

- **Cylindrical (18650, 21700 and larger formats):** mature, robust steel can, built-in vent, good manufacturing yield; many cells per pack means many connections and more cooling and busbar complexity; gaps between cells reduce volumetric packing.
- **Prismatic (aluminium or steel can):** good volumetric packing, fewer cells, large format simplifies electrical connection; heat removal from the large face; needs compression management and robust vent design.
- **Pouch (laminated foil):** lightest packaging, flexible form factor, high gravimetric energy density; needs mechanical support, swelling allowances, edge sealing protection and careful compression.
- Pack-level comparison: use pack energy density (not cell) and cost per kWh, includes structure, cooling, busbars and safety.
- Selection factors: supply security, qualification cost, thermal path (cooling surface per kWh), safety features (CID, vent), fast charge capability, swelling behaviour, thermal runaway propagation behaviour.
- Check that format availability and dimensions are as of your supplier datasheet; formats and sizes change.

**Gotchas:** cell-level energy density claims versus pack-level reality.

## Verify
- [ ] Pack-level energy density and cost computed per format using the same assumptions.
- [ ] Thermal and compression requirements listed per format.
