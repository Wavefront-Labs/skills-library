---
id: manufacturing-production.production-line-operations.standard-work.writing-takt-paced-standard-work-with-5s-and-andon
name: writing-takt-paced-standard-work-with-5s-and-andon
category: manufacturing-production
field: production-line-operations
product: standard-work
tags: [standard-work, production-line-operations, takt-time, cycle-time, standard-work-combination-sheet, swcs, standard-wip, work-sequence, job-element-sheet, 5s, sort-set-in-order-shine-standardise-sustain, 5s-audit, visual-management, visual-controls, shadow-board, floor-marking, andon, andon-cord, escalation, toyota-production-system, tps, lean]
level: practitioner
status: draft
description: "Write standard work that actually runs: compute takt, time the elements, build a combination sheet, set standard WIP, back it with 5S and visual controls, and define andon response times."
sources: ["Liker, J. The Toyota Way (2004)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Writing takt-paced standard work with 5S and andon

**Goal:** a station where any trained operator does the same steps, in the same order,
in the same time, with abnormalities visible at a glance and help arriving fast.
Standard work is the baseline that improvement is measured against — without it,
kaizen just changes noise.

## 1. Compute takt time
**Takt = available working time ÷ customer demand** for the same period.
Example: 2 shifts × 450 min (after breaks) = 900 min = 54,000 s; demand 1,200 units/day
→ takt 45 s. Takt is a demand rate, not a machine speed. If the actual cycle time of a
station exceeds takt, that station cannot keep up and needs rebalancing
(see engineering-technology.industrial-manufacturing-systems-engineering.work-design-ergonomics.time-study-and-assembly-line-balancing).

## 2. Observe and time the elements
- Break the job into elements (the smallest sensible steps: "pick housing and place in
  fixture"). Time each at least 10 cycles with the operator who does it best *and*
  one who struggles — the gap shows where the method is undefined.
- Record **manual time**, **walk time** and **machine (auto) time** separately.
- Use the **lowest repeatable** time for each element, not the average, and don't
  include out-of-cycle work (fetching a box every 50 parts) — handle that separately.

## 3. Build the three standard-work documents
1. **Standard work combination sheet:** each element with its manual (solid line),
   walk (wavy) and machine (dashed) time, plotted against a red takt line. You see at
   once whether the operator waits on a machine or the cycle overruns takt.
2. **Standard work chart / layout:** station plan showing the walking path, the
   **standard WIP** (the minimum parts that must be in place — in the fixture, in the
   machine — for the sequence to run) and quality/safety check points.
3. **Job element sheets / work instructions:** each element's key points ("seat until
   click"), the reasons why, and photos. Keep text short; photos of good vs bad.
Post them at the station, at eye height, and date/version them.

## 4. Make the station run to it: 5S
- **Sort:** remove everything not needed for this job (red-tag it, decide within a set
  time).
- **Set in order:** a place for everything at point of use, in sequence order, outlined
  (shadow boards, floor tape, labelled bins with min/max).
- **Shine:** clean as inspection — leaks and loose bolts show up on a clean machine.
- **Standardise:** photo of the station "as it should look"; daily checklist.
- **Sustain:** regular **5S audit** with a score, done by someone outside the area,
  results posted. 5S that is not audited decays in weeks.

## 5. Visual management and andon
- Anyone walking by should know in 10 seconds: are we on plan? Hour-by-hour board
  (plan vs actual, reason for any miss), WIP markings that show over/under, status
  lights on machines.
- **Andon:** a cord/button/light the operator uses at the first abnormality (missing
  part, defect, can't make takt). Define the response in writing: e.g. team leader
  arrives within **one takt** or a set time like 60 s, decides fix/continue/stop.
- Calls must be *welcomed*. If pulling andon gets the operator blamed, it stops being
  pulled and problems hide. Track andon calls as improvement input, not a KPI to drive
  down.

## Gotchas
- Standard work written in an office from a drawing never matches the floor.
- Instructions nobody updates after a change become wrong — and then ignored.
- Don't set the standard on your fastest operator's best cycle; it must be sustainable
  for a full shift, including fatigue and ergonomics.

## Verify
- [ ] Takt computed from demand; every station's cycle at or below it.
- [ ] Combination sheet shows manual/walk/machine time against takt.
- [ ] Standard WIP defined and visible.
- [ ] 5S audit scored and trended.
- [ ] Andon response time written down and met.
