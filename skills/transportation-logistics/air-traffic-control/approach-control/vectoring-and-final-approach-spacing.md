---
id: transportation-logistics.air-traffic-control.approach-control.vectoring-and-final-approach-spacing
name: vectoring-and-final-approach-spacing
category: transportation-logistics
field: air-traffic-control
product: approach-control
tags: [air-traffic-control, atc, approach-control, terminal-control, tracon, radar-vectoring, final-approach, ils-intercept, localizer, base-turn, downwind, speed-control, arrival-sequencing, spacing, wake-turbulence, recat, trombone, point-merge, missed-approach, minimum-vectoring-altitude, mva, compression, descent-planning, terminal-airspace]
level: practitioner
status: gated
description: "Vector arrivals onto final with consistent spacing: build the sequence, use speed control and base turns, allow for compression, and manage missed approaches."
sources: ["https://www.faa.gov/air_traffic/publications/atpubs/atc_html/chap5_section_5.html", "https://www.faa.gov/documentLibrary/media/Order/JO_7110_659C.pdf"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Vectoring and final-approach spacing

**Goal:** a steady stream of arrivals crossing the threshold at the required interval,
achieved early with small corrections rather than late with orbits.

> Draft: numbers are typical illustrations, not rules. Your unit sets minima
> (commonly 3 NM radar (gated: unconfirmed, source is paywalled or blocked), 2.5 NM on final where approved, wake distances), intercept
> angles and speed limits.

## 1. Build the sequence early
1. Decide the **landing order** 30–40 NM out using estimated times, wake category and
   the gap tower wants for departures.
2. Write it down (strip order, sequence list or AMAN). Tell each aircraft its number
   and type of approach early.
3. Identify the **spacing target** for each pair = max(radar minimum, wake minimum,
   tower's requested gap). Example ICAO legacy wake: Medium behind Heavy 5 NM (gated: unconfirmed, source is paywalled or blocked),
   Light behind Heavy 6 NM (gated: unconfirmed, source is paywalled or blocked) — check whether your unit uses RECAT-EU/US.

## 2. The tools, in order of preference
1. **Speed control** (cheapest, invisible to the pilot's workload): e.g. 250 kt in
   descent, 210–220 on downwind, 180 on base/intercept, 160 kt to ~4 NM (a common
   practice, not a rule (gated: unconfirmed, source is paywalled or blocked); jets may not hold slower than ~160 clean). Never assign a speed change
   inside ~4 NM final.
2. **Path stretching**: extend downwind ("trombone"), dog-legs, point-merge arcs.
3. **Base turn timing**: the main precision lever.
4. **Orbits/holding**: last resort, and only where separated and charted.

## 3. Turning onto final
- Intercept heading (gated: unconfirmed, source is paywalled or blocked): usually ≤ 30° to the localiser (≤ 45° may be allowed in some
  rules for approaches with tighter turns); intercept at least ~2 NM before the final
  approach fix and below the glideslope so the aircraft captures from below.
- Clearance pattern: "Turn left heading 240, descend 3,000 ft, cleared ILS runway 27"
  — heading, altitude above MVA, approach clearance.
- **Lead the turn** for groundspeed: a 250 kt groundspeed turns wide; with a strong
  tailwind on base, turn earlier.
- Check the vector keeps the aircraft at or above the **MVA** with the map on.

## 4. Compression
Spacing shrinks on final because the leader slows first. Plan **extra on the base
turn**: if you need 3 NM at the threshold, aim for ~4 NM as the follower turns final
with a headwind on final; less with calm wind. Calibrate per runway and per wind.
Watch groundspeeds, not IAS: a 25 kt headwind at 2,000 ft changes everything.

## 5. Missed approaches and breakouts
- Know the published missed approach and your unit's coordination with tower.
- A go-around climbs into the following traffic's downwind: have a heading and
  altitude ready for both.
- If spacing is lost on final: **break out early** with a clear instruction ("turn
  right heading 360, climb 4,000 ft, I'll bring you back around") rather than hope.

## 6. Gotchas
- Uncorrected tailwind on base produces overshoots through the localiser — and close
  parallels make that a separation issue.
- Speed restrictions must be cancelled or updated; "resume normal speed" is easy to forget.
- Light aircraft in a jet stream: assign them a separate gap, not a slot at jet speed.
- Read MVA altitudes, not memory, when the active runway changes.

## Verify
- [ ] Landing order was set before aircraft reached the downwind.
- [ ] Every pair's target spacing accounts for wake category.
- [ ] Intercepts are within angle limits, below glideslope and above MVA.
- [ ] Measured threshold spacing matches the plan within ~0.5 NM after a few cycles.
- [ ] You have a go-around plan for every aircraft inside 10 NM.

## Checked

Jurisdiction: US (FAA JO 7110.65) and ICAO wake categories. Checked 2026-10-25 by search excerpts of FAA JO 7110.65 chapter 5: 2.5 NM separation on the final approach course within 10 NM of the runway is authorised only in the conditions the order sets (FUSION or single-sensor slant range within 40 miles of the antenna) and with wake turbulence separation applied; small behind heavy is 6 miles; wake recategorisation (JO 7110.659C) replaces the legacy table where authorised. The 3 NM radar minimum, speed schedules, intercept angles and the ICAO medium-behind-heavy 5 NM figure were not confirmed and are marked gated. FAA pages (JO 7110.65, AIM) returned 403 to the fetch tool; search-result excerpts were used where stated.

Method: documentation only; no commands were run.
