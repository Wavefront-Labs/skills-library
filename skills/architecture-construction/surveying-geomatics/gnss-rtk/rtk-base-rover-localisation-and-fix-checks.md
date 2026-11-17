---
id: architecture-construction.surveying-geomatics.gnss-rtk.rtk-base-rover-localisation-and-fix-checks
name: rtk-base-rover-localisation-and-fix-checks
category: architecture-construction
field: surveying-geomatics
product: gnss-rtk
tags: [gnss-rtk, gnss, gps, rtk, network-rtk, vrs, ntrip, base-rover, site-calibration, localisation, localization, geoid, datum, projection, fixed-solution, float-solution, pdop, multipath, check-shot, survey-controller, trimble-access, leica-captivate, emlid, geomatics, surveying]
level: practitioner
status: draft
description: "RTK GNSS survey: base or network setup, site localisation to local control, fixed vs float judgement, and the check-in/out routine that proves positions before you trust them."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# GNSS / RTK — base-rover, localisation and fix quality

**Goal:** produce centimetre-level positions that agree with the project's coordinate
system and heights, and know when the receiver is lying to you.

## 1. Choose the correction source
- **Own base:** set the base over a known mark (or on an autonomous position, then
  translated later), measure antenna height to the correct reference point (ARP vs
  slant to the bumper — the controller must know which). Radio range is typically a few
  km and line-of-sight dependent.
- **Network RTK (NTRIP / VRS):** login to a CORS network via mobile data; no base to
  guard. Check which datum/realisation the network broadcasts (e.g. a national ITRF/ETRF
  realisation) — it must match your project or be transformed.
- Rule of thumb: horizontal precision degrades by roughly 1 mm per km of baseline on
  top of ~8–10 mm; vertical is about twice as bad. Long baselines = poorer heights.

## 2. Coordinate system: projection, datum, geoid
Set the job with: datum, map projection/zone, and **geoid model** for orthometric
heights. GNSS gives ellipsoidal heights; without the right geoid model your levels can
be metres out. Most site errors of "the GPS is 30 m off" are the wrong zone or datum,
not the receiver.

## 3. Site localisation (calibration)
When the site uses a local grid or local control:
1. Observe **at least 3, preferably 4+ control points** surrounding the work area (never
   extrapolate far outside the hull of the points).
2. Compute the localisation: horizontal (translation, rotation, scale) and vertical
   (inclined plane/shift).
3. Read the **residuals** for each point. Rule of thumb: horizontal residuals of a
   couple of centimetres or less; one point with a large residual is usually a disturbed
   mark or a wrong coordinate — remove it and re-check, don't just accept the fit.
4. Check the **scale factor** the fit produced. A scale far from 1 (beyond a few
   tens of ppm, unless the local grid is a deliberate ground grid) suggests a bad point.
5. Save the localisation into the job and record which points were used.

## 4. Fixed vs float — trusting a position
- Store only on a **fixed** (integer-ambiguity) solution. Float is decimetre-class.
- Watch the precision estimates (HRMS/VRMS or CQ), satellite count and PDOP. Typical
  acceptance: PDOP below about 3–4, a healthy multi-constellation count.
- A fix can be **wrong** ("bad fix"), especially near buildings, trees and fences.
  Defences: occupy for multiple epochs (e.g. 5–30 s), re-initialise and re-observe
  important points, and observe them again at a different time of day (different
  satellite geometry).

## 5. The check-in / check-out routine
- **Start of day:** observe a known control point, compare against its coordinates
  before measuring anything else. Record the delta.
- **After any base move, radio dropout, or re-initialisation:** check in again.
- **End of day:** check out on the same or another known point.
If check-in fails, stop: wrong localisation, wrong antenna height, or base on the wrong mark.

## Gotchas
- Multipath from walls, vehicles and glass gives confident-looking but wrong fixes.
- Rover pole height: verify the pole is at the height you entered (telescopic poles slip).
- RTK under canopy or in urban canyons may never fix properly — use a total station from
  GNSS-established control instead.
- Heights for drainage and floor levels: GNSS vertical precision may not meet the spec;
  use levelling (see digital-level skill) where millimetres matter.
- Leap-second, firmware and geoid-file versions differ between controllers; keep them
  consistent across crews on a job.

## Verify
- [ ] Datum, projection/zone and geoid model set and recorded in the job.
- [ ] Localisation residuals reviewed; scale sensible; points used are logged.
- [ ] Check-in at start and check-out at end both within tolerance.
- [ ] Critical points observed twice with independent initialisations.
- [ ] Only fixed solutions stored.

*Uncertainty:* the precision figures are typical manufacturer-spec-sheet ranges and
vary by receiver and network; confirm against your equipment's specification.
