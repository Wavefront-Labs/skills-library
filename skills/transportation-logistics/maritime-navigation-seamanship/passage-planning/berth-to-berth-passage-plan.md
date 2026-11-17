---
id: transportation-logistics.maritime-navigation-seamanship.passage-planning.berth-to-berth-passage-plan
name: berth-to-berth-passage-plan
category: transportation-logistics
field: maritime-navigation-seamanship
product: passage-planning
tags: [passage-planning, voyage-planning, maritime-navigation-seamanship, appraisal-planning-execution-monitoring, apem, imo-a893, under-keel-clearance, ukc, squat, tidal-window, no-go-areas, wheel-over, abort-point, contingency-anchorage, weather-routing, sailing-directions, admiralty-list-of-lights, tide-tables, notices-to-mariners, ships-routeing, tss, ecdis-route, great-circle, rhumb-line, load-line-zones, eca]
level: practitioner
status: draft
description: "Write a berth-to-berth passage plan using appraisal-planning-execution-monitoring: publications, UKC and squat, no-go areas, wheel-over and abort points, contingencies and weather routing."
sources: ["IMO Resolution A.893(21) Guidelines for voyage planning"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Berth-to-berth passage plan — think it through before letting go

**Goal:** a plan, approved by the master and briefed to all OOWs, that covers the
whole voyage from berth to berth, including pilotage waters, built on the four stages
of IMO A.893: **appraisal, planning, execution, monitoring**.

## 1. Appraisal — gather everything
- Charts (ENC/paper) at the right scales for the whole route, corrected to date;
  T&P notices; navigational warnings.
- Sailing directions, list of lights, radio signals (VTS, reporting points, pilot
  boarding), tide tables and tidal stream atlases, ocean passages/routeing charts,
  ships' routeing (TSS, deep-water routes, areas to be avoided).
- Ship particulars: draught (arrival/departure, trim), air draught, manoeuvring data,
  equipment defects.
- Regulations on the route: ECAs (fuel changeover points), load line zones, MARPOL
  special areas, ballast water rules, mandatory reporting.
- Weather: seasonal (pilot charts) and forecast; weather routing service if used.

## 2. Planning — draw it
1. **Route:** great circle offshore where safe (shorter), rhumb lines near the coast;
   respect TSS and recommended routes; distance off dangers per SMS (e.g. ≥ 2 nm off
   coast offshore where practicable).
2. **No-go areas:** shade water shallower than the safety depth (see UKC below).
   Margins of safety around them; clearing lines/bearings.
3. **UKC:** required UKC = static draught + squat + allowances ≤ charted depth + height
   of tide. Squat estimate (Barrass, approximate): open water `≈ Cb × V² / 100` m,
   confined channel `≈ 2 × Cb × V² / 100` m (V in knots). Check company minimum UKC
   (e.g. 10% of draught in port approaches). Where tide is needed, define a **tidal window**.
4. **Leg details:** course, distance, speed, ETA, XTD limits, **wheel-over points**
   (from turning data), parallel index lines, fix method and interval per area.
5. **Abort points** (last point to turn back before a narrow entrance) and **points
   of no return**; **contingency anchorages** and emergency berths.
6. Reporting points, VTS channels, pilot boarding area, tug requirements, speed limits.
7. Changes of steering mode, engine readiness (standby), and when extra watchkeepers
   or the master must be on the bridge.

## 3. Execution
- Brief all OOWs; master signs the plan.
- Adjust ETAs for weather/current; recheck tidal windows if ETA changes.
- Weather routing: avoid heavy weather sectors; slow steaming or diversion weighed
  against risk, fuel and charter-party terms.

## 4. Monitoring
- Fix and track checks per the plan; ECDIS route check and display set as planned
  (see transportation-logistics.maritime-navigation-seamanship.ecdis.ecdis-route-check-and-safety-settings).
- Deviations from plan approved and recorded, plan amended and re-briefed.

## Gotchas
- Plan "pilot to pilot" only — the pilotage waters are where groundings happen.
  Pilot on board does not remove the need for the ship's plan.
- Squat increases sharply with speed (V²) in shallow/confined water.
- Air draught under bridges and power lines; check at the tidal height for the transit.
- Copying last voyage's plan without rechecking updates and draught.

## Verify
- [ ] All charts and publications for the whole route listed and up to date.
- [ ] UKC calculated for the most critical points with squat; tidal windows defined.
- [ ] No-go areas, wheel-overs, abort points and contingency anchorages marked.
- [ ] Master signed; all OOWs briefed and signed.
- [ ] ECDIS route matches the plan and passed a route check.

*Uncertainty:* Barrass squat formula is an approximation; use ship-specific squat tables where available; distance-off and UKC values are SMS-dependent.
