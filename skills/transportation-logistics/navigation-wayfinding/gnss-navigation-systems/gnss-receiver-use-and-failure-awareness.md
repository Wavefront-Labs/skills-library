---
id: transportation-logistics.navigation-wayfinding.gnss-navigation-systems.gnss-receiver-use-and-failure-awareness
name: gnss-receiver-use-and-failure-awareness
category: transportation-logistics
field: navigation-wayfinding
product: gnss-navigation-systems
tags: [gnss-navigation-systems, gnss, gps, galileo, glonass, beidou, sbas, waas, egnos, navigation-wayfinding, waypoints, routes, tracks, datum, wgs84, coordinate-format, utm, mgrs, hdop, pdop, accuracy, multipath, jamming, spoofing, interference, raim, handheld-gps, chartplotter, garmin, gpx]
level: practitioner
status: draft
description: "Use a GNSS receiver properly: set datum and coordinate format, build waypoints and routes, read accuracy (HDOP/EPE), and recognise multipath, jamming and spoofing with independent cross-checks."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# GNSS receiver use and failure awareness — trust it, but check it

**Goal:** navigate with GPS/Galileo/GLONASS/BeiDou receivers (handhelds, chartplotters,
phones, aviation/marine units) — set them up so coordinates match your maps, plan
waypoints and routes, and notice quickly when the position is wrong.

## 1. Set-up (do this before you trust any coordinate)
- **Datum / map datum:** most receivers default to WGS84. Paper maps and charts may use
  another datum (e.g. OSGB36, NAD27, ED50); mismatches give offsets from metres to
  hundreds of metres. Match the receiver to the map or apply the chart's datum shift note.
- **Position format:** decimal degrees (51.50123), degrees decimal minutes
  (51°30.074'), degrees-minutes-seconds, UTM/MGRS, or a national grid. Mixing these up
  is the most common data-entry error: 51.30 ≠ 51°30'.
- **Units:** distance (nm/km/mi), heading reference (true vs magnetic — set magnetic if
  you'll compare with a compass, true for charts/ECDIS).
- **Constellations:** enable multi-GNSS for availability; enable SBAS (WAAS/EGNOS/MSAS)
  where supported for better accuracy and integrity.
- Update firmware and maps; check the almanac/first fix at home before a trip.

## 2. Waypoints, routes and tracks
- **Waypoint:** a stored position — name it clearly (`CAMP2`, `JNC-A12`), verify by
  plotting on the map, not just typing.
- **Route:** ordered waypoints you intend to follow; the receiver gives bearing/distance
  to next, cross-track error (XTE), ETA.
- **Track:** the breadcrumb log of where you went — useful for retracing in poor
  visibility. Set logging interval (e.g. auto or every 10–30 s) and memory.
- Exchange with planning software via **GPX** files; open the GPX on a map to check
  before loading.

## 3. Reading accuracy
- Consumer receivers typically achieve a few metres horizontally in open sky; worse in
  canyons, forests, cities, and near cliffs.
- **EPE / estimated accuracy** and **HDOP/PDOP**: lower DOP = better geometry
  (HDOP < 2 good, > 5 poor). Vertical accuracy is typically worse than horizontal (×1.5–2).
- Averaging a position (many units offer it) improves a static waypoint.

## 4. Failure modes and how to spot them
| Problem | Symptoms | Response |
|---|---|---|
| Signal blockage / multipath | jumping position, track zig-zags near buildings/cliffs | move to open sky; rely on map/compass |
| Jamming | loss of fix, sudden "no position", many units affected at once | revert to independent methods; report (aviation/marine) |
| Spoofing | plausible but wrong position, sudden jump, time errors, speed/heading inconsistent with your motion | cross-check against radar, visual, DR, compass; distrust GNSS until resolved |
| Wrong datum/format | consistent offset from map features | fix settings |
| Battery/cold | sudden shutdown | lithium cells, spare batteries, keep warm |
GNSS interference has become common near conflict zones (e.g. parts of the Baltic,
Eastern Mediterranean, Black Sea) — affecting ships and aircraft. Expect it there.

## 5. Always keep an independent method
- Land: map and compass, terrain association (see
  transportation-logistics.navigation-wayfinding.map-compass-land-navigation.terrain-association-and-bearings).
- Sea: radar, visual bearings, DR and depth (see
  transportation-logistics.navigation-wayfinding.dead-reckoning.dr-and-estimated-position-plotting).
- Air: VOR/DME, DR, visual landmarks; RAIM/FDE checks before GPS approaches.
Compare GNSS position with one independent method at regular intervals.

## Gotchas
- Phone GPS kills battery fast; airplane mode + offline maps extends it.
- "Go-to" lines are straight — they ignore cliffs, rivers and shoals.
- Magnetic vs true mismatch between receiver and compass.
- Automatic map rerouting on a phone can take you onto closed or unsuitable roads.

## Verify
- [ ] Datum, format and north reference match your map/chart.
- [ ] Each route waypoint checked on the map, not only typed.
- [ ] Accuracy indicator read and understood at each fix.
- [ ] Independent cross-check done regularly; plan for GNSS loss exists.

*Uncertainty:* accuracy figures are typical, not guaranteed; interference hotspots change with events.
