---
id: natural-sciences.amateur-astronomy.astrophotography.deep-sky-imaging-polar-alignment-guiding-and-exposure
name: deep-sky-imaging-polar-alignment-guiding-and-exposure
category: natural-sciences
field: amateur-astronomy
product: astrophotography
tags: [astrophotography, deep-sky-imaging, equatorial-mount, polar-alignment, drift-alignment, sharpcap, nina, phd2, autoguiding, guiding-rms, image-scale, dithering, sub-exposure, gain, offset, iso, calibration-frames, darks, flats, bias, dark-flats, stacking, siril, deep-sky-stacker, narrowband, light-pollution, backfocus, star-trails, 500-rule, npf-rule]
level: practitioner
status: draft
description: "Capture deep-sky data that stacks well: accurate polar alignment, PHD2 guiding judged against image scale, choosing gain and sub-exposure length, dithering and calibration frames, then stacking."
sources: ["Glover, Deep Sky Astrophotography with CMOS Cameras (talk by the SharpCap author, on sub-exposure length)", "PHD2 user guide (openphdguiding.org)", "Siril documentation"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Deep-sky imaging: polar alignment, guiding and exposure

**Goal:** a night of sub-exposures that are round-starred, well-exposed above read noise,
and calibrate and stack cleanly. (Processing is covered in
natural-sciences.amateur-astronomy.pixinsight.calibrate-integrate-and-stretch-workflow.)

## 1. Untracked nightscapes (no mount)
To avoid trailing on a fixed tripod, the classic **500 rule** (500 / (focal length × crop
factor) seconds) is loose for modern high-resolution sensors. The **NPF rule** (accounts for
pixel pitch and aperture) gives shorter, more realistic limits — apps like PhotoPills
compute it. Wide aperture, ISO ~1600–6400, RAW, manual focus on a bright star with live view
magnified.

## 2. Polar alignment (equatorial mounts)
- Level the tripod roughly, set latitude on the mount.
- Use a **plate-solving polar alignment** routine (SharpCap Pro, NINA's Three-Point Polar
  Alignment, ASIAIR, or the mount's own) — faster and more accurate than a polar scope.
  Aim for error ≲ 1–2′ for long guided exposures (*more tolerance with good guiding*).
- No view of the pole? Drift alignment or the three-point methods that work anywhere in the sky.
- Balance the mount slightly **east-heavy** in RA so the gears stay meshed.

## 3. Guiding
- **Image scale** (″/pixel) = 206.265 × pixel size (µm) / focal length (mm).
- PHD2: run the **Guiding Assistant** to measure seeing and backlash, calibrate near the
  celestial equator and meridian, guide exposure ~1–3 s (longer averages seeing).
- Judge guiding by **total RMS in arcseconds** compared to imaging scale: total RMS ≲ half
  the imaging scale is a common target (e.g. at 2″/px aim for ≲1″). Don't chase RMS
  numbers below what seeing allows.
- **Dither** every 1–3 frames (a few pixels) — essential with uncooled or older sensors to
  break up walking noise and hot-pixel patterns.

## 4. Gain, offset and sub-exposure length
- Dedicated CMOS cameras: use the manufacturer's **unity gain** or the gain at the
  read-noise drop (high conversion gain mode) as a starting point; set offset so no pixel
  clips at zero in a bias frame.
- **Sub-exposure length:** long enough that sky-background noise swamps read noise.
  A common rule: background ≥ ~3–10× read noise² in electrons (*different authors use
  different factors*). Under bright suburban skies with a broadband filter that may be
  30–60 s; under dark skies or with narrowband filters several minutes.
- Total integration time matters more than sub length: SNR grows with √(total time).
- Check the histogram: background peak clearly off the left edge, stars not mostly
  saturated.

## 5. Calibration frames
- **Flats**: same optical train, focus and rotation as lights (don't touch the camera
  between lights and flats), with a light panel or sky at dusk; histogram peak ~40–60%.
- **Darks**: same gain, offset, temperature and exposure as lights (cooled cameras make
  this easy; build a library).
- **Bias or dark-flats** to calibrate the flats (for many CMOS cameras, dark-flats are more
  reliable than short bias frames).
- Collect 20–50 of each.

## 6. Stacking
Siril, Deep Sky Stacker or PixInsight WBPP: calibrate → register → reject outliers (sigma
clipping, winsorized for many frames) → integrate. Discard subs with clouds, poor FWHM or
satellite flares (rejection handles trails if you have enough frames).

## Gotchas
- Backfocus wrong for the flattener/reducer → elongated stars in the corners.
- Dew on optics at 2 a.m. — dew heaters from the start.
- Cable snags during meridian flip; check cable routing through the full sweep.
- Flats taken the next day after removing the camera.

## Verify
- [ ] Polar-alignment error measured, not guessed.
- [ ] Guide RMS compared with image scale in arcseconds.
- [ ] Sub-exposure background well above read noise; dithering on.
- [ ] Flats, darks and dark-flats matched to the lights.
- [ ] Stacked image shows round stars to the corners and no dust donuts.
