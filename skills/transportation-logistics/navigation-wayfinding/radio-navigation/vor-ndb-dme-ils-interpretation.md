---
id: transportation-logistics.navigation-wayfinding.radio-navigation.vor-ndb-dme-ils-interpretation
name: vor-ndb-dme-ils-interpretation
category: transportation-logistics
field: navigation-wayfinding
product: radio-navigation
tags: [radio-navigation, radio-navigation-aids, navaids, vor, vor-dme, ndb, adf, dme, ils, localizer, glideslope, cdi, hsi, obs, radial, to-from-flag, reverse-sensing, rmi, morse-ident, dme-arc, cross-radial-fix, slant-range, navigation-wayfinding, ifr, instrument-flying, aviation-navigation, conventional-navigation]
level: practitioner
status: draft
description: "Use ground-based aviation navaids: identify, set OBS and track VOR radials, read TO/FROM, home or track with NDB/ADF, fly DME arcs, cross-fix position, and interpret ILS localizer and glideslope."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# VOR, NDB, DME and ILS interpretation — conventional radio navigation

**Goal:** determine position and track courses using VOR, NDB, DME and ILS, as a
backup to GNSS and for conventional procedures. This is instrument-flying knowledge;
practise under instruction and in a simulator before using it in IMC.

## 1. Always identify the station
Tune the frequency and **listen to the Morse ident** (and check the published ident on
the chart). No ident, or a test signal (TST), → don't use it. Many receivers now
decode the ident on screen; still confirm. Check NOTAMs for outages.

## 2. VOR
- A VOR gives **radials** — magnetic bearings **from** the station (360 of them).
- Set the **OBS** (course selector) to a course; the **CDI** needle shows whether you're
  left or right of that course line; **TO/FROM flag** shows whether that course takes
  you toward or away from the station.
- To find which radial you're on: rotate OBS until needle centres with **FROM** flag —
  that's your radial.
- **Tracking inbound:** set OBS to the inbound course (radial + 180°), TO flag; steer
  toward the needle with small corrections (e.g. 10–20° intercept, then a wind-correction
  angle that keeps it centred).
- Full-scale CDI deflection ≈ 10° off course (each dot ≈ 2° on a 5-dot display).
- **Reverse sensing:** with a conventional CDI, if the OBS is set to the reciprocal of
  your heading direction, the needle reads backwards. Keep the OBS roughly matching
  your heading. An HSI eliminates this when set correctly.
- Cone of confusion over the station: flag flickers; hold heading until it settles.
- Accuracy roughly ±1–2° of radial — at 60 nm that's 1–2 nm.

## 3. NDB / ADF
- The ADF needle points **to** the NDB. **Magnetic bearing to station = magnetic
  heading + relative bearing** (from a fixed-card ADF). An RMI does the sum for you.
- **Homing** (keep needle on the nose) drifts you in a curve in wind — instead **track**:
  intercept the bearing and hold a wind-correction angle so the bearing stays constant.
- Errors: night effect, thunderstorms (needle points to lightning), coastal refraction,
  mountain effect. Treat NDB as less accurate (±5° or worse).

## 4. DME
- Gives **slant range** (nm) to the station — at altitude directly over the station it
  reads your height in nm. Slant-range error is small when distance is > ~3× altitude
  (in thousands of ft vs nm, roughly).
- Groundspeed readouts are only meaningful flying directly to/from the station.
- **DME arc:** fly a constant distance; turn ~90° to the radial at the lead point,
  then keep the RMI/bearing pointer near the wingtip, turning 10–20° inward each time the
  DME increases slightly. Published lead radials tell you when to turn inbound.

## 5. Cross-fixing position
- Two VOR radials crossing (ideally 60–120° apart) → fix; or VOR radial + DME distance
  (single station, best).
- Plot on the chart or set as a waypoint check against GNSS.

## 6. ILS
- **Localizer** (VHF, 108.10–111.95 MHz, odd tenths): lateral guidance; full-scale
  deflection ≈ 2.5° either side (four times more sensitive than a VOR).
  CDI course setting doesn't affect the needle on a conventional indicator — but set it
  to the inbound course anyway (it matters for an HSI and back-course).
- **Glideslope** (UHF, paired): vertical guidance, typically 3°; full-scale ≈ ±0.7°.
- Fly needles centred with small corrections; descent rate ≈ groundspeed (kt) × 5 for
  a 3° slope (ft/min).
- Back-course: reverse sensing on a CDI unless HSI set to the front course.
- Marker beacons or DME/fixes confirm glideslope altitude checks — check the altimeter
  at the published fix (false glideslope captures exist above the true slope).

## Gotchas
- Wrong frequency because ident wasn't checked.
- Reverse sensing on VOR/back-course with a CDI.
- ADF homing mistaken for tracking in a crosswind.
- Capturing a false glideslope from above.

## Verify
- [ ] Every navaid identified by Morse before use.
- [ ] Can state current radial, DME and position from cross-fix.
- [ ] Tracking holds course within a dot with wind correction.
- [ ] ILS glideslope altitude cross-checked at the final approach fix.

*Uncertainty:* sensitivity and accuracy figures are typical; certification standards and aircraft equipment differ — follow your aircraft's AFM and the current AIP.
