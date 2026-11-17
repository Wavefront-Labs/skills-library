---
id: energy-mining-utilities.energy-storage-operations.pumped-hydro-operation.pump-generate-mode-changes-in-pumped-storage
name: pump-generate-mode-changes-in-pumped-storage
category: energy-mining-utilities
field: energy-storage-operations
product: pumped-hydro-operation
tags: [pumped-hydro-operation, pumped-storage, pumped-hydro, phes, reversible-pump-turbine, motor-generator, generating-mode, pumping-mode, synchronous-condenser, mode-changeover, synchronisation, synchroniser, back-to-back-start, sfc, static-frequency-converter, dewatering, tailwater-depression, compressed-air-depression, governor, wicket-gates, penstock, surge-tank, waterway, upper-reservoir, lower-reservoir, reservoir-levels, water-hammer, hydro-operator]
level: practitioner
status: draft
description: "Operate a pumped-storage unit: starting and synchronising in generate mode, pump-mode start methods, mode changeover sequences, reservoir level limits and waterway inspections."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Pump-generate mode changes in pumped storage

**Goal:** move a reversible pumped-storage unit between generating, pumping and other
modes safely and on time for the dispatch schedule, while keeping reservoirs and
waterways within limits.

> Status: draft. Sequences are automated and plant-specific; this describes what the
> operator monitors and why. Exact interlocks and timings come from the station's
> operating instructions.

## 1. Modes
- **Generate (turbine) mode:** water flows from the upper reservoir through the
  penstock and turbine to the lower reservoir; the machine produces power.
- **Pump mode:** the machine runs in reverse as a motor-driven pump, lifting water up.
- **Synchronous condenser (spinning) modes:** the machine spins connected to the grid
  with the runner **dewatered** (water pushed out with compressed air) to provide
  reactive power or fast readiness.
- Variable-speed units (doubly-fed or full-converter) can adjust pump power; fixed-speed
  units pump at essentially fixed power.

## 2. Starting in generate mode
1. Pre-start checks: cooling water, bearing oil, governor oil pressure, excitation
   ready, no permits on the unit, intake gate/valve open, waterway pressurised.
2. Open the main inlet valve (after balancing pressure across it), open the wicket gates
   to accelerate the unit to synchronous speed.
3. Apply excitation; the **synchroniser** matches voltage, frequency and phase angle
   before closing the generator breaker. A bad synchronisation is a severe mechanical
   and electrical shock — never override a synchroniser check without a procedure.
4. Load to the dispatch setpoint at the allowed ramp rate.

## 3. Starting in pump mode
- A pump-turbine can't start pumping from standstill against water easily, so:
  - **Dewater the runner** with compressed air (tailwater depression),
  - accelerate the dry machine to synchronous speed using a **static frequency
    converter (SFC)** or **back-to-back start** from another unit,
  - synchronise, then **re-water** (vent the air), open the wicket gates and prime the
    pump. Watch for the pressure build and the transition to stable pumping.
- Watch for failures to prime, air not venting, or excessive vibration in the
  transition — trip conditions are set for these.

## 4. Mode changeovers
- Generate → pump typically goes via shutdown (or condenser mode) because the rotation
  direction reverses. Total changeover times range from minutes to tens of minutes
  depending on design — know your plant's figures, as dispatch relies on them.
- Rapid cycling stresses machines; respect minimum run and minimum stop times.

## 5. Reservoirs and waterways
- Keep upper and lower reservoir levels within operating limits: don't pump the upper
  reservoir over its full supply level, don't draw down below minimum (vortex/air
  entrainment at intakes, slope stability on embankments).
- Rapid drawdown rates can destabilise reservoir banks — limits are set by the
  dam engineer.
- Waterway: watch surge tank levels and penstock pressures during load changes and
  trips; **water hammer** from fast gate closures is limited by governor closing laws.
- Periodic dewatered inspections of tunnels, penstocks and gates check for erosion,
  cavitation damage and lining cracks.

## Gotchas
- Debris on intake trash racks raises head loss and vibration — check differential.
- Seasonal inflows and evaporation change the energy actually stored.
- Communications loss with the dispatcher: follow the default schedule rules.

## Verify
- [ ] Unit pre-start checks complete; no conflicting permits.
- [ ] Synchronisation achieved by the synchroniser without override.
- [ ] Pump start priming and re-watering normal.
- [ ] Reservoir levels and drawdown rates inside limits.
- [ ] Changeover times logged against the plant's declared values.
