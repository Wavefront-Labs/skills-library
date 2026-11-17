---
id: energy-mining-utilities.mineral-mining.gas-monitoring-systems.using-and-calibrating-mine-gas-detectors
name: using-and-calibrating-mine-gas-detectors
category: energy-mining-utilities
field: mineral-mining
product: gas-monitoring-systems
tags: [gas-monitoring-systems, gas-detection, multi-gas-detector, personal-gas-monitor, bump-test, calibration, calibration-gas, span, zero, methane, ch4, lel, carbon-monoxide, co, oxygen, o2, hydrogen-sulphide, h2s, nitrogen-dioxide, no2, catalytic-bead, infrared-sensor, electrochemical-sensor, sensor-poisoning, telemetric-monitoring, tube-bundle, gas-chromatograph, alarm-response, underground-mining, coal-mining]
level: practitioner
status: gated
description: "Use mine gas detection: bump-testing and calibrating multi-gas detectors, sampling technique by gas density, reading fixed telemetric sensors and tube bundle data, and alarm response."
sources:
  - "https://www.ecfr.gov/current/title-30/part-75/section-75.320"
  - "https://www.ecfr.gov/current/title-30/part-75/section-75.342"
  - "https://www.ecfr.gov/current/title-30/part-75/section-75.323"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Using and calibrating mine gas detectors

**Goal:** trust your gas readings — because the instrument has been checked, you sampled
in the right place, and you respond correctly when it alarms.

> Alarm setpoints and statutory limits vary by country and by coal vs
> metalliferous mines; your detector's manual and site procedures govern. Sensor
> behaviour notes below are general and model-dependent.

## 1. Before each shift: bump test
- A **bump test** exposes the detector briefly to a known gas mix to confirm the sensors
  respond and the alarms (audible, visual, vibration) fire. Do it daily before use (gated: unconfirmed, source is paywalled or blocked),
  following the maker's recommendation, typically with a docking station.
- A **calibration** adjusts the readings to match the known gas concentration (zero in
  clean air, span with the cylinder). Done on a schedule (US underground coal, 30 CFR 75.320(a): at least once every 31 days for methane detectors; check the maker and your regulator for other gases and commodities) or after a
  failed bump test or a sensor change.
- Check the cylinder is in date and the concentration on its label matches the
  detector's settings. Expired or wrong cal gas silently produces a wrongly calibrated
  instrument.
- Zero only in known clean air — zeroing underground in contaminated air sets the
  baseline wrong.

## 2. How the sensors behave
- **Catalytic bead (pellistor)** methane sensors read %LEL and need oxygen to work;
  in very low oxygen they under-read. Silicones, sulphides and lead compounds **poison** (gated: unconfirmed, source is paywalled or blocked)
  them; high methane can also over-range and damage them. Many coal-mine instruments
  use **infrared** methane sensors instead, which don't need oxygen and aren't
  poisoned, but don't respond to hydrogen.
- **Electrochemical** sensors (CO, H₂S, O₂, NO₂) have cross-sensitivities — e.g. some
  CO sensors respond to hydrogen (such as from battery charging) (gated: unconfirmed, source is paywalled or blocked) — check the
  manufacturer's cross-sensitivity table before trusting an odd reading.
- Sensors have warm-up times and life spans; replace at end of life.

## 3. Sampling technique
- **Methane** is lighter than air: test at the roof, in cavities and high points,
  and in the "dead" space close to the face.
- **CO₂ and H₂S** are heavier: test low down, in sumps, winzes and confined spaces.
- **CO** mixes broadly; test after blasting, near diesels and anywhere a fire is
  suspected.
- Use an aspirated probe or a sampling pump with tubing to reach into places you
  shouldn't put your head; allow the stated time per metre of tubing.
- Test before entering, while working, and when conditions change.

## 4. Fixed systems
- **Telemetric sensors** (real-time) at fixed points report to a surface control room
  and can trip power automatically. In US underground coal, 30 CFR 75.342 requires methane monitors to be calibrated at least every 31 days, to give a warning signal at 1.0% methane and to deenergize at 2.0% or when the monitor is not operating properly. Respect their calibration schedule and position
  rules; a sensor moved out of the airstream reads nothing.
- **Tube bundle** systems draw air through tubes to a surface analyser (often a gas
  chromatograph). Slower (minutes of delay) but measure a wider range and gases like
  hydrogen and ethylene, useful for spontaneous combustion trending in coal goafs.
- Watch **trends and ratios** (e.g. CO make, Graham's ratio for heating) rather than
  single readings — interpretation is a specialist task.

## 5. Alarm response
- First alarm: stop work, step back toward fresh air, confirm the reading, notify
  supervision. Above action levels (US coal, 30 CFR 75.323: at 1.0% methane in a working place or intake air course equipment is deenergized; at 1.5% persons are withdrawn): withdraw people and remove power as the rules
  require.
- Never silence and carry on. Never assume it is "just the sensor" until it has been
  checked against another instrument.

## Gotchas
- A detector worn under clothing reads the air inside your jacket.
- Low battery mid-shift: leave the area as if you had no detector.
- Dropped detectors need a bump test before re-use.

## Verify
- [ ] Bump test passed today; calibration in date; cal gas in date.
- [ ] Sampling heights matched the gas being sought.
- [ ] Cross-sensitivities considered for unexpected readings.
- [ ] Fixed sensor positions and calibration records current.
- [ ] Alarm actions taken and recorded.

## Checked

Date checked: 2026-10-25. Jurisdiction: United States, underground coal (MSHA, 30 CFR Part 75).

Sources: https://www.ecfr.gov/current/title-30/part-75/section-75.320; https://www.ecfr.gov/current/title-30/part-75/section-75.342; https://www.ecfr.gov/current/title-30/part-75/section-75.323 (versions: current eCFR and web pages as read on the date above).

Confirmed: 75.320(a): methane detectors calibrated with a known methane-air mixture at least once every 31 days. 75.342: methane monitors calibrated at least every 31 days, warning signal at 1.0% methane, automatic deenergizing at 2.0% or when the monitor is not operating properly. 75.323: 1.0% methane in a working place or intake air course deenergizes equipment, 1.5% withdraws persons and disconnects power.

Gated: claims marked as gated were not confirmed. The daily bump-test practice, catalytic-bead poisoning and electrochemical cross-sensitivity statements come from manufacturer guidance that was not fetched.

Method: documentation only; no commands were run.
