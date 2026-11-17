---
id: energy-mining-utilities.mineral-mining.mine-ventilation.airflow-surveys-and-ventilation-control
name: airflow-surveys-and-ventilation-control
category: energy-mining-utilities
field: mineral-mining
product: mine-ventilation
tags: [mine-ventilation, ventilation, ventilation-officer, airflow, air-quantity, anemometer, vane-anemometer, traverse, smoke-tube, pressure-survey, regulator, stopping, ventilation-door, airlock, auxiliary-fan, vent-duct, recirculation, methane, firedamp, carbon-monoxide, diesel-particulate, dust-suppression, heat-stress, wet-bulb, underground-mining, coal-mining]
level: practitioner
status: docs-checked
description: "Measure and control underground airflow: anemometer traverses, regulator and stopping work, auxiliary fan and duct set-up, and gas and dust checks against the plan."
sources:
  - "https://www.ecfr.gov/current/title-30/part-75/section-75.323"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Airflow surveys and ventilation control

**Goal:** confirm every working place gets the air it needs, adjust the circuit safely,
and catch recirculation and gas build-up before they hurt someone.

> Required quantities, velocities and gas limits are statutory and vary
> by country and commodity (coal is stricter). Network design is in
> engineering-technology.mining-geological-engineering.mine-ventilation.ventilation-network-and-fan-design.

## 1. Measuring air quantity
- **Quantity = average velocity × cross-sectional area** (m³/s = m/s × m²).
- Velocity: do a **moving traverse** with a vane anemometer: hold it at arm's length
  on a rod, upstream of your body, and sweep the whole cross-section slowly and evenly at the speed and duration your instrument and procedure specify. Repeat until two readings agree within a few percent. Apply the
  instrument's calibration correction; a body-in-airway correction is sometimes
  applied when standing in the airway.
- Very low velocities (below what a vane reads reliably) — use a smoke tube: time a
  puff over a measured distance and apply the correction factor from your procedure to get average velocity. Treat as approximate.
- Area: measure width and height at several points, or use a scan. Irregular
  headings make area the bigger error.
- Record location, time, velocity, area, quantity, and compare with the plan and the
  last survey.

## 2. Controls and adjusting them
- **Stoppings** block air; **regulators** (adjustable openings in a stopping) throttle
  a split; **doors** let traffic through — install them in pairs (airlock) so one is
  always shut.
- Changing a regulator affects other splits. Make one change at a time, then
  re-measure the affected places. Never adjust without authorisation from whoever
  controls the ventilation plan.
- Leaking stoppings and doors propped open are the commonest reason a face is short of
  air. Walk the circuit and fix them before reaching for fan changes.

## 3. Auxiliary (face) ventilation
- **Forcing** system: fan blows fresh air through duct to the face. Keep the duct end
  within the specified distance of the face (the distance set in your ventilation plan or standard) and the duct free of tears and kinks.
- **Recirculation trap:** the auxiliary fan must sit in fresh air, upstream of the
  return, with more air passing it in the main airway than the fan draws. Otherwise it
  re-breathes its own exhaust, concentrating gas, heat and diesel fumes.
- Never switch off an auxiliary fan and leave a dead-end heading occupied.

## 4. Gas, dust and heat
- Test before entering and regularly while working: methane at the roof and high
  points (it is light), CO₂ and H₂S low down, CO near diesels and after blasting.
  Statutory action levels apply (US coal, 30 CFR 75.323: at 1.0% methane in a working place or intake air course electrical equipment is deenergized and other mechanized equipment is shut off; at 1.5% everyone except persons permitted by the Act is withdrawn and power is disconnected at the power source; follow your own regulations).
- Dust: water sprays on cutters and transfer points, wet down muckpiles, scrubbers;
  personal sampling for respirable dust and silica.
- Heat: track wet-bulb temperature or the site's heat index; stop or rotate work above
  limits.

## Gotchas
- An open door can short-circuit a whole section; check doors before blaming a fan.
- Uneven traverses bias the result: lingering in the fast centre of the airway reads
  high, lingering near the walls reads low. Sweep at a steady pace.
- Diesel fleet changes alter the air requirement; recheck after adding machines.

## Verify
- [ ] Quantities measured at all working places and matched to plan/minimums.
- [ ] Doors in airlocks shut; stoppings intact.
- [ ] Auxiliary fans in fresh air, no recirculation, duct to face.
- [ ] Gas readings logged at the right heights; action levels known.
- [ ] Changes made one at a time and re-measured.

## Checked

Date checked: 2026-10-25. Jurisdiction: United States, underground coal for the methane action levels (MSHA, 30 CFR 75.323); the measurement method is general.

Sources: https://www.ecfr.gov/current/title-30/part-75/section-75.323 (versions: current eCFR and web pages as read on the date above).

Confirmed: 75.323: at 1.0% methane in a working place or intake air course electrical equipment is deenergized and other mechanized equipment shut off; at 1.5% everyone except persons permitted by section 104(c) is withdrawn and electrical equipment disconnected at the power source. The quantity formula (velocity x area) is dimensional arithmetic.

Method: documentation only; no commands were run.
