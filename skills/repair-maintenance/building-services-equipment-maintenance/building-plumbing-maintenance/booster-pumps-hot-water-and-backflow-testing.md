---
id: repair-maintenance.building-services-equipment-maintenance.building-plumbing-maintenance.booster-pumps-hot-water-and-backflow-testing
name: booster-pumps-hot-water-and-backflow-testing
category: repair-maintenance
field: building-services-equipment-maintenance
product: building-plumbing-maintenance
tags: [building-services-equipment-maintenance, building-plumbing-maintenance, plumbing, booster-set, booster-pump, pressure-vessel, accumulator, pre-charge, calorifier, water-heater, hot-water-plant, legionella, tmv, thermostatic-mixing-valve, backflow-preventer, rpz, reduced-pressure-zone, double-check-valve, backflow-test-kit, risers, prv, pressure-reducing-valve, drain-jetting, cctv-drain-survey, grease-trap, l8, hsg274, asse-5110]
level: practitioner
status: docs-checked
description: "Maintain building water services: booster set pressures and vessel pre-charge, hot-water plant temperatures and calorifier blowdown, TMVs, RPZ backflow tests and planned drain jetting."
sources: ["https://www.hse.gov.uk/legionnaires/hot-and-cold.htm", "https://www.hse.gov.uk/healthservices/scalding-burning.htm", "https://www.hse.gov.uk/pubns/books/hsg274.htm"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Booster pumps, hot water and backflow testing

**Goal:** steady pressure at every outlet, hot water that's safe (hot enough to control
legionella, not hot enough to scald at the tap), drinking water protected from
backflow, and drains that don't block. Local codes govern much of this — US plumbing
codes and ASSE standards, UK Water Supply (Water Fittings) Regulations, ACoP L8 and
HSG274 — so check the schedule your site follows.

## 1. Booster sets (monthly)
- Record **cut-in / cut-out pressures** (or VSD setpoint) and compare with design; check
  the highest outlet still has adequate pressure (to the design pressure at the most
  remote fixture).
- **Pressure vessel pre-charge:** isolate and drain the vessel water side, measure air
  pre-charge at the Schrader valve with a tyre gauge — set to the maker's value for the
  cut-in pressure. Low pre-charge → **rapid pump cycling**.
- Duty/standby rotation working; run hours balanced; no leaks at mechanical seals;
  non-return valves holding (pressure doesn't collapse when pumps stop).
- Break tank (where fitted): clean, lid sealed, float valve working, overflow screened;
  inspected and cleaned on the water-safety schedule.

## 2. Hot water plant
- Under the UK's HSG274 approach, calorifiers store at **≥60 °C**, distribute so outlets
  reach **≥50 °C (≥55 °C in healthcare)** within one minute; US sites follow their
  ASHRAE 188 water management plan. Follow your site's water management plan.
- Monthly: flow and return temperatures at the calorifier; sentinel outlet temperatures
  (nearest and furthest outlets on each loop).
- **Blowdown** calorifier drain to remove sediment (at the frequency in your written scheme). Annual inspection/descale per plan; pressure
  relief and temperature/pressure relief valves tested.
- Circulation pumps running; balancing valves set so returns stay hot.

## 3. Thermostatic mixing valves (TMVs)
Where scalding risk exists (care homes, schools, hospitals), TMVs limit outlet temperature
(HSE: a Type 3 TMV so water is not discharged above 44 °C where vulnerable people use baths and showers). Test: measure mixed temp; then isolate cold supply
— outlet must shut off or reduce to a safe trickle within the standard's time. Service
strainers and check valves; record annually or more often.

## 4. Backflow preventers
- Device type follows hazard: **RPZ (reduced pressure zone)** for high hazard (e.g. boiler
  feed with chemicals, irrigation with fertiliser), **double check valve** for lower hazard.
- **Testing:** by a certified tester with a calibrated differential pressure gauge kit,
  annually (often required by the water authority) and after installation or repair.
  RPZ test checks: check valve 1 holds the minimum differential, the relief valve opens
  at its minimum differential, and check valve 2 holds tight; the minimum values come from
  the test procedure you follow. Follow the test procedure for the jurisdiction exactly.
- An RPZ dumping water continuously = fouled first check or relief valve; never plug the
  relief outlet.

## 5. Drains
- Planned **jetting** of known problem runs (kitchen lines, long horizontal soil runs)
  on a schedule set by the problem history; **grease traps** emptied on a schedule that
  stops fats building up.
- CCTV survey a recurring blockage before repeated jetting — root ingress, collapsed pipe
  or poor fall can't be jetted away.
- Floor gullies and traps topped up (dry traps let sewer gas in).

## 6. Pressure reducing valves and risers
Check downstream pressure gauges against setpoint on each PRV station; PRV creep shows
as rising pressure at no-flow. Exercise isolation valves annually so they'll actually
close when needed.

## Gotchas
- Dead legs (unused outlets) grow legionella: flush per the water management plan or remove the pipework.
- Raising calorifier temperature without TMVs raises scald risk.
- Rapid pump cycling destroys seals and motors — check the vessel first.

## Verify
- [ ] Booster pressures and vessel pre-charge recorded; pumps not short-cycling.
- [ ] Calorifier flow/return and sentinel temperatures within plan limits.
- [ ] TMV fail-safe test passed and recorded.
- [ ] Backflow test reports current and filed with the water authority if required.
- [ ] Drain jetting/CCTV logged by location with findings.

## Checked

Date checked: 2026-10-25. Jurisdiction: United Kingdom (HSE HSG274 Part 2 and scalding guidance); US codes mentioned only by name.
HSE hot and cold water page: hot water stored at 60 C or higher and distributed so outlets reach 50 C (55 C in healthcare) within one minute, monthly checks of sentinel outlets and cylinder temperatures, TMV inlet temperature measured at the hot supply. HSE scalding page: Type 3 TMV so water is not discharged above 44 C where vulnerable people can use baths and showers, TMVs as close to the outlet as possible, pipe runs after TMVs not over 2 m. HSG274 second edition (March 2024) has Part 2 for hot and cold water. Removed unconfirmed claims: minimum pressure at remote outlet, vessel pre-charge offset, ASHRAE 188 storage temperature, blowdown interval, RPZ differential values, jetting interval and grease trap fill level, weekly flushing.

Method: documentation only; no commands were run.
