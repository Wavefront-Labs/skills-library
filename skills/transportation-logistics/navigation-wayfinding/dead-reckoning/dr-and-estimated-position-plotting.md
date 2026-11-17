---
id: transportation-logistics.navigation-wayfinding.dead-reckoning.dr-and-estimated-position-plotting
name: dr-and-estimated-position-plotting
category: transportation-logistics
field: navigation-wayfinding
product: dead-reckoning
tags: [dead-reckoning, dr, ded-reckoning, estimated-position, ep, navigation-wayfinding, speed-time-distance, course-to-steer, set-and-drift, tidal-stream, current-triangle, leeway, vector-triangle, chartwork, plotting, log, compass-course, true-course, variation, deviation, wind-triangle, heading, track, cog, sog, gnss-backup]
level: practitioner
status: draft
description: "Keep a dead-reckoning plot: speed-time-distance, DR vs EP with set, drift and leeway, course-to-steer vector triangles, compass error conversion, and checking DR against fixes."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# DR and estimated position plotting — always know roughly where you are

**Goal:** maintain a running position from heading, speed and time, improved by known
current and leeway, so that when GNSS fails (or disagrees) you have an independent
position good enough to stay safe. Notation below is marine; the same vector logic is
the aviation wind triangle.

## 1. Speed, time, distance
`D = S × T` (nm = kn × h). Useful forms:
- Minutes × speed ÷ 60 = distance (12 min at 10 kn = 2 nm).
- "Six-minute rule": distance in 6 min = speed ÷ 10 (in nm).
Keep a log: time, heading (and which reference), log reading/speed, events.

## 2. Compass conversion (True ↔ Compass)
True = Compass + deviation + variation (East +, West −).
Going compass → magnetic → true, **add East, subtract West** (mnemonic: "Cadbury's
Dairy Milk Very Tasty" for C-D-M-V-T, with "add Easterly" going that way).
Example: compass 045°, deviation 3° W, variation 5° E → magnetic 042°,
true 047°. Reverse the signs going true→compass.

## 3. DR vs EP
- **DR position:** from the last fix, along the **heading** (water track) for the distance
  run through the water. Ignores current and leeway. Plot with a single arrow.
- **EP (estimated position):** DR + **leeway** (wind pushes the boat sideways — estimate
  degrees from the angle between the wake and the centreline) + **set and drift** of the
  current/tidal stream for the same time. Plot water track (one arrow), then current
  vector (three arrows) from its end → EP (a triangle symbol).
- Tidal stream: from a tidal diamond/atlas for each hour, scaled by spring/neap range.

## 4. Course to steer (CTS)
Problem: you want a **ground track** from A to B; current sets you off.
1. Draw A→B (ground track, two arrows), extended.
2. From A, draw the current vector for 1 hour (set and drift) → point C.
3. With dividers set to your boat speed (1 hour of distance), from C swing an arc to cut
   the ground track → point D.
4. **C→D is the water track to steer**; A→D length = speed over ground.
5. Apply leeway (steer up into the wind by the leeway angle), then convert true → compass.
For a multi-hour passage across tides, sum the hourly current vectors at A first
(they may largely cancel) and draw one triangle for the whole leg.

## 5. Checking and resetting
- Whenever you get a fix (GNSS, bearings, celestial), plot it alongside the EP and note
  the difference. Consistent offset → your current or leeway estimate is wrong; adjust.
- Start a new DR from every reliable fix.
- In reduced visibility near danger, plot EPs at short intervals (e.g. every 15–30 min).

## 6. On land and in the air
- Land: DR by **bearing and pace count** (see the map-and-compass skill); "aiming off".
- Air: heading + true airspeed + forecast wind → ground speed and drift via the
  wind triangle (E6B or electronic flight computer); recompute on any wind change.

## Gotchas
- Mixing water track and ground track (or heading and track) in the same plot.
- Applying leeway the wrong way (it is downwind of the heading).
- Variation changes year to year — use the chart's annual change.
- Speed log errors: calibrate over a measured distance or against GNSS in slack water.

## Verify
- [ ] Log kept with times, headings, speeds and reference (C/M/T).
- [ ] EP includes leeway and set/drift for the same time interval.
- [ ] CTS triangle drawn with matching time units; compass course converted correctly.
- [ ] DR/EP compared with each fix and current/leeway estimates updated.

*Uncertainty:* leeway and current estimates are judgement calls; refine them against every fix.
