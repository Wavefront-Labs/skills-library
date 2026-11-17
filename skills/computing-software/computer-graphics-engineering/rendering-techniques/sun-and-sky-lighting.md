---
id: computing-software.computer-graphics-engineering.rendering-techniques.sun-and-sky-lighting
name: sun-and-sky-lighting
category: computing-software
field: computer-graphics-engineering
product: rendering-techniques
tags: [computer-graphics-engineering, rendering-techniques, local-illumination, sun-light, sky-lighting, directional-light, sun-disk, atmosphere, time-of-day]
level: practitioner
status: draft
description: "Light outdoor scenes with sun and sky: directional sun as a disk light, sky ambient from atmosphere/SH, matching sun illuminance to sky, and time-of-day updates."
sources: ["https://seblagarde.files.wordpress.com/2015/07/course_notes_moving_frostbite_to_pbr_v32.pdf", "https://sebh.github.io/publications/egsr2020.pdf", "https://docs.unrealengine.com/5.3/en-US/sky-atmosphere-component-in-unreal-engine/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Sun and sky lighting

## 1. Sun as a directional light
- Intensity in lux: clear noon ~100 000-120 000 lx at sea level (sun disk only, sky adds
  ~20 000 lx). Low sun is weaker and redder because of atmospheric transmittance: multiply the
  sun colour by transmittance along the view-to-sun path (from the atmosphere LUT).
- **Sun disk area**: the sun subtends ~0.53 degrees. Treat it as a disk light for specular
  (Frostbite: modify the reflection direction toward the disk to get a correctly sized highlight
  on smooth surfaces) and for soft shadow penumbra (PCSS light size).

## 2. Sky ambient
- Atmosphere model (Hillaire 2020 / Bruneton) renders sky radiance; capture it into a low-res
  cubemap (e.g. 32^2-128^2) every few frames or when the sun moves, then prefilter for IBL and
  project to SH for diffuse.
- Real-time: time-slice the capture (one face per frame) to amortise.
- Indoors/occluded: sky light must be occluded (SSAO, baked sky visibility, probes); otherwise
  interiors glow blue.

## 3. Balancing
With physical units the sky is roughly 1/5-1/10 of the sun at noon, shadows look blue-ish. Exposure
EV100 ~ 14-15. Don't arbitrarily boost ambient; check against reference photos (shadow vs lit
ratio ~ 1:5-1:10).

## 4. Time of day
- Drive sun direction from date/latitude or artist curve; update transmittance colour, sky
  capture, fog inscattering colour together.
- Moon as a second directional light at night (~0.1-0.3 lx full moon) with a different exposure
  target; switch shadows to the moon when the sun is below the horizon.
- Cascaded shadow cache invalidation as the sun moves: update slowly or in steps.

## Gotchas
- Sun specular on very smooth materials as a point light gives an unrealistically tiny bright
  highlight that aliases; disk approximation fixes it.
- Sky cubemap that includes the sun disk plus a separate sun light double counts; mask the disk
  out of the sky capture.

## Verify
- [ ] Lit/shadow luminance ratio within a plausible range for clear sky.
- [ ] Sunset reddens both direct light and sky consistently.
