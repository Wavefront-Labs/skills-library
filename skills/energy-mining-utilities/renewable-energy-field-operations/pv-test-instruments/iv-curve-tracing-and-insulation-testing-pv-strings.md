---
id: energy-mining-utilities.renewable-energy-field-operations.pv-test-instruments.iv-curve-tracing-and-insulation-testing-pv-strings
name: iv-curve-tracing-and-insulation-testing-pv-strings
category: energy-mining-utilities
field: renewable-energy-field-operations
product: pv-test-instruments
tags: [renewable-energy-field-operations, pv-test-instruments, iv-curve-tracer, iv-curve, i-v-curve, voc, isc, pmax, fill-factor, stc, insulation-resistance, insulation-tester, megger, riso, irradiance-meter, reference-cell, pyranometer, thermal-camera, thermography, infrared, hot-spot, bypass-diode, pid, potential-induced-degradation, iec-62446, commissioning-test, solar-pv, pv-technician]
level: practitioner
status: draft
description: "Prove PV string faults with instruments: Voc/Isc and IV-curve tracing against STC models, insulation resistance testing, irradiance meters and thermal imaging under load."
sources:
  - "IEC 62446-1 (PV test, documentation and maintenance) and IEC 62446-3 (infrared thermography), concepts paraphrased"
  - "IV-curve tracer manufacturers' application notes, general principles paraphrased"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# IV-curve tracing and insulation testing of PV strings

**Goal:** turn a suspicion ("string 14 is low") into proof (which module, what failure),
using instruments correctly so the numbers mean something.

## 1. Conditions first
- Irradiance stable and high enough — commonly ≥ 700 W/m² in the module plane for
  meaningful IV curves (some standards accept ≥ 400 W/m² for basic tests); no passing cloud.
- Measure irradiance with a **reference cell or calibrated irradiance meter** in the same
  plane as the modules (tilt/tracker angle), and module **back-of-module temperature**.
- Thermography likewise needs ≥ ~600 W/m² and the string under load.

## 2. Voc and Isc (basic string test)
With the string isolated from the inverter (DC disconnect open, verified zero current):
- **Voc** with a CAT-rated multimeter or tester at the combiner — compare to expected:
  modules × Voc(STC), corrected for temperature (Voc falls ~0.25–0.35%/°C above 25 °C for
  crystalline silicon — use the datasheet coefficient).
- A string low by about one module's Voc → module missing/shorted bypass; low by ~ a third
  of a module → a failed (shorted) bypass diode.
- **Isc** via the tester's short-circuit function (never by bridging leads) — compare to
  Isc(STC) × (G/1000). Proportionally low Isc on one string = soiling, shading or
  degradation.

## 3. IV-curve tracing
1. Enter module model (or pick from database), modules per string, strings in parallel.
2. Connect tracer to the isolated string; connect irradiance and temperature sensors.
3. Trace; the tester translates to STC and overlays the expected model curve.
Reading the shape:
- **Steps/notches** in the curve → bypass diodes active: shading, cracked cells, hot spots.
- **Reduced slope near Isc (curve leans)** → shunt losses, PID, or mismatch.
- **Rounded knee / slanted near Voc** → high series resistance: bad connectors, corroded
  joints, undersized/damaged cables.
- **Uniformly low current** → soiling, degradation, wrong irradiance reading.
- **Low voltage** → missing/shorted modules, temperature error.
Fill factor and Pmax deviation (%) give a number to report and trend.

## 4. Insulation resistance
- With the string isolated and **PV+ and PV− shorted together through a suitable
  device** (method per IEC 62446-1; or test each pole to earth), test to the frame/earth at
  the specified test voltage (commonly 500 or 1000 V DC depending on system voltage).
- Minimum values are typically ≥ 1 MΩ for larger systems (per standard/table — check).
- Low insulation readings: isolate further (split string, test half by half) to find the
  damaged cable or module. Damp mornings reveal faults that are gone by noon.
- Only use insulation testers designed for PV (they handle the live DC source); some
  general testers are damaged or unsafe.

## 5. Thermal camera
Under load at good irradiance: scan from the back if possible (reflections on glass mislead).
Hot cell (single cell much hotter), hot substring (bypass active), hot junction box, hot
connectors. Note ΔT vs normal cells and log with irradiance.

## Gotchas
- Irradiance sensor at a different tilt or in shade invalidates every STC translation.
- Temperature: a sensor not in contact with the back sheet gives wrong Voc expectations.
- Drones with radiometric cameras are great for screening; confirm on the ground.

## Verify
- [ ] Irradiance ≥ threshold, in-plane, stable; module temperature measured.
- [ ] String isolated and zero current verified before connecting.
- [ ] Voc/Isc compared with temperature/irradiance-corrected expectations.
- [ ] IV shape interpreted; Pmax deviation recorded.
- [ ] Insulation test at correct voltage; result vs minimum logged.

*Uncertain:* thresholds and test voltages vary by standard edition and system voltage; check
the current IEC 62446-1 and your instrument manual.
