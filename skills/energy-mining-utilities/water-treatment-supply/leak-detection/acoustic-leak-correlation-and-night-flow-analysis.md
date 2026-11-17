---
id: energy-mining-utilities.water-treatment-supply.leak-detection.acoustic-leak-correlation-and-night-flow-analysis
name: acoustic-leak-correlation-and-night-flow-analysis
category: energy-mining-utilities
field: water-treatment-supply
product: leak-detection
tags: [water-treatment-supply, leak-detection, leak-correlator, acoustic-correlation, listening-stick, ground-microphone, geophone, noise-logger, minimum-night-flow, mnf, step-test, dma, district-metered-area, non-revenue-water, nrw, water-loss, pipe-velocity, sound-velocity, plastic-pipe-leak, hydrophone, leakage-technician, pinpointing]
level: practitioner
status: draft
description: "Find hidden water leaks: read minimum night flow in a DMA, step test to narrow it, sound with a listening stick and pinpoint with an acoustic correlator."
sources:
  - "IWA Water Loss Specialist Group / AWWA M36 (Water Audits and Loss Control Programs) concepts, paraphrased"
  - "Correlator manufacturers' operating guidance, general principles paraphrased"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Acoustic leak correlation and night flow analysis

**Goal:** go from "this area is losing water" to "dig here" with the fewest wasted holes.

## 1. Is there a leak? — Minimum night flow (MNF)
In a district metered area (DMA), flow between ~02:00 and 04:00 is mostly leakage plus a
small legitimate night use.
- Take the minimum (or average of the lowest hour) from the inlet meter logger.
- Subtract an allowance for legitimate night use (household and known non-household night
  users — use your utility's per-property figure).
- What's left, compared to the DMA's normal baseline, is the leak signal. A step up that
  stays is a new burst; a slow creep is background leakage.
- Check meters and boundary valves first — an open boundary valve looks exactly like a leak.

## 2. Where in the DMA? — Step test
At night, with the inlet logger running, close valves in sequence from the far end back
toward the meter, a few minutes per step. A drop in inlet flow when a section is shut
means the leak is in that section. Re-open everything in reverse and confirm all valves
are back. (Pressure-sensitive customers and fire supply must be considered; many utilities
now use noise-logger lift-and-shift instead.)

## 3. Survey — listen
- **Listening stick / ground mic** on every fitting (valves, hydrants, meters) in the
  suspect section. Leak noise is a steady hiss/roar that does not change with time; traffic
  and pumps vary.
- **Noise loggers** left overnight on fittings flag consistent noise; loggers with
  correlation capability narrow it further.
- Metal pipe carries sound well (hundreds of metres between contact points); plastic
  pipe attenuates quickly — contact points need to be much closer, or use hydrophones.

## 4. Pinpoint — correlate
1. Put two sensors on fittings either side of the suspected leak, on the same pipe.
2. Enter the distance between sensors **as measured along the pipe** (wheel it, include
   bends), pipe material and diameter — the correlator uses these to pick sound velocity.
3. The correlator computes the time delay between the two signals; leak position =
   (D − v·Δt)/2 from the nearer sensor.
4. Run with different filter bands; a genuine leak gives a sharp, repeatable peak.
5. Confirm on the surface with a ground mic directly over the predicted position — the
   sound should be loudest there.

## 5. Before you dig
Mark the spot, check for other noises (PRVs, customer usage, a running toilet in a nearby
property), and confirm services. Record the find and, after repair, re-check MNF to
confirm the saving.

## Gotchas
- Wrong pipe material or distance in the correlator moves the result by metres; mixed
  materials need the segment velocity entered per section.
- A leak at a fitting or a bend can reflect sound and create a false second peak.
- Correlating across a tee: the leak may be on the branch.
- High pressure makes leaks louder — survey at night at full pressure.
- Plastic mains: low-frequency noise; set filters lower and expect weak peaks.

## Verify
- [ ] MNF baseline compared after removing legitimate night use; boundary valves checked.
- [ ] Step-test valves all reopened and logged.
- [ ] Correlation peak repeatable with correct along-pipe distance and material.
- [ ] Ground mic confirms the loudest point before excavation.
- [ ] MNF drops after repair by roughly the estimated leak flow.

*Uncertain:* night-use allowances and sound velocities are utility/manufacturer specific;
use your correlator's tables.
