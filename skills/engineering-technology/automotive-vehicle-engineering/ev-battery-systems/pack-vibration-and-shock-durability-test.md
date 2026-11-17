---
id: engineering-technology.automotive-vehicle-engineering.ev-battery-systems.pack-vibration-and-shock-durability-test
name: pack-vibration-and-shock-durability-test
category: engineering-technology
field: automotive-vehicle-engineering
product: ev-battery-systems
tags: [pack-vibration-test, vibration-test, shock-test, random-vibration, psd, mechanical-integrity, pack-mechanical, un-38-3, un-r100, durability, resonance-search]
level: practitioner
status: gated
description: "Plan pack vibration and mechanical shock durability testing: derive profiles from road data, run resonance search and random tests, and define post-test pass checks."
sources:
  - "UN Regulation 100 (REESS safety; confirm current revision at https://unece.org)"
  - "UN Manual of Tests and Criteria, section 38.3 (transport tests for lithium cells and batteries; confirm current edition)"
  - "Warner, Lithium-Ion Battery Chemistries and Pack Design (chapter list)"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# Pack vibration and shock durability test

## 1. Which test is which
- **UN 38.3 (includes vibration and shock tests):** transport safety tests for lithium cells and batteries; a pass is required to ship. It is not a vehicle durability test.
- **UN R100 (REESS) and local regulations:** require vibration and mechanical shock tests on the REESS with defined profiles for road-vehicle approval (gated: unconfirmed, source is paywalled or blocked); confirm the current revision.
- **OEM durability tests:** longer and representative of life; typically more severe and based on measured road data.

## 2. Build the load profile
Measure acceleration at the pack mounts on durability roads (rough roads, pave, potholes, curb strikes) with accelerometers on the body-side mounting points. Convert time histories to power spectral density for random tests, or replay waveforms on a shaker. Extrapolate to life using Miner damage and an accelerated level with a fatigue exponent appropriate to the failing material (justify and document it).

## 3. Test sequence
1. Resonance search (low-level sine sweep) per axis to find pack modes; compare with CAE and body-mode targets.
2. Random vibration per axis at the required duration and temperature.
3. Mechanical shock in the specified directions.
4. Optional combined thermal and vibration (climatic chamber on shaker).
Mount the pack with real fasteners and brackets; keep fixture resonances above the test band; control accelerometers at mount points.

## 4. Pass criteria
During and after: no leakage or electrolyte spillage, no fire or explosion, isolation resistance within limit, no loss of function, capacity and impedance change within the agreed limit, no loose fasteners, cracked welds or visible damage on teardown. Check cell tabs, busbar fatigue, connector fretting, sensor harness integrity and coolant leaks.

## 5. Common problems
- Cell tab or busbar fatigue at a pack resonance that matches a road input.
- Harness fretting at clips.
- Fastener torque loss: use a locking strategy and re-torque checks.

## Verify
- [ ] Profile derived from measurements with documented damage equivalence.
- [ ] Resonances correlated with CAE.
- [ ] Post-test electrical, thermal and leak checks plus teardown.
- [ ] Regulatory test edition confirmed for the market.
