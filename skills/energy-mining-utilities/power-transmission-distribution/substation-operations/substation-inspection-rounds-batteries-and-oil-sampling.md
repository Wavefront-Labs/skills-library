---
id: energy-mining-utilities.power-transmission-distribution.substation-operations.substation-inspection-rounds-batteries-and-oil-sampling
name: substation-inspection-rounds-batteries-and-oil-sampling
category: energy-mining-utilities
field: power-transmission-distribution
product: substation-operations
tags: [substation-operations, substation, zone-substation, switchyard, inspection-round, routine-inspection, power-transformer, oil-level, winding-temperature, oil-temperature, buchholz-relay, silica-gel-breather, tap-changer, oltc, sf6, gas-density, circuit-breaker, dc-battery, battery-charger, float-voltage, specific-gravity, dc-earth-fault, oil-sampling, dga, dissolved-gas-analysis, transformer-oil, thermography, infrared-scan]
level: practitioner
status: draft
description: "Walk a substation inspection round that catches failures early: transformer gauges, breathers and leaks, SF6 density, DC battery and charger checks, and taking a clean DGA oil sample."
sources:
  - "General utility substation maintenance practice; IEEE C57.104 and IEC 60599 for the principles of dissolved-gas interpretation (summarised, not reproduced)"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Substation inspection rounds, battery checks and oil sampling

**Goal:** spot a failing transformer, breaker or battery weeks before it fails, and
record readings in a form that shows trends. You are entering a live site: you must
hold the right authorisation, stay on walkways, keep approach distances and never open
a cubicle or climb plant during a round.

## 1. Before entering
- Sign in (logbook or remote check-in with control), state purpose and duration.
- Look at the site from the gate: anything burning, smoking, humming abnormally,
  oil on the ground, fence damage, animals in the yard? If so, back off and call control.

## 2. Transformer checks
- **Oil level** on the conservator gauge, compared with oil temperature (a low level
  on a hot day is worse than on a cold one).
- **Oil and winding temperature gauges:** read the current value and the **maximum
  pointer**, record both, then reset the max pointer if your procedure says so.
- **Breather silica gel:** note the colour band. Most gels change from orange to
  green, or blue to pink, as they saturate; replace well before it is all changed.
  Check the oil cup at the bottom has oil in it.
- **Buchholz relay** window: any visible gas is significant — report it, don't vent it.
- **Leaks** at gaskets, valves, radiators, bushing bases. Photograph and mark.
- **Tap changer:** operations counter reading (trend it) and position indication
  matching SCADA.
- Fans and pumps: run when they should; no failed fan on a hot loaded day.

## 3. Switchgear
- **SF6 breakers:** read gas density gauges (green zone); a slow downward trend means
  a leak long before the alarm.
- Breaker operation counters, spring-charged indications, heater/condensation in
  outdoor kiosks, door seals.
- Unusual sounds: crackling or hissing near insulators or cable boxes can be
  partial discharge or tracking.
- Thermal scanning, where you are trained and equipped, from safe positions: compare
  like with like (phase A vs B vs C on the same load).

## 4. DC battery and charger
The battery trips the breakers. If it's flat when a fault happens, the protection
cannot clear the fault.
- **Charger:** output volts and amps, no alarms. Float voltage should match the
  manufacturer's figure; typical values are about 2.23–2.27 V/cell for vented
  lead-acid and about 1.40–1.45 V/cell for NiCd (**check the battery's datasheet**).
- **Cells:** electrolyte level between marks (vented types), no cracked cases,
  no corroded terminals, pilot-cell voltage and specific gravity if the procedure asks.
- **DC earth fault indicator:** an earth on either pole is a latent problem; a second
  earth can cause a false trip or fail-to-trip.
- Battery room ventilation working; no ignition sources; eyewash present.

## 5. Taking an oil sample for DGA
Do this only where authorised and the valve is accessible from a safe position.
1. Use the designated sampling valve (usually low on the tank). Wipe it clean.
2. **Flush** a quantity of oil to waste first (the stagnant oil in the valve is not
   representative) — the lab or procedure gives the volume.
3. Fill a clean **glass syringe** (or approved sample bottle) from the bottom up
   with no air bubbles; air contaminates the dissolved gas result.
4. Cap, label (asset, date, time, oil temperature, load if known) and protect from light.
5. Close the valve fully and check for drips.

Interpreting results is a specialist step, but know the headline pattern: hydrogen
points to partial discharge; ethylene/methane to overheating; **acetylene to arcing
— even small amounts deserve a quick call**; carbon monoxide/dioxide to paper
insulation ageing. **Trends** matter more than single values.

## 6. Record and report
Write every reading, not only defects. A spreadsheet of normal numbers is what makes
the abnormal one obvious. Raise defects with photos and priority.

## Verify
- [ ] Signed in; site scanned from the gate first.
- [ ] Transformer level, temperatures (including max), breather, Buchholz, leaks recorded.
- [ ] SF6 density and breaker counters recorded and trended.
- [ ] Charger, float voltage, cells and DC earth status checked.
- [ ] Oil sample flushed, bubble-free, labelled with temperature.
- [ ] Defects reported, readings logged, signed out.
