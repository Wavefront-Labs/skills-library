---
id: engineering-technology.automotive-vehicle-engineering.powertrain-design.reading-a-bsfc-map
name: reading-a-bsfc-map
category: engineering-technology
field: automotive-vehicle-engineering
product: powertrain-design
tags: [bsfc-map, bsfc, fuel-consumption-map, efficiency-island, brake-thermal-efficiency, engine-map]
level: practitioner
status: gated
description: "Read a BSFC map: islands of minimum fuel use, conversion to thermal efficiency, constant-power hyperbolae and how to pick operating points for economy."
sources:
  - "Heywood, Internal Combustion Engine Fundamentals"
  - "Guzzella and Sciarretta, Vehicle Propulsion Systems"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# Reading a BSFC map

1. Axes: engine speed vs torque (or BMEP); contours of brake-specific fuel consumption in g/kWh.
2. Efficiency: `eta = 3600/(bsfc[g/kWh]/1000*LHV[kJ/kg])`. With gasoline LHV about 43 MJ/kg (gated: unconfirmed, source is paywalled or blocked) (arithmetic below computed), 240 g/kWh gives 3600/(0.24*43000) = 34.9%; 220 g/kWh gives about 38%.
3. Best island sits at mid speed and high load (low pumping loss). Light load is poor because of throttling and friction share.
4. Constant-power lines are hyperbolae `T = P/omega`. At a required power the lowest BSFC point along that line gives the optimal operating speed: lower speed and higher load is typically better (downspeeding).
5. For a CVT or hybrid, trace the "optimal operating line" through the island minima for each power level.
6. Maps are warm steady-state; transient, cold start, and enrichment at high load change real consumption.

**Gotchas:** diesel maps differ (best bsfc roughly 200 g/kWh (gated: unconfirmed, source is paywalled or blocked); at diesel LHV 42.8 MJ/kg that is 42%); different LHV values.

## Verify
- [ ] Efficiency conversion cross-checked by hand at two points.
- [ ] Operating line plotted on the map for several power levels.
