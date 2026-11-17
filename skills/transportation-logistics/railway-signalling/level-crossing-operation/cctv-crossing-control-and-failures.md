---
id: transportation-logistics.railway-signalling.level-crossing-operation.cctv-crossing-control-and-failures
name: cctv-crossing-control-and-failures
category: transportation-logistics
field: railway-signalling
product: level-crossing-operation
tags: [level-crossing-operation, level-crossing, grade-crossing, railroad-crossing, barriers, gates, mcb, manually-controlled-barriers, cctv-crossing, mcb-cctv, crossing-keeper, barrier-sequence, crossing-clear, obstruction-detection, od, obstacle-detection, crossing-failure, barrier-failure, local-control, crossing-attendant, road-traffic, pedestrians, vehicle-trapped, misuse, near-miss]
level: practitioner
status: draft
description: "Operate and monitor a level crossing from a box or control centre: lower barriers in the right sequence, confirm the crossing clear on CCTV, respond to obstructions, and work failed crossings."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# CCTV crossing control and failures

**Goal:** close the road, prove the crossing is clear of people and vehicles, and only
then let a train approach — and know exactly what to do when barriers or detection
fail.

*Draft: modelled on manually controlled barrier crossings with CCTV (common in the
UK) plus generic failure principles. Crossing types, timings and failure rules vary
by country — follow your instructions.*

## 1. The sequence
1. **Time it:** lower early enough that the crossing is proved clear before the
   train reaches the signal protecting it — but not so early that road users wait
   needlessly (long waits increase misuse). Learn the strike-in point for each
   train type.
2. Press **lower**: road lights flash amber then red, entrance barriers lower first,
   exit barriers after a delay (so vehicles aren't trapped).
3. **Crossing clear check:** on the CCTV monitor, look along the whole crossing —
   both carriageways, footways, the area between barriers, the track itself. Look
   for: pedestrians walking between barriers, cyclists, a car stopped on the tracks,
   animals, objects.
4. Only when satisfied, press **crossing clear** (or equivalent) — this allows the
   protecting signal to clear.
5. After the train passes and the track is clear, **raise** the barriers. Check for a
   second train before raising.

## 2. Obstruction response
- Something on the crossing after you've proven it clear and the signal is off:
  **put the protecting signal back to danger** if the train can still stop at it,
  and use emergency procedures (railway emergency call / radio to driver) if the
  train is already past it.
- Vehicle trapped between barriers: do not raise and lower in a hurry; stop the
  train first, then raise to let the vehicle out.
- Obstacle-detection crossings (radar/lidar): if detection reports an obstruction,
  trust it until the crossing is verified clear.

## 3. Failure working
| Failure | Typical response (check rules) |
|---|---|
| Barrier won't lower | Stop trains at the protecting signal; arrange crossing attendant/police |
| CCTV lost | Don't prove clear on a blank screen; caution trains, attendant on site |
| Barriers stuck down | Inform road authorities/police; prioritise reopening |
| Lights failure | Treat as unprotected; trains caution over at low speed |

When a crossing is under local control or attended by staff, give the attendant
clear instructions and confirm each train movement with them.

## 4. Misuse and records
- Log near-misses and misuse (drivers zig-zagging, pedestrians ducking barriers) with
  time and CCTV reference so it can be reviewed.
- Repeated misuse at one crossing is a design/timing signal, not just bad behaviour.

## Gotchas
- Glare, rain, darkness and camera dirt can hide a pedestrian — zoom/switch views when
  unsure.
- "The road was empty a second ago" — check again immediately before crossing clear.
- Raising barriers while a second train is approaching on the other line.

## Verify
- [ ] Barriers lowered at the correct strike-in point for each train.
- [ ] Crossing clear confirmed by deliberate full-area CCTV scan every time.
- [ ] No barrier raised with another train approaching.
- [ ] Failures and misuse logged with times and actions.
