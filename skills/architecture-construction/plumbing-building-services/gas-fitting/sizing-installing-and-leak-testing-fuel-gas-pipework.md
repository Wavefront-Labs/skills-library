---
id: architecture-construction.plumbing-building-services.gas-fitting.sizing-installing-and-leak-testing-fuel-gas-pipework
name: sizing-installing-and-leak-testing-fuel-gas-pipework
category: architecture-construction
field: plumbing-building-services
product: gas-fitting
tags: [plumbing-building-services, gas-fitting, gas-fitter, natural-gas, lpg, propane, gas-pipe-sizing, pressure-drop, btu, mj-per-hour, csst, black-iron, copper-gas, appliance-connection, isolation-valve, regulator, tightness-test, leak-test, manometer, purging, flueing, combustion-air, gas-safe, nfpa-54, as-nzs-5601]
level: advanced
status: draft
description: "Size fuel gas pipework by load and length, install and support it, connect appliances, and tightness/leak test before commissioning — licensed work in most places."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Sizing, installing and leak-testing fuel gas pipework

**Goal:** enough gas at every appliance at full simultaneous load, no leaks, safe
flueing and combustion air. **In nearly every jurisdiction this is licensed work**
(e.g., Gas Safe in the UK, licensed gasfitter in AU/NZ, permit + inspection in the US).
This skill describes the method; it does not replace the licence or local code
(NFPA 54/IFGC, AS/NZS 5601, BS 6891 / IGEM).

## 1. Load
- List every appliance and its input rating (MJ/h or Btu/h, kW) from the data plate.
- Total connected load is normally used for sizing (allow for future appliances if the
  client plans them).
- Note supply pressure: low-pressure natural gas (~1.0–2.75 kPa / 4–11 in w.c.) vs LPG
  (~2.75 kPa / 11 in w.c.) vs elevated pressure systems.

## 2. Sizing by the longest-length method (typical)
1. Measure the length from the meter/regulator to the **most remote** appliance (add
   equivalent length for fittings, or use code allowances).
2. Using the code table for that gas, pressure and allowed pressure drop, find the pipe
   size that carries the total load at that length for the first section.
3. Work outward: each section sized for the load downstream of it, but always read at the
   **same longest length** column.
- CSST and copper have their own tables; manufacturers' sizing is required for CSST.
- Under-sizing shows as poor flame, yellow tipping, or appliance lockouts at full load.

## 3. Installation
- Approved materials only (black steel, copper where permitted, CSST, PE underground).
- Support at code spacings; protect from damage; sleeve through walls and slabs.
- **Isolation valve** at each appliance, accessible, and a dirt leg/sediment trap where
  required.
- CSST: bonding to the electrical earth per manufacturer/code (lightning risk).
- No concealed unions/mechanical joints where prohibited.
- LPG: cylinders outside, clear of drains, openings and ignition sources per code
  distances; LPG is heavier than air and pools.

## 4. Tightness (leak) test
1. Isolate appliances (or test with them connected per code method).
2. Pressurise with air/inert gas (new pipework) to the code test pressure — commonly a
   multiple of working pressure, held for a set time with a calibrated manometer.
3. Allow temperature stabilisation, then hold: **any** drop beyond the allowed value
   fails. Find leaks with leak-detection solution (never a flame).
4. Record test pressure, duration and result.

## 5. Purging and commissioning
- Purge air to a safe place outside (never into an enclosed space), until gas is present.
- Light each appliance, check **burner pressure** at the test point against the data
  plate, flame picture, and operation of safety devices (flame failure).
- Check **flue**: draught/spillage test on open-flued appliances, terminals at code
  clearances, combustion air openings sized and unobstructed.
- Carbon monoxide alarm where required.

## Gotchas
- Sizing each section by its own length instead of the longest length → undersized
  remote branches.
- Leaving an open (uncapped) end after removing an appliance.
- Flue spillage in tight modern houses when extract fans run.
- Mixing LPG and natural gas jets/regulators — appliances must be converted correctly.

## Verify
- [ ] Load schedule and sizing worksheet on file.
- [ ] Tightness test passed and recorded (pressure, time, gauge).
- [ ] Each appliance: burner pressure to spec, safety device tested, flue spillage test OK.
- [ ] All open ends capped; isolation valves accessible.
- [ ] Compliance certificate/inspection completed.

*Status: draft — methods summarised from common code structure; numbers deliberately
indicative. Never act on these without the local code and a licence.*
