---
id: transportation-logistics.maritime-navigation-seamanship.ecdis.ecdis-route-check-and-safety-settings
name: ecdis-route-check-and-safety-settings
category: transportation-logistics
field: maritime-navigation-seamanship
product: ecdis
tags: [ecdis, electronic-chart, enc, s-57, s-101, s-52, maritime-navigation-seamanship, safety-contour, safety-depth, shallow-contour, deep-contour, route-check, route-planning, cross-track-distance, xtd, chart-updates, avcs, permits, alarms, anti-grounding, look-ahead, scamin, overscale, catzoc, zoc, imo-stcw, type-specific-training, passage-planning]
level: practitioner
status: draft
description: "Set ECDIS safety contour/depth from draught and UKC, keep ENCs updated, run and resolve a route check with proper XTD, and configure alarms and display so dangers actually show."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# ECDIS route check and safety settings — make the chart warn you in time

**Goal:** configure ECDIS so it reliably alerts to shallow water and dangers along the
planned route, and confirm that by checking, not trusting, the automatic route check.
Menus differ by manufacturer (type-specific training is required under STCW/ISM);
the settings and logic are common to IMO-compliant systems.

## 1. Charts first
- Correct **ENC permits** installed and current (e.g. AVCS); **weekly updates** applied
  (base + updates, not just base). Check the update status report for every cell on
  the route — gaps show as missing/not-up-to-date cells.
- T&P notices and navigational warnings (NAVTEX, NAVAREA) entered as manual
  updates/mariner's objects where they affect the route.
- Note areas where only **RNC/raster** or no ENC exists: raster mode does not give
  depth-contour alarms — plan extra monitoring there.

## 2. Safety values (the core calculation)
- **Safety depth** = static draught + required UKC + squat allowance + other
  allowances (tide error, swell/heave, ZOC uncertainty). Soundings shallower than
  this show bold.
- **Safety contour** = set it equal to (or just above) the same value. ECDIS uses the
  **next deeper contour available** in the ENC: set 13.4 m and the displayed safety
  contour may be the 20 m line. Check which contour was actually adopted on screen.
- **Shallow contour** ≈ draught; **deep contour** ≈ e.g. 2× draught, to shade water.
- When planning to use the tide, compute on the tidal height for transit time and
  adjust — document it in the passage plan.

## 3. Build and check the route
1. Create waypoints; set **XTD/corridor** per leg: wide offshore, narrow in pilotage
   waters but not so narrow it's impossible to keep (and not wider than the safe water).
2. Set turn radius and speed per leg; check wheel-over points.
3. Run the **route check** with current safety settings. It reports crossings of the
   safety contour, dangers, restricted areas, and areas with special conditions inside
   the corridor.
4. **Resolve every item**: modify the route, or record an acceptance with reason
   (e.g. "precautionary area — no action, monitored"). Never ignore a long list.
5. **Visual check at the correct scale**: scroll the whole route at the compilation
   scale of the ENCs. Automatic checks can miss objects that only show at larger
   scales (SCAMIN) or isolated dangers depending on settings.

## 4. Display and alarms during the passage
- Display: **Standard** base + all relevant layers (isolated dangers, spot soundings
  near the track, unknown objects). "Base" display alone hides too much.
- Turn on **isolated dangers in shallow water** and check day/dusk/night palette.
- Look-ahead (anti-grounding) zone: ahead time in minutes, enough to stop or turn
  (e.g. 6–12 min depending on speed and manoeuvrability), wide enough to include the XTD.
- Alarms on: safety-contour crossing, off-track, approach to waypoint, position
  source loss, datum mismatch. Investigate every alarm; do not mute systematically.
- Avoid **overscale** (zoomed beyond compilation scale — position of objects is less
  precise than it looks); check **CATZOC/ZOC** quality of survey data in the area.

## 5. Cross-check position
Compare the ECDIS position (from GNSS) with radar overlay, visual bearings and parallel
indexes; never let one sensor be the only proof. See
transportation-logistics.maritime-navigation-seamanship.radar-arpa.radar-tuning-and-collision-plotting.

## Gotchas
- Safety contour silently snapping to a much deeper/shallower contour.
- Route check run with different safety settings than those used on passage.
- Updates applied on one ECDIS but not the backup.
- Over-reliance: "the line is green" ≠ the area was checked visually.

## Verify
- [ ] All ENCs on route licensed and updated to the latest weekly update.
- [ ] Safety depth/contour calculation written in the passage plan; adopted contour noted.
- [ ] Route check items each resolved or accepted with reason.
- [ ] Visual scroll done at appropriate scale; alarms and look-ahead set and tested.
- [ ] Backup ECDIS has the same route, charts and settings.

*Uncertainty:* typical numeric settings vary by company SMS; follow the SMS where it specifies values.
