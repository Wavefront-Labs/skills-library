---
id: creative-arts.film-live-action.cinema-cameras.focus-assist-tools-and-rangefinders
name: focus-assist-tools-and-rangefinders
category: creative-arts
field: film-live-action
product: cinema-cameras
tags: [cinema-cameras, film-live-action, focus-assist-tools, light-ranger-use, cine-rt, cinetape, preston-light-ranger, dji-lidar, focus-bug, rangefinder, focus-overlay, wireless-follow-focus]
level: practitioner
status: draft
description: "Use focus assist tools as a 1st AC: Cinetape and ultrasonic rangefinders, Preston Light Ranger 2, LiDAR focus, overlays on a focus monitor, and their failure modes."
sources:
  - "https://prestoncinema.com (Preston Cinema Systems - Light Ranger 2 and FIZ documentation)"
  - "https://www.cinetape.com (Cinematography Electronics - Cinetape)"
  - "https://www.dji.com (DJI LiDAR Range Finder / Focus Pro documentation)"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Focus assist tools and rangefinders

**Goal:** sharp focus on fast, unrehearsable moves - using distance-measuring tools to
inform, not replace, the focus puller's judgement.

## 1. The tools
- **Ultrasonic** (Cinetape, Focus Bug Cine RT): measures distance to the nearest object in
  a cone; display shows feet/metres near the focus puller. Good for one subject; confused
  by foreground objects, glass and soft surfaces.
- **Preston Light Ranger 2**: infrared array overlaid on the video feed - shows zones
  across the frame with distances and a focus bar indicating where focus currently is;
  tap a zone to see/follow distance. Integrates with Preston FIZ.
- **LiDAR** (DJI LiDAR Range Finder, DJI Focus Pro, Nucleus-type): fast multi-point
  measurement with autofocus assist on gimbals and small rigs; AF/MF modes.
- **Camera tools**: peaking, magnification, and autofocus on some cine cameras.
- **Focus monitor**: a 7" monitor on the focus puller's position with false colour/
  peaking off, and the rangefinder overlay.

## 2. Setup and calibration
- Mount the sensor aligned with the lens axis and at the right offset; enter the
  **offset from the sensor plane** (focal plane mark) so distances are true.
- Calibrate the lens (motor lens mapping) for the FIZ system; check marks against a tape
  measure at a few distances.
- Define measurement zone width to the subject size.

## 3. Use in practice
- Still set **marks** in rehearsal (tape/ distance for key positions); the tool helps
  between marks and when actors miss them.
- Watch the image *and* the readout; anticipate - the readout lags slightly.
- In multi-subject frames, choose the zone; ignore readings from foreground props.
- Gimbals/Steadicam: LiDAR autofocus with manual override is common on fast shots.

## 4. Failure modes
Glass/water/mirrors (reflections), very dark or IR-absorbent surfaces, fog/haze/rain,
crowds of moving objects, sun interference for IR in bright daylight. Have a fallback:
marks and eye.

## Gotchas
- Offset not set: everything slightly off.
- Following the number into the foreground object that crossed the beam.
- Relying on the tool in rain or haze.
- Lens map out of date after a lens swap.

## Verify
- [ ] Sensor mounted, offset entered, lens mapped and checked with a tape.
- [ ] Marks still set in rehearsal.
- [ ] Zone chosen per shot; readout used with the image.
- [ ] Fallback plan for difficult conditions.
