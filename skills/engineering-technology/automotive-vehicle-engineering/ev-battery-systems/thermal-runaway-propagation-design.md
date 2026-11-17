---
id: engineering-technology.automotive-vehicle-engineering.ev-battery-systems.thermal-runaway-propagation-design
name: thermal-runaway-propagation-design
category: engineering-technology
field: automotive-vehicle-engineering
product: ev-battery-systems
tags: [thermal-propagation, thermal-runaway, propagation-barrier, venting-path, cell-spacing, aerogel]
level: practitioner
status: gated
description: "Design to delay or stop thermal runaway propagation: trigger methods, barriers, cell spacing, vent paths, detection and what regulations require."
sources:
  - "UN GTR 20 (EVS) and GB 38031 overview; confirm current texts"
  - "Warner, Lithium-Ion Battery Chemistries and Pack Design"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# Thermal runaway propagation design

1. Understand the event: a cell in runaway releases heat and hot gas/particles; neighbours heat by conduction, radiation and hot gas; propagation depends on cell chemistry, energy, spacing and venting.
2. Regulations: UN GTR 20 and UN R100 revisions include requirements relating to thermal events and occupant warning (gated: unconfirmed, source is paywalled or blocked); China's GB 38031 requires no fire or explosion for a defined time after a thermal runaway warning (gated: unconfirmed, source is paywalled or blocked) (verify the current text and times for your market).
3. Test method: initiate a cell with a heater, nail, or overcharge; instrument cell and pack temperatures and gas pressure; record with video.
4. Design measures: insulating/intumescent barriers (mica, aerogel, ceramic fibre) between cells or modules; larger gaps or heat-absorbing structures; directed vent path away from occupants and from neighbours; metal cell-to-cell shields; cold plate heat sink; fire-resistant top cover.
5. Detection: gas sensors, pressure sensors, cell temperature and voltage, abnormal dV/dt; signal the vehicle and occupants.
6. Pack-level: venting path through pack with no combustible cross-over; HV connectors and busbars shielded.
7. Cost/mass trade: aerogel cost, density loss.

**Gotchas:** propagation tests are chemistry- and format-specific; do not extrapolate between cell types.

## Verify
- [ ] Propagation test shows delay or no propagation to the target time.
- [ ] Vent and warning timing measured and documented.
