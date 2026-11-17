---
id: transportation-logistics.air-traffic-control.surveillance-systems.radar-display-and-degradation-handling
name: radar-display-and-degradation-handling
category: transportation-logistics
field: air-traffic-control
product: surveillance-systems
tags: [air-traffic-control, atc, surveillance-systems, radar, ads-b, mlat, ssr, psr, data-block, track-label, electronic-flight-strips, efs, stars, eram, itec, topsky, console-setup, range-rings, filters, radar-failure, surveillance-degradation, coast-track, transponder, mode-c, mode-s, squawk, controller-workstation]
level: practitioner
status: draft
description: "Set up an ATC surveillance console (range, filters, data blocks, strips), keep the picture clean, and fall back safely when radar, ADS-B or labels degrade."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Radar display management and degradation handling

**Goal:** a picture you can trust at a glance — every target you own is labelled
correctly, nothing irrelevant clutters it — and a rehearsed response for when the
surveillance chain lets you down.

> Draft: written from general ATC practice across systems (STARS/ERAM in the US,
> iTEC/TopSky/Thales and similar in Europe). Exact menus, keystrokes and minima are
> unit- and system-specific; your unit's manual of operations (MATS/7110.65/local
> orders) overrides everything here.

## 1. Console setup at position takeover
Do it before you plug in, not while traffic builds:
1. **Range and centre** — the whole sector plus ~10–20 NM of the neighbours you hand
   to/from. Too tight and inbound traffic appears late; too wide and labels overlap.
2. **Altitude filter** — your sector's vertical limits plus a buffer (e.g. 1,000–2,000 ft)
   so you see climbers/descenders about to enter. Never filter out VFR primary-only
   targets near your airspace boundary.
3. **Maps** — sector boundary, airways/fixes, MVA/MSA map (minimum vectoring altitude)
   always on when vectoring; restricted/danger areas active today.
4. **Brightness** — maps dim, targets and labels bright, history trails short (3–5).
5. **Leader lines and label offset** — set default direction away from your busiest flow.
6. **Check the system status window**: which radar heads/ADS-B/MLAT sources are feeding,
   any NOTAM'd outages, and whether you are on the main or fallback tracker.

## 2. Data-block housekeeping
A data block (label) is only as good as its last update. Keep it honest:
- **Cleared level / assigned altitude** entered the moment you issue it — the label is
  your memory and your relief's briefing.
- **Mode C/S readout vs assigned**: a difference over ~200–300 ft (local tolerance) needs
  a "confirm level" check; the pilot's report wins until resolved.
- **Squawk check** at first contact: verify the code matches the flight plan; a
  duplicate code mis-correlates two tracks.
- **Hand off / accept promptly** so ownership symbols match reality.
- **Drop or suppress** labels for aircraft long gone; leave limited blocks for VFR.
- On EFS, the strip state (pending/active/transferred) must mirror the label. A
  strip parked in the wrong bay is how aircraft get forgotten.

## 3. Recognising degradation early
| Symptom | Likely cause | First move |
|---|---|---|
| Target "coasting" symbol, position frozen | Track lost, tracker predicting | Ask position/level; don't separate off a coast track |
| Label jumps between two targets | Duplicate squawk / mis-correlation | Assign a new code, re-identify |
| Primary-only blip, no label | Transponder off or failed | Identify by turn or position report |
| Whole sector stale / timestamp alarm | Radar head or feed failure | Declare to supervisor, start fallback |
| Mode C reads garbage | Encoder fault | Request pilot level reports, inhibit readout |

## 4. Fallback: surveillance failure
1. **Say it out loud** to the supervisor and adjacent sectors.
2. **Freeze the picture mentally**: last known positions, levels, headings.
3. **Establish vertical separation first** — it needs no radar. Assign different levels
   to anything converging, using the standard procedural vertical minimum (typically
   1,000 ft below FL290 / RVSM).
4. Broadcast to all aircraft if needed: "Radar service terminated" (or local
   phraseology), request position reports over fixes.
5. **Stop new traffic**: flow-control inbound via the supervisor/flow position.
6. Transition to procedural separation (see the oceanic-procedural-control skill
   `transportation-logistics.air-traffic-control.oceanic-procedural-control.procedural-separation-and-position-reports`).
7. On recovery, re-identify every aircraft before resuming radar separation.

## 5. Gotchas
- ADS-B positions come from the aircraft's own GNSS: a spoofed or jammed receiver shows a
  confident, wrong position. Cross-check with radar/MLAT where available.
- Filters you set hide things from you, not from the sky. Reset them at takeover.
- Relief briefings must cover non-default console settings you changed.
- Label overlap in a hold stack: separate them by leader direction, not by ignoring them.

## Verify
- [ ] At takeover you checked sources, filters, maps and MVA display.
- [ ] Every owned label shows the cleared level you actually issued.
- [ ] You can name the first three actions for a total surveillance failure.
- [ ] Duplicate squawks and Mode C discrepancies are resolved, not tolerated.
- [ ] After recovery, every track was re-identified before radar separation resumed.
