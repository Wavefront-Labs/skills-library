---
id: energy-mining-utilities.energy-storage-operations.thermal-mechanical-storage-operation.molten-salt-flywheel-and-caes-operation
name: molten-salt-flywheel-and-caes-operation
category: energy-mining-utilities
field: energy-storage-operations
product: thermal-mechanical-storage-operation
tags: [thermal-mechanical-storage-operation, thermal-energy-storage, tes, molten-salt, solar-salt, hot-tank, cold-tank, freeze-protection, heat-tracing, salt-freezing, csp, concentrated-solar-power, hot-water-store, thermocline, district-heating, flywheel, flywheel-energy-storage, vacuum, magnetic-bearing, caes, compressed-air-energy-storage, salt-cavern, recuperator, adiabatic-caes, liquid-air, charge-discharge-cycle, round-trip-efficiency]
level: practitioner
status: draft
description: "Operate non-battery storage: molten-salt hot/cold tank cycling and freeze protection, hot-water thermal stores, flywheel vacuum and bearing watch, and compressed-air storage cycling."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Molten-salt, flywheel and CAES operation

**Goal:** charge and discharge non-battery storage plant within its physical limits —
temperature for thermal stores, speed and vacuum for flywheels, pressure for
compressed air — and avoid each technology's signature failure.

> Status: draft. These technologies are less standardised than batteries, and fewer
> plants exist; the notes are general and must be checked against your plant's
> operating manual. Temperatures quoted are commonly published figures for
> "solar salt" (sodium/potassium nitrate) and may differ for your salt.

## 1. Molten-salt thermal storage
- Two-tank systems: a **cold tank** (often around 290 °C) and **hot tank** (often around
  565 °C for tower plants). Charging heats salt from cold to hot; discharging runs it
  through steam generators back to the cold tank.
- **Freezing is the signature failure.** Solar salt freezes at roughly 220–240 °C. Any
  line, valve or instrument tap that falls below that solidifies and can burst on
  re-melting or block the circuit.
  - Keep **heat tracing** healthy; check tracing circuits and temperature sensors daily.
  - **Drain lines** that will sit idle, according to the procedure, before they cool.
  - Treat a tracing alarm on a filled line as urgent.
- Watch tank level and temperature stratification, tank foundation temperatures (hot tank
  foundations are cooled), and thermal ramp rates on heat exchangers — thermal shock
  cracks tube sheets.
- Salt chemistry: check for nitrite/chloride build-up and corrosion products per the
  sampling plan.

## 2. Hot-water thermal stores
- Large insulated tanks or pits keep a **thermocline** — hot water on top, cold below.
  Charge and discharge slowly through diffusers so mixing doesn't destroy stratification;
  monitor the temperature profile along the height.
- Watch for oxygen ingress (corrosion), and pressurisation/nitrogen blanket where used.

## 3. Flywheels
- Energy is stored as rotational speed; stored energy rises with the square of speed.
  Units run in a **vacuum** enclosure on magnetic or low-loss bearings.
- Monitor: speed, vacuum level (rising pressure = leak or outgassing → drag and heat),
  bearing temperatures and vibration, and power electronics status.
- Flywheels are designed with containment for rotor failure; never defeat interlocks
  on containment or approach a unit reporting abnormal vibration at speed — spin it
  down first.
- They handle very high cycle counts but self-discharge relatively quickly (hours), so
  they suit short-duration services such as frequency response.

## 4. Compressed-air energy storage (CAES)
- Charging: compressors push air into an underground cavern (often salt) or vessels.
  Discharging: air expands through turbines (in diabatic CAES, heated by burning gas;
  in adiabatic designs, reheated from stored compression heat).
- Keep cavern pressure between minimum and maximum limits set by geomechanics;
  respect pressure change rates — fast cycling stresses cavern walls.
- Monitor compressor intercooler/aftercooler temperatures, moisture removal, and
  recuperator performance; wellhead and cavern integrity surveys are periodic.

## 5. Cycling and efficiency
Record energy in and out every cycle. **Round-trip efficiency** trending down points at
heat loss (insulation, tracing), leaks (vacuum, air) or degraded machines.

## Gotchas
- Thermal stores lose heat whether used or not; plan dispatch around standing losses.
- Power loss to tracing in winter is the classic molten-salt emergency — have the
  backup power plan.
- Flywheel spin-down takes time; plan maintenance windows accordingly.

## Verify
- [ ] Salt lines above freeze margin; tracing alarms clear.
- [ ] Thermocline / tank temperatures normal; ramp rates respected.
- [ ] Flywheel vacuum, bearing and vibration readings in range.
- [ ] Cavern pressure within limits and rate of change respected.
- [ ] Round-trip efficiency logged per cycle.
