---
id: engineering-technology.automotive-vehicle-engineering.ev-battery-systems.charge-curve-design
name: charge-curve-design
category: engineering-technology
field: automotive-vehicle-engineering
product: ev-battery-systems
tags: [charge-curve, cc-cv, fast-charging, charge-taper, lithium-plating-limit, c-rate-profile]
level: practitioner
status: verified
description: "Design the DC fast-charge current profile versus SOC and temperature: CC-CV and stepped CC, plating and voltage limits, and the 10-80% time target."
sources:
  - "Plett, Battery Management Systems Vol. 1"
  - "Warner, Lithium-Ion Battery Chemistries and Pack Design"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# Charge curve design

1. Constraints: maximum cell voltage (at the CV phase), maximum cell current by temperature, anode potential/plating risk (higher SOC and lower temperature reduce permitted current), cell temperature limit, charger and cable capability, pack fusing and contactor ratings.
2. Profile shape: constant current at the allowed rate up to the voltage limit, then taper (CV); real fast-charge curves step current down as SOC rises (multi-step CC) to stay under the plating/voltage limit.
3. Build the limit map `I_limit(SOC, T)` from cell supplier data, then validate on cells with a lab test (post-mortem or three-electrode analysis for plating where possible).
4. Targets: 10-80% time (vehicle level) is the customer metric; the average C-rate is `0.7/time_h`. For example 18 min for 10-80% needs about 2.3C average (computed 0.7/0.3 = 2.33C).
5. Interact with thermal: higher current heats the pack; preconditioning and cooling set the achievable curve.
6. Ageing trade-off: charge-curve aggressiveness versus cycle life; compare with warranty model.
7. Communication: BMS requests current via the charging protocol each cycle; the charger follows.

**Gotchas:** the curve changes with pack ageing and temperature; do not hard-code.

## Verify
- [ ] Curve measured at the target temperatures against the map; no violation.
- [ ] Ageing test confirms capacity retention goals for the chosen curve.
