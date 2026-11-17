---
id: creative-arts.film-live-action.cinematography.exposure-and-lighting-ratios-for-a-scene
name: exposure-and-lighting-ratios-for-a-scene
category: creative-arts
field: film-live-action
product: cinematography
tags: [cinematography, film-live-action, dp, director-of-photography, exposure, exposure-control, stops, t-stop, f-stop, iso, ei, exposure-index, shutter-angle, 180-degree-shutter, nd-filters, neutral-density, light-meter, incident-meter, false-color, waveform, zebras, log, dynamic-range, key-light, fill-light, backlight, lighting-ratio, contrast-ratio, three-point-lighting, motivated-lighting, negative-fill, bounce, diffusion, skin-tone-exposure, false-colour-exposure, zebra-exposure, exposure-tools, waveform-exposure, ire-targets, exposing-with-scopes, stop-arithmetic, nd-calculation, t-stop-math, measuring-ratios, ratio-meter, setting-ratios]
level: practitioner
status: draft
description: "Expose and light a live-action scene with intent: stops and the exposure triangle on cinema cameras, metering with incident meter and false colour, key-to-fill ratios, and motivated lighting."
sources: []
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Exposure and lighting ratios for a scene

**Goal:** control how bright the subject is and how much contrast sits across the
face and frame — on purpose, consistently from shot to shot — so the image tells the
story and the colourist has a clean negative to grade.

## 1. Think in stops
A **stop** is a doubling or halving of light. Every exposure control is counted in stops:
- **Aperture (T-stop on cine lenses):** T1.4, 2, 2.8, 4, 5.6, 8, 11, 16 — each step is
  one stop. Cine lenses are marked in T-stops (measured light transmission), which is why
  they match between lenses better than f-stops.
- **Shutter angle:** at 24 fps, **180°** ≈ 1/48 s gives "normal" motion blur. Changing
  shutter alters motion feel, so it's usually left at 180° and not used for exposure.
  (Under 50 Hz mains or LED flicker, 172.8° or other flicker-safe settings may be needed.)
- **ISO/EI:** on most digital cinema cameras the base ISO gives the most dynamic range;
  changing EI mostly shifts where highlights vs shadows sit, it doesn't add light.
- **ND filters:** the main exposure tool outdoors. ND 0.3 = 1 stop, 0.6 = 2, 0.9 = 3,
  1.2 = 4, etc. Choose the stop for **depth of field**, then ND to match exposure.

## 2. Measure
- **Incident meter** at the subject, dome pointed at the lens, set to your fps/shutter
  and EI: gives the stop for correct exposure of the key. Point it at each light separately
  (cover the others) to read individual sources for ratios.
- **False colour** on the monitor: maps brightness bands to colours. Learn your
  camera's chart — e.g. where it shows 18% grey and typical skin. Expose the important
  skin at its intended band; check highlights aren't clipping (often shown red/white).
- **Waveform:** shows brightness across the frame horizontally; clipping appears as a flat
  line at the top. Better than judging the on-set monitor by eye, which lies in sunlight.
- When shooting **log**, the picture looks flat; judge exposure through a monitoring LUT
  but measure with false colour/waveform on the log signal per your camera's guidance.

## 3. Lighting ratios (key to fill)
The ratio of light on the bright side of the face (key + fill) to the shadow side (fill):
- **2:1** (1 stop difference) — soft, bright, comedy/commercial.
- **4:1** (2 stops) — natural drama.
- **8:1** (3 stops) and beyond — moody, noir, thriller.
Measure key and fill with the incident meter; the stop difference *is* the ratio
(each stop doubles). Keep the ratio consistent across a scene's shots so faces match when
cut together — re-meter after each turnaround.

## 4. Build the scene's light
1. **Motivation:** decide where the light "comes from" in the story world (window,
   practical lamp, moon, screen). Place the key to agree with it.
2. **Key** — soft (large/diffused source, close) for flattering, hard (small, far) for
   drama. Many DPs key from the **far side** (the side of the face away from camera) for
   shape.
3. **Fill** — bounce, a dim large source, or simply none. Control contrast also with
   **negative fill** (black flags/floppies absorbing spill) — often more useful than adding light.
4. **Back/edge light** — separates subject from background; keep it motivated or subtle.
5. **Background** — usually darker than the face for depth; add pools and texture,
   control with flags.
6. **Practicals** — lamps in frame; dim them (bulbs, dimmers, ND gel) so they read
   without clipping.

## Gotchas
- Lighting the wide and forgetting the closeups need re-shaping (ratio changes as camera turns).
- Mixed colour temperatures unplanned — daylight from windows vs tungsten practicals;
  gel deliberately (CTB/CTO) or choose the mix as a look.
- Exposing to the sky, losing faces; exposing everything "middle" — kills mood.
- Trusting a phone app meter for critical work (fine for scouting only).

## Verify
- [ ] Stop chosen for depth of field; ND used to hit exposure; shutter kept at 180° (or flicker-safe).
- [ ] Key skin tone sits at a planned false-colour band; no unintended clipping on waveform.
- [ ] Key:fill ratio measured and noted per scene; consistent across the scene's shots.
- [ ] Every light has a motivation or a deliberate stylistic reason.
