---
id: energy-mining-utilities.oil-gas-extraction.production-operations.pumper-rounds-and-tank-battery-operation
name: pumper-rounds-and-tank-battery-operation
category: energy-mining-utilities
field: oil-gas-extraction
product: production-operations
tags: [production-operations, pumper, lease-operator, lease-rounds, oilfield, tank-battery, separator, two-phase-separator, three-phase-separator, heater-treater, emulsion, free-water-knockout, fwko, tank-gauging, strapping, thief, bs-and-w, basic-sediment-and-water, run-ticket, lact-unit, gas-meter, chart-recorder, scada, wellhead, casing-pressure, tubing-pressure, h2s, vapour-recovery, spill-prevention]
level: practitioner
status: draft
description: "Run daily pumper rounds on an onshore lease: well checks, separator and heater-treater operation, tank gauging and thieving, run tickets, and spotting problems before they cost production."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Pumper rounds and tank battery operation

**Goal:** check every well and the battery each day, keep fluids separating and flowing
to sales, and catch problems (down wells, leaks, bad oil) the same day.

> Status: draft. Onshore North American terminology is used (pumper, lease, run
> ticket). Sales specs, gauging standards (e.g. API MPMS), and regulatory reporting
> vary by purchaser and jurisdiction.

## 1. At each well
- Is it running? Pump jack stroking smoothly, no knocking or banging (fluid pound or
  mechanical issue); ESP/gas-lift wells: check the controller, injection rate and
  pressures.
- Read and record **tubing pressure** and **casing pressure**; compare with yesterday.
  A rising casing pressure on a rod-pumped well can mean gas interference or a pump-off
  controller issue; falling tubing pressure may mean a tubing leak or low production.
- Look for **leaks** at the stuffing box, flowlines and wellhead; check the polished
  rod and stuffing box packing.
- Note anything for the production foreman or SCADA ticket.

## 2. Separation at the battery
- **Separator:** splits gas from liquids (two-phase) or gas, oil and water
  (three-phase). Check pressure, liquid level controllers and dump valves are cycling.
  A stuck dump valve floods gas lines with liquid or blows gas into the tanks.
- **Free-water knockout** removes bulk water early.
- **Heater-treater:** heats the emulsion so water drops out. Check burner and pilot
  operation, temperature setpoint, oil and water levels, and the interface. Too cold and
  oil goes to tanks wet; too hot and you lose light ends and waste fuel.
- Chemical injection pumps (demulsifier, corrosion inhibitor, paraffin control): check
  tank levels and that pumps are actually stroking.

## 3. Tank gauging
- **Gauge** each tank with a tape and bob from the gauge hatch (top gauge or innage);
  read to the nearest 1/4 in or as your purchaser requires; convert with the tank's
  **strapping table** to barrels.
- **Thief** samples (top, middle, bottom or all-levels) to check **BS&W** (basic sediment
  and water) with a centrifuge "shake-out" and temperature/API gravity with a
  thermometer and hydrometer.
- Bottom water: water-finding paste on the bob shows the oil/water interface.
- **H₂S and vapour hazard:** gauge hatches can release toxic, oxygen-poor vapour.
  Stand upwind, wear a monitor, follow the site's rule on hatch opening (many operators
  now restrict manual gauging; there have been fatalities from hydrocarbon vapour
  exposure at hatches).

## 4. Sales
- When a truck runs a tank (or a LACT unit runs oil automatically), record opening and
  closing gauges, temperatures, BS&W and seal numbers on the **run ticket**. Check the
  trucker's numbers before signing.
- Never sell oil above the purchaser's BS&W limit; treat it again first.

## 5. Daily records
Production per well (from tests or allocation), tank levels, water hauled, gas sales,
downtime with reasons. Trends reveal a well declining unexpectedly.

## Gotchas
- Thunderstorms: tank battery lightning strikes cause fires — don't gauge in storms.
- Wet oil can look fine at the hatch; trust the shake-out, not the colour.
- Unreported spills grow into regulatory problems; report per the plan.

## Verify
- [ ] Every well checked, pressures recorded and compared.
- [ ] Separators and treaters cycling; temperatures and levels normal.
- [ ] Tanks gauged and converted correctly; BS&W and gravity measured.
- [ ] Run tickets checked and signed with seals recorded.
- [ ] H₂S/vapour precautions followed at hatches.
