---
id: creative-arts.film-live-action.cinematography.dynamic-range-testing-and-shooting-for-hdr
name: dynamic-range-testing-and-shooting-for-hdr
category: creative-arts
field: film-live-action
product: cinematography
tags: [cinematography, film-live-action, dynamic-range-test, latitude-test, clip-point, hdr-capture, shooting-for-hdr, hdr-on-set, stop-chart, noise-floor, hdr-monitoring]
level: practitioner
status: draft
description: "Test a camera's latitude (over/under exposure series, clip point, noise floor, EI choice) and adapt capture for HDR delivery: highlights, specular sources, monitoring and LUTs."
sources:
  - "American Cinematographer Manual (ASC, 11th ed.) - digital capture and HDR"
  - "https://partnerhelp.netflixstudios.com (Netflix - camera testing and HDR production guidance)"
  - "https://www.dolby.com/about/support/guide/ (Dolby Vision - production and on-set guidelines)"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Dynamic range testing and shooting for HDR

**Goal:** know exactly how many stops your camera holds above and below key at your
chosen EI - and expose so the HDR grade has clean highlights and shadows to use.

## 1. Latitude test
1. Light a subject (face + grey card + white and black patches + a colour chart) evenly;
   meter the key.
2. Shoot a **series** from -6 to +6 stops in 1-stop increments (change exposure by
   shutter or lights, not ISO/EI - keep EI fixed; or use ND).
3. In the grade, **normalise** each clip back to correct exposure and compare: where do
   highlights **clip** (no detail returns) and where do shadows become noisy/unusable?
4. Record the usable range above and below key - e.g. "+6/-5 at EI 800".
5. Repeat at other EIs: raising EI shifts latitude toward the highlights (more over,
   less under) on most cinema cameras - choose the EI for the scene's balance.

## 2. Stop charts
Transmissive stop charts (e.g. Xyla 21) show the full DR in one frame for measuring the
**clip point** and **noise floor** precisely; good for comparing cameras.

## 3. Shooting for HDR
HDR (PQ, up to 1000-4000 nits mastering) shows highlight detail and colour SDR clips:
- **Protect highlights**: speculars, practicals, windows and skies will be displayed
  bright and detailed - clipped highlights look harsh (flat white blobs, colour shifts).
- Practicals and lamps: control their level - HDR makes them very bright; a bare bulb in
  frame can be distractingly intense.
- **Shadows**: HDR reveals shadow noise more; expose for clean shadows or accept noise
  as texture.
- Sensor and lens flare/veiling glare become more visible.
- Wardrobe/production design: extreme whites and saturated colours show differently.

## 4. Monitoring
Monitor in HDR on set where possible (e.g. Sony BVM-HX310 / FlandersScientific HDR
monitors) at least at the DIT/video village; otherwise use waveform in nits/PQ and a
show LUT with an HDR version. Check false colour for clipping in the log signal.

## Gotchas
- Changing EI mid-test (it's not a latitude test then).
- Judging clip from the Rec.709 LUT rather than the log signal.
- Practicals at levels that look fine in SDR but blinding in HDR.
- No HDR monitoring; issues found in the HDR grade.

## Verify
- [ ] Latitude series shot and analysed; usable stops recorded per EI.
- [ ] Clip point and noise floor known; EI chosen per scene type.
- [ ] Highlights and practicals controlled for HDR.
- [ ] HDR monitoring or log-based checks in place.
