---
id: engineering-technology.automotive-vehicle-engineering.ev-battery-systems.traction-pack-sizing-and-architecture
name: traction-pack-sizing-and-architecture
category: engineering-technology
field: automotive-vehicle-engineering
product: ev-battery-systems
tags: [ev, bev, phev, traction-battery, battery-pack, pack-sizing, cell-selection, series-parallel, 400v, 800v, c-rate, nmc, lfp, lithium-ion, cell-to-pack, module, thermal-management, cooling-plate, bms, battery-management-system, soc-window, degradation, thermal-propagation, thermal-runaway, iso-26262, iso-6469, unece-r100, gb-38031, un-38-3, dc-fast-charging]
level: practitioner
status: gated
description: "Size a traction battery: energy from Wh/km and usable SOC window, series/parallel cell count from voltage and power, C-rate, thermal load and BMS limits."
sources:
  - "UN ECE Regulation No. 100 (electric power train safety)"
  - "ISO 6469-1 (RESS safety) and ISO 26262 (functional safety)"
  - "GB 38031 (China traction battery safety requirements)"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# Traction pack sizing and architecture

**Goal:** go from a range and performance target to a cell choice, an s×p configuration,
a gross energy, and first-cut thermal and BMS requirements that hold at end of life.

## 1. Energy
```
E_usable = range × consumption_at_battery      E_gross = E_usable / usable_SOC_fraction
```
Example: 450 km WLTP at 160 Wh/km (battery terminals) → 72 kWh usable. With a 93%
usable window → **~77 kWh gross**.
Decide what range is promised at end of life. If EOL is defined at 70–80% capacity and
range must hold, you either oversize or accept the fade — make it an explicit decision,
not an accident. Also budget real-world consumption (winter, motorway) separately from
the homologation number.

## 2. Voltage class → series count
Pick the bus voltage first (400 V or 800 V class), then:
- NMC (≈3.6–3.7 V nominal, 4.2 V max, ~2.8–3.0 V min): 96s → ~403 V max, ~290 V
  min for 400 V class; ~192s for 800 V class.
- LFP (3.2 V nominal, 3.65 V max, ~2.5 V min): ~108–120s for 400 V class.
Check the **minimum** voltage at low SOC, cold and under load: inverter current and the
motor's base speed are set there. 800 V halves current for the same power (thinner
cables, faster charging) but costs in semiconductor and component availability.

## 3. Parallel count
`Ah_pack = E_gross / (N_s · V_nom)`. Example: 77 000 / (96 · 3.65) = 220 Ah. With 60 Ah
prismatic cells → 4p (240 Ah, ~84 kWh) or choose a ~75 Ah cell at 3p. Round to what the
supplier sells; cell format (cylindrical, prismatic, pouch) drives the mechanical concept.

## 4. Power and C-rate
Peak discharge current = P_peak / V_min,loaded. Example: 200 kW / 330 V ≈ 606 A, per
cell in 4p ≈ 152 A ≈ 2.5C on a 60 Ah cell. Confirm the cell's 10 s and 30 s pulse power
tables at low SOC and 0 °C, not only at 50% SOC / 25 °C. DC fast charge 10–80% in 20
min is ~2.1C average — check the cell's charge map and lithium-plating limits by
temperature.

## 5. Heat load
Ohmic heat ≈ I² · R_pack, with R_pack = N_s · R_cell / N_p.
Example: R_cell = 1.0 mΩ → R_pack = 24 mΩ; 606 A peak → ~8.8 kW briefly; ~480 A
fast-charge → ~5.5 kW sustained for tens of minutes — **fast charging usually sizes the
cooling system**, not driving. Targets commonly used: cells in ~15–35 °C for operation,
cell-to-cell spread within ~5 °C (gated: unconfirmed, source is paywalled or blocked). (All worked numbers in sections 1, 3, 4, 5 recomputed: 72 kWh, 77.4 kWh, 403/288 V, 220 Ah, 606 A, 2.1C, 24 mOhm, 8.8 kW, 5.5 kW.) Cold climates need heating (heat pump, PTC or motor
waste heat) to allow fast charging.

## 6. Architecture choices
- Module-based vs cell-to-pack (fewer parts, higher volumetric density, harder repair).
- Cooling plate under cells (common), side cooling (cylindrical), or immersion (niche).
- High-voltage junction: main contactors on both poles, pre-charge circuit, pyro-fuse,
  service disconnect, current sensor (shunt and/or Hall).

## 7. BMS requirements to write down early
- Cell voltage measurement accuracy (single-digit mV; LFP's flat OCV curve needs the
  tightest), temperature sensing density, current sensing range and offset.
- SOC/SOH estimation approach, balancing (passive is typical), contactor control and
  welding detection, isolation monitoring (UN R100 is commonly quoted as ≥100 Ω/V DC and ≥500 Ω/V AC (gated: unconfirmed, source is paywalled or blocked); FMVSS 305 S5.3 states 500 Ω/V and 100 Ω/V options, fetched; check the current revision).
- Functional safety: overcharge, over-discharge, over-temperature and over-current
  hazards are usually allocated high ASILs under ISO 26262 (often ASIL C (gated: unconfirmed, source is paywalled or blocked), depending on the
  HARA); the cell supervision chain must meet that.

## 8. Safety and abuse
Design for thermal propagation (barriers, venting paths, gas management) as well as
single-cell runaway prevention. Requirements are moving: China's GB 38031 revision
tightens propagation requirements toward "no fire, no explosion" — verify the edition and
effective date applicable to your market. Also UN 38.3 for transport, UN R100 / ISO 6469-1,
and crash/intrusion protection in the vehicle structure.

## Gotchas
- Quoting gross kWh as range energy overstates range by the unusable window.
- Non-cell mass (housing, cooling, electrics, crash structure) is a large share of pack
  mass — very roughly a quarter to two-fifths for module designs, less for cell-to-pack (gated: unconfirmed, source is paywalled or blocked);
  use your own benchmark data, these figures vary widely.
- Cold power fade can halve available discharge power (gated: unconfirmed, source is paywalled or blocked); validate at −20 °C.

## Verify
- [ ] Usable and gross energy stated separately; EOL range policy written down.
- [ ] Series count checked at max and min voltage against inverter and charger limits.
- [ ] Peak current and C-rate checked at low SOC and low temperature.
- [ ] Cooling sized for the fast-charge case.
- [ ] BMS accuracy, isolation monitoring and ASIL targets captured as requirements.
- [ ] Applicable safety regulations and editions confirmed for each target market.
