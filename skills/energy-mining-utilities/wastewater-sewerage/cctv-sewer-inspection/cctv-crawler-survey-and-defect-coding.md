---
id: energy-mining-utilities.wastewater-sewerage.cctv-sewer-inspection.cctv-crawler-survey-and-defect-coding
name: cctv-crawler-survey-and-defect-coding
category: energy-mining-utilities
field: wastewater-sewerage
product: cctv-sewer-inspection
tags: [wastewater-sewerage, cctv-sewer-inspection, cctv, sewer-survey, drain-survey, crawler-camera, push-camera, pan-and-tilt, pipe-inspection, defect-coding, mscc, mscc5, pacp, nassco, en-13508-2, condition-grading, structural-defect, service-defect, chainage, cable-counter, ovality, laser-profiling, sonar, root-intrusion, joint-displacement, crack, fracture, deformation, infiltration, inspection-report, wincan, posm, itpipes]
level: practitioner
status: draft
description: "Run a CCTV sewer survey with a crawler or push camera: set-up, chainage, pan-and-tilt at defects, coding to MSCC/PACP-style schemes and a report engineers can use."
sources:
  - "WRc Manual of Sewer Condition Classification (MSCC5) and EN 13508-2, concepts paraphrased"
  - "NASSCO PACP reference manual concepts, paraphrased"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# CCTV crawler survey and defect coding

**Goal:** produce a survey that someone who never saw the pipe can use to decide repair,
rehab or leave alone — accurate distances, clear footage and consistent codes.

## 1. Before you drop the camera
1. Confirm which coding standard the client wants (MSCC5/EN 13508-2 in UK/Europe, PACP in
   North America, a national variant elsewhere). Codes and grading differ.
2. Get pipe details: start and finish nodes (manhole IDs), direction, expected
   material/diameter/shape. Note survey direction relative to flow.
3. **Clean first** if the job spec calls for it (jetting) — debris hides defects and
   stops crawlers. Control flow: survey in low-flow hours or plug/over-pump; a camera under
   water sees nothing (sonar or a float system then).
4. Crawler: wheels and camera head suited to diameter; camera centred in the pipe
   (adjust lift). Push camera for small drains (typically ≤ 150–225 mm).
5. Confined-space rules apply at manholes — deploy from the surface wherever possible.

## 2. Distances and set-up
- **Zero the cable counter at the pipe entry** (the joint face where the pipe leaves the
  start manhole), not at the cable drum or chamber floor.
- Record header info: date, operator, weather, pre-cleaned yes/no, nodes, direction,
  material, size, use (foul/storm/combined).

## 3. Driving the survey
- Travel steadily (commonly ≤ ~0.1–0.2 m/s) with the camera looking ahead; keep lighting
  even, lens clean (wipe/air if fogging).
- **Stop at every defect, junction and joint of interest**: pan around the full
  circumference, tilt to look into connections, then return to forward view.
- Pressing on into a collapse or heavy roots risks losing the crawler; abandon the
  run and survey from the other end (reverse set-up, note it).

## 4. Coding defects
Every observation gets: distance, code, clock position(s), and a quantity (percentage
cross-section loss, length, joint gap in mm, etc.).
Typical families (names vary by scheme):
- **Structural:** cracks, fractures, broken, hole, deformation (% of diameter), joint
  displaced (radially, longitudinally), collapse.
- **Service/operational:** roots (fine/mass), encrustation, debris, fat/grease, infiltration
  (seeping/dripping/running/gushing), obstruction, water level.
- **Construction features:** junctions, connections (with clock and diameter), material
  change, line deviation.
- **Continuous defects** get a start and finish distance — not repeated point codes.
Use the scheme's grade rules (e.g. 1–5) as calculated by software; don't hand-grade.

## 5. Reporting
Software (e.g. WinCan, POSM, ITpipes or equivalents) produces the standard report and
exchange file. Check before sending: header complete, all defects have stills, distances
add up to the measured manhole-to-manhole length, abandoned surveys explained.
Flag **urgent** findings (collapse, voids visible behind pipe, large infiltration under
roads) to the client immediately, not in the next weekly report.

## Gotchas
- Cable stretch and wheel slip make long runs over-read; check against measured length.
- Water level hides invert defects; record water level as an observation.
- Calling a lateral "defective connection" vs "connection" changes rehab cost — be exact.
- Unrecorded clock positions make cutter robots and patch repairs guess.

## Verify
- [ ] Counter zeroed at pipe entry; final distance matches measured length.
- [ ] Every defect has code, distance, clock reference, quantity and a still.
- [ ] Continuous defects coded with start/finish, not repeated.
- [ ] Correct coding standard used; report exported in client format.
- [ ] Urgent defects escalated the same day.

*Uncertain:* exact code letters and grading thresholds depend on the scheme version; use the
current manual for the scheme you're contracted to.
