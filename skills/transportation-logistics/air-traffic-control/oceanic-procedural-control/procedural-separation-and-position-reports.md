---
id: transportation-logistics.air-traffic-control.oceanic-procedural-control.procedural-separation-and-position-reports
name: procedural-separation-and-position-reports
category: transportation-logistics
field: air-traffic-control
product: oceanic-procedural-control
tags: [air-traffic-control, atc, oceanic-procedural-control, oceanic-control, procedural-control, non-radar, procedural-separation, longitudinal-separation, lateral-separation, vertical-separation, position-report, time-estimate, mach-number-technique, nat, north-atlantic-tracks, nat-ots, oceanic-clearance, cpdlc, ads-c, fans, pbcs, hf-radio, selcal, flight-progress-strips, slop]
level: advanced
status: draft
description: "Separate aircraft without surveillance: time and distance longitudinal standards, lateral and vertical separation, processing position reports, and oceanic clearances."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Procedural separation and position reports

**Goal:** keep aircraft apart using only clearances, reports and arithmetic — and
detect when the arithmetic no longer matches the aircraft.

> Draft: standards illustrated here (e.g. 10-minute longitudinal with Mach number
> technique, 1,000 ft vertical) are common ICAO/regional figures but vary with
> region, equipment (PBCS, ADS-C, CPDLC) and aircraft approvals. Use ICAO Doc 4444,
> regional supplementary procedures (Doc 7030) and your unit orders.

## 1. The three dimensions
1. **Vertical** — the simplest and most robust: different flight levels (1,000 ft in
   RVSM airspace, 2,000 ft otherwise or for non-RVSM aircraft).
2. **Lateral** — different tracks separated by a minimum distance or by protected
   airspace (e.g. tracks spaced at 1° of latitude, or reduced lateral standards for
   suitably equipped aircraft).
3. **Longitudinal** — same track, same level: separation in **time** (e.g. 15 min
   basic; 10 min with Mach number technique where the following aircraft is the
   same or slower Mach) or **distance** via ADS-C/RNP standards.
You only need one dimension at any moment — but you must always have one, including
during level changes.

## 2. Processing a position report
Standard content: callsign, position, time, level, next position + estimate,
following position.
1. **Compare actual time with the previous estimate.** Revise when the difference
   exceeds the threshold your region uses (often 2–3 minutes).
2. Recompute the **time interval to the aircraft ahead and behind** at the next
   common point. If it is shrinking toward the minimum, act now (Mach change or
   level change), not at the next report.
3. Update the strip or flight data system immediately; a stale estimate is how
   procedural losses happen.
4. **Missed report**: start communications search (SELCAL, other frequency,
   relay via another aircraft, ADS-C demand contract) and protect the airspace for
   the aircraft's possible positions.

## 3. Level changes procedurally
- A climb or descent through another aircraft's level needs separation from it
  during the transition: e.g. "climb to FL360, to be level by 50N030W" or
  "climb after passing 30W". Make the restriction checkable from a report.
- Consider ADS-C/CPDLC-based reduced-separation climbs only where the regional
  rules and aircraft approvals allow (this skill does not cover the exact criteria).

## 4. Oceanic clearances (NAT-style example)
- Clearance contains entry point and time, track or random route, flight level and
  **Mach number**.
- Check the requested entry time against other aircraft on the same track/level:
  if two are within the longitudinal minimum, offer the next level, a different
  track or a later entry time.
- Many regions now issue clearances by datalink; confirm the crew has loaded and
  accepted the route — reroutes are a well-known source of waypoint insertion errors.

## 5. Contingencies
- Pilots may fly a **strategic lateral offset** (SLOP) of 1 or 2 NM right of
  centreline — expected, not a deviation.
- Weather deviations and in-flight contingencies (e.g. an aircraft unable to maintain
  level) follow published offset-and-level procedures; know them for your region.
- HF propagation fades: use CPDLC, relay, or SATVOICE as allowed.

## Gotchas
- Mach technique only holds when the following aircraft is not faster; check the
  assigned Machs, not the filed ones.
- Time estimates from the crew are on their clock; time checks matter.
- An unreported position with an unchanged estimate is not "probably fine".

## Verify
- [ ] Every pair of aircraft has at least one standard applied at every moment.
- [ ] Each report was compared with its estimate and revisions applied.
- [ ] Level changes carry a restriction that keeps separation through the transition.
- [ ] Oceanic clearances checked entry time, track, level and Mach against others.
- [ ] Missed reports triggered a comms search within your local time limit.
