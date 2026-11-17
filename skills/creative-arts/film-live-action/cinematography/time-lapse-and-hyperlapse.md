---
id: creative-arts.film-live-action.cinematography.time-lapse-and-hyperlapse
name: time-lapse-and-hyperlapse
category: creative-arts
field: film-live-action
product: cinematography
tags: [cinematography, film-live-action, timelapse, time-lapse, intervalometer, hyperlapse, holy-grail-timelapse, motion-timelapse, interval-calculation, day-to-night]
level: practitioner
status: draft
description: "Shoot time-lapse: interval and duration maths, intervalometers, exposure and shutter for motion blur, day-to-night ramps, motion-control and hyperlapse moves, and processing."
sources:
  - "https://www.lrtimelapse.com (LRTimelapse - holy grail day-to-night workflow)"
  - "American Cinematographer Manual (ASC, 11th ed.) - time-lapse photography"
  - "https://www.syrp.co.nz (Syrp/Genie motion time-lapse documentation)"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Time-lapse and hyperlapse

**Goal:** smooth, flicker-free compressed time with the right speed, motion blur and
exposure through changing light.

## 1. The maths
`frames needed = clip length (s) x playback fps`; `interval = event duration / frames`.
Example: a 10-second shot at 24 fps = 240 frames; a 2-hour sunset -> interval = 7200 s /
240 = 30 s. Typical intervals: clouds 2-5 s, city traffic 1-3 s, sun/stars 15-30 s, plants
growing minutes.

## 2. Camera and intervalometer
Use a stills camera (raw) or a cinema camera's built-in **interval record** mode
(ARRI, RED, Blackmagic offer time-lapse). External intervalometer or in-camera interval
timer. Manual everything: **focus, white balance, aperture** (aperture flicker from
lens stopping down - use manual-aperture lenses or a fixed wide-open setting).

## 3. Exposure and motion blur
- Long shutter (e.g. 1/2 to several seconds, ND filters in daylight) gives smooth blur
  in moving things (traffic trails, flowing clouds); short shutter gives staccato.
- A common guideline: shutter about half the interval for smooth motion.
- **Day-to-night ("holy grail")**: exposure changes by 10+ stops. Ramp shutter/ISO in
  steps (or with auto-ramping intervalometers), then deflicker and smooth in software
  (LRTimelapse with Lightroom, or Resolve's deflicker).

## 4. Motion time-lapse and hyperlapse
- **Motion control sliders/heads** (eMotimo, Syrp Genie, Edelkrone) move a tiny amount
  between frames - parallax reveals depth.
- **Hyperlapse**: camera moved over long distances between frames (walking along a path),
  aligned to a fixed point in frame; stabilise in post (Warp Stabilizer, Resolve).

## 5. Practicalities
Power for hours (external batteries, AC), card capacity, weather protection, secure the
rig (and guard it in public), lens heater against dew at night. Shoot a test sequence.

## 6. Processing
Raw stills -> batch grade -> deflicker -> render image sequence at the project frame rate
(Resolve, After Effects, LRTimelapse). Higher-than-delivery resolution allows reframing
and digital moves.

## Gotchas
- Auto exposure/white balance - flicker and colour jumps.
- Aperture flicker from electronic lenses.
- Dew on the lens during night lapses.
- Not enough frames for the required length.

## Verify
- [ ] Interval and frame count calculated for the clip length.
- [ ] Manual focus/WB/aperture; shutter chosen for motion blur.
- [ ] Power, storage, dew and security handled.
- [ ] Deflickered sequence rendered at project fps.
