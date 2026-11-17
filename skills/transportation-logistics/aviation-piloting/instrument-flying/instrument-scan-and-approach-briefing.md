---
id: transportation-logistics.aviation-piloting.instrument-flying.instrument-scan-and-approach-briefing
name: instrument-scan-and-approach-briefing
category: transportation-logistics
field: aviation-piloting
product: instrument-flying
tags: [aviation-piloting, instrument-flying, ifr, imc, instrument-rating, instrument-scan, radial-scan, selected-radial-cross-check, attitude-indicator, control-and-performance, primary-and-supporting, approach-briefing, ils, localizer, rnav-approach, rnp, lpv, lnav-vnav, vor-approach, non-precision-approach, cdfa, decision-altitude, mda, minima, missed-approach, holding, hold-entry, partial-panel, spatial-disorientation]
level: practitioner
status: gated
description: "Fly by instruments: the attitude-centred radial scan, control-and-performance, a structured approach briefing, flying ILS and RNAV/non-precision approaches, holds and partial panel."
sources: ["https://www.faa.gov/air_traffic/publications/atpubs/aim_html/chap5_section_3.html", "https://www.faa.gov/regulations_policies/handbooks_manuals/aviation/instrument_flying_handbook"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Instrument scan and approach briefing

**Goal:** fly accurately with no outside reference, arrive at minima stable and on
the procedure, and know — before you start down — exactly what you'll do at minimums.

> Draft: general IFR training practice (FAA Instrument Flying Handbook / EASA IR-style).
> Approach design, minima and hold-entry rules vary slightly by State (ICAO PANS-OPS vs
> FAA TERPS). Your charts and the AIP are authoritative.

## 1. The scan
- **Attitude indicator at the centre** (control instrument): set an attitude, then check
  the performance instruments, then return to the AI. The "radial" or hub-and-spoke scan.
- **Control and performance**: attitude + power produce performance. E.g. a light
  piston single (gated: unconfirmed, source is paywalled or blocked): ~2,300 RPM and +5° pitch for a 500 fpm climb at Vy; descent at 90 kt
  with ~1,800 RPM and −3° (calibrate for your aircraft — write your own table).
- Fixation (staring at one gauge), omission (forgetting one) and emphasis
  (over-trusting one) are the three classic scan errors.
- Trim relentlessly: an out-of-trim airplane steals scan time.

## 2. Approach briefing (before the IAF)
Brief from the chart, top to bottom, in the same order every time:
1. Procedure name, **chart date**, runway.
2. **Frequencies**: localiser/VOR, its identifier (identify it — Morse or display), approach
   and tower.
3. **Final approach course** and **FAF** altitude/fix.
4. **Minimums**: DA (precision/LPV/LNAV-VNAV) or MDA (non-precision); visibility required;
   set the minimums bug.
5. **Missed approach**: the first action words (e.g. "climb straight ahead to 2,000,
   then left turn direct VOR, hold").
6. Airport: elevation, runway length, lighting, MSA.
7. Threats: terrain, weather, fatigue, unfamiliar procedure.

## 3. Flying the approach
- **Stabilised approach** criteria (common (gated: unconfirmed, source is paywalled or blocked)): by 1,000 ft above the runway (500 ft in
  VMC for many operators): on course and glidepath, configured, speed and sink rate
  within limits. Not stable → go around.
- **ILS/LPV**: keep localiser and glideslope deflections within about one dot; small
  heading corrections (2–5°) once established.
- **Non-precision (LNAV, VOR)**: fly a **continuous descent final approach (CDFA)** on a
  constant angle (e.g. 3°: rough vertical speed ≈ groundspeed × 5 fpm), treating the MDA
  like a DA with an addition if your operator requires. Avoid "dive and drive".
- At **DA/MDA**: required visual references in sight → land; otherwise **missed approach
  immediately** — say "go around", pitch, power, clean up, fly the briefed missed.

## 4. Holding
- Standard hold (gated: unconfirmed, source is paywalled or blocked): **right turns**, 1-minute inbound legs at or below 14,000 ft (FAA; ICAO
  similar), timing adjusted for wind to achieve the inbound time.
- Entries by sector relative to the inbound course: **direct**, **teardrop** (offset 30°),
  **parallel** — with ±5° flexibility in the boundary.
- Wind correction: triple the inbound drift correction on the outbound leg (rule of thumb).

## 5. Partial panel and disorientation
- Loss of the attitude indicator: cover it (it lies). Use turn coordinator for bank,
  ASI/altimeter/VSI for pitch; make standard-rate turns by timing (3°/s).
- Spatial disorientation (the "leans", somatogravic illusion on go-around acceleration):
  **believe the instruments**, keep head movements minimal, use the autopilot if available.

## Gotchas
- Not identifying the navaid — a localiser under test can show valid needles.
- Wrong altimeter setting is a silent killer on non-precision approaches; cross-check
  with ATC and the other altimeter.
- Cold-temperature corrections may be required at some airports.
- "Just a bit lower" at MDA: the source of many CFIT accidents.

## Verify
- [ ] Your scan returns to the attitude indicator between every other instrument.
- [ ] The briefing covered frequencies/ident, FAF, minimums and missed approach.
- [ ] You were stable by the gate or went around.
- [ ] Non-precision approaches flown as CDFA with a computed descent rate.
- [ ] You can fly a hold entry and a partial-panel approach to standard.

## Checked

Jurisdiction: US FAA with ICAO notes. Checked 2026-10-25: the 3 degree glide path rule of thumb (vertical speed about groundspeed in knots x 5 fpm) holds by arithmetic (about 5.3 x groundspeed). FAA AIM and the Instrument Flying Handbook returned 403 to the fetch tool, so the hold standard, stabilised approach gates and the aircraft power and pitch figures are marked gated; the skill already tells the pilot to calibrate figures for the aircraft.

Method: documentation only; no commands were run.
