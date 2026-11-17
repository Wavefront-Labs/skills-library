---
id: natural-sciences.atmospheric-sciences.atmospheric-chemistry.trace-gas-and-aerosol-measurement-qa
name: trace-gas-and-aerosol-measurement-qa
category: natural-sciences
field: atmospheric-sciences
product: atmospheric-chemistry
tags: [atmospheric-chemistry, air-quality, trace-gas, ozone, no2, nox, co, so2, co2, ch4, aerosol, pm2.5, pm10, particulate-matter, inlet-design, zero-and-span, calibration-gas, gpt, multipoint-calibration, mixing-ratio, ppb, ppm, stp-correction, data-flagging, quality-assurance, low-cost-sensors, collocation, humidity-correction, gaw, wmo-scale]
level: advanced
status: gated
description: "Run trace-gas and aerosol instruments so the data hold up: inlet design, zero/span and multipoint calibration traceable to standards, data flagging, unit conventions and low-cost sensor collocation."
sources: []
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Trace-gas and aerosol measurement QA

**Goal:** a time series of atmospheric concentrations (O₃, NOx, CO, SO₂, CO₂/CH₄, PM)
that is traceable to recognised standards, with known uncertainty and every bad period
flagged — the difference between a dataset others can use and a pretty plot.

## 1. Inlet and sampling line
- Inlet away from local sources (exhausts, vents, vegetation canopy edge) and obstructions;
  height and siting per the network's criteria (e.g. regulatory siting rules, WMO GAW guidance).
- Reactive gases: **PFA/PTFE** tubing, short as practical, with high flow to keep residence
  time short (seconds). O₃ is lost on dirty or long lines (gated: unconfirmed, source is paywalled or blocked); NO + O₃ react in the line,
  shifting the NO/NO₂ split — keep residence time low and correct if necessary.
- Particulate filter in gas lines (PTFE, changed on schedule; a dirty filter scrubs O₃).
- Aerosol: size-selective inlet (PM10/PM2.5 cyclone or impactor) at its **design flow** —
  the cut size depends on flow rate. Avoid bends and long horizontal runs (particle losses);
  use conductive tubing (stainless or conductive silicone) to avoid electrostatic losses.
- Dry aerosol samples to RH < ~40 % before sizing/measuring where the method says so; water
  uptake inflates particle size and mass.

## 2. Calibration
- **Zero and span** checks routinely (daily/automated for many analysers): zero air
  (scrubbed, certified) and span gas near the upper part of the expected range.
  Track drift; adjust only according to the SOP, not every day by eye.
- **Multipoint calibration** (e.g. 5 points across range (gated: unconfirmed, source is paywalled or blocked) at installation, after repairs and
  periodically, to confirm linearity.
- Standards must be traceable: gas cylinders with certificates; O₃ via a transfer standard
  photometer referenced to a standard reference photometer; GHG measurements on the **WMO
  scale** for CO₂/CH₄ (e.g. via NOAA-calibrated tanks).
- NO₂ converter efficiency (molybdenum converters) checked by **gas-phase titration**; note
  that molybdenum converters also convert some other oxidised nitrogen species (PAN, HNO₃),
  so "NO₂" is an upper bound.
- Flow calibration for aerosol samplers with a traceable flow meter.

## 3. Units and conventions
- Gases: **mixing ratio** (ppb, ppm; nmol/mol) is independent of temperature and pressure.
  Mass concentration (µg/m³) depends on T and P: state the reference conditions (local vs
  standard, e.g. 20 °C or 25 °C and 1013.25 hPa — regulations differ).
- Convert ppb to µg/m³: µg/m³ = ppb × M / V_m, with V_m ≈ 24.45 L/mol at 25 °C and 1 atm (computed RT/P = 24.465; at 20 °C it is 24.06, so 100 ppb O₃ is 196 µg/m³ at 25 °C and 200 µg/m³ at 20 °C).
- Time stamps in UTC; state whether averages are period-beginning or period-ending.

## 4. Data flagging and processing
- Flag calibration periods, instrument faults, maintenance, power outages and local
  contamination events (e.g. a generator, wind from a nearby road) — keep flags with data
  rather than deleting points.
- Apply zero/span drift corrections per the SOP (linear interpolation between checks is common).
- Compute averages only with sufficient coverage (e.g. ≥ 75 % of valid points in the hour (gated: unconfirmed, source is paywalled or blocked).
- Keep raw data, processed data and the processing version.

## 5. Low-cost sensors
Electrochemical gas sensors and optical PM sensors are cross-sensitive (temperature,
humidity, other gases) and drift. **Collocate** with a reference instrument for weeks
covering the range of conditions, build a correction (often including RH and T), and
re-check periodically. Optical PM sensors overestimate in high humidity; their mass
estimate depends on assumed particle properties.

## Gotchas
- O₃ analysers (UV absorption) have interferences from aromatic compounds and mercury in
  some settings.
- Ambient temperature swings in a non-climate-controlled shelter shift analyser baselines.
- Leaks upstream of the instrument dilute the sample — leak-check after every line change.
- A regulatory method (e.g. reference/equivalent designation) may be required for compliance data.

Uncertain here: specific intervals and acceptance limits are network-specific; follow the
SOP of the network the data report to.

## Verify
- [ ] Inlet materials, length/residence time and size-cut flow documented.
- [ ] Zero/span and multipoint calibrations logged against traceable standards.
- [ ] Units and reference conditions stated; times in UTC.
- [ ] Flags applied for calibrations, faults and local contamination; raw data retained.
- [ ] Low-cost sensor data corrected from a documented collocation.
