---
id: creative-arts.film-live-action.cinematography.log-and-raw-capture-with-on-set-luts
name: log-and-raw-capture-with-on-set-luts
category: creative-arts
field: film-live-action
product: cinematography
tags: [cinematography, film-live-action, dp, director-of-photography, dit, log-capture, log, raw, log-encoding, log-c, logc3, logc4, s-log3, red-log3g10, blackmagic-film, v-log, canon-log, dynamic-range, latitude, ei-rating, exposure-index, base-iso, dual-base-iso, native-iso, highlight-headroom, etr, expose-to-the-right, middle-grey, on-set-lut, monitoring-lut, show-lut, viewing-lut, rec709-lut, cdl, look-management, colour-pipeline, aces, wide-gamut, prores, braw, arriraw, redcode, r3d, bit-depth, compression, data-rate, log-curves, logc-exposure, s-log3-exposure, raw-vs-log, data-budget, raw-decision, lut-creation, loading-luts, show-lut-on-set, dual-native-iso, noise-floor, iso-noise, exposing-for-grade, dp-colourist, grade-intent, rating-the-sensor, ei-choice, overexposing-log]
level: practitioner
status: draft
description: "Capture log or RAW correctly: what each encoding keeps, choosing EI and base ISO per scene, placing exposure in the latitude, monitoring through a show LUT with CDL, and notes for the colourist."
sources:
  - "American Cinematographer Manual, 10th ed. - Digital capture; Exposure; Color management"
  - "https://www.arri.com/en/learn-help/learn-help-camera-system/camera-workflow/image-science/log-c (ARRI LogC)"
  - "https://pro.sony/ue_US/technology/s-log3 (Sony S-Log3 technical summary)"
  - "https://www.blackmagicdesign.com/products/blackmagicraw (Blackmagic RAW)"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Log and RAW capture with on-set LUTs

**Goal:** record the maximum usable dynamic range, placed where the scene needs it,
while everyone on set judges a picture that looks like the intended film - and the
colourist receives footage plus the intent, not a mystery.

## 1. What you're recording
- **Log** (LogC3/LogC4, S-Log3, V-Log, Canon Log 2/3, RED Log3G10, Blackmagic Film Gen 5):
  a gamma curve that packs the sensor's 13-17 stops into a 10/12-bit codec (ProRes 422 HQ /
  4444 / XQ, XAVC, etc.). White balance, ISO and look are baked but highlights/shadows
  are kept with room to grade. The picture looks flat and desaturated by design.
- **RAW** (ARRIRAW, REDCODE R3D, Blackmagic RAW, X-OCN, ProRes RAW): sensor data before
  debayer; ISO, white balance and tint are **metadata** (changeable in post), bit depth
  12-16. Larger files; the grade starts from the best possible negative. Compression
  ratios (e.g. BRAW 3:1-12:1, REDCODE HQ/MQ/LQ) trade size against artefacts - test.
- **Rec.709 / "video" gamma** throws away range; only for live/news or when post is zero.
Decide per show with the post house; both Log and RAW go through a colour-managed
pipeline (ACES or camera-native wide gamut) in the grade.

## 2. EI, base ISO and where the range sits
- **Base/native ISO** (e.g. 800 on Alexa, dual base 800/3200 on Venice, 400/3200 on
  FX6) is where noise and latitude are best. Changing **EI** doesn't change sensitivity on
  most cinema cameras; it moves where middle grey is placed relative to the sensor's
  range: lower EI = more highlight headroom, less shadow room; higher EI = more shadow
  room, noisier look, less highlight. Alexa at EI 800 gives roughly 7+ stops over
  middle grey and 6+ under; EI 400 shifts a stop toward highlights.
- Choose EI per **scene**, not per shot: bright exteriors with important highlights ->
  lower EI (or just ND); night with deep shadows -> base or a dual-base high setting.
- Dual-base cameras: the high base is a different sensor mode; switching mid-scene changes noise texture - don't.

## 3. Placing exposure in log
- Middle grey in LogC3 ~ 38-40 IRE on a waveform of the log signal; S-Log3 ~ 41%;
  skin usually 5-15% above grey depending on tone. Learn the camera's **false colour**
  bands for log, or judge via the LUT with the waveform on the *log* signal.
- Protect what matters: expose so that the story-important highlight (a window, a sky,
  a face in sun) sits within range; many DPs rate log cameras 1/3-2/3 stop over the
  meter to keep shadows clean ("expose to the right"), then bring down in the grade -
  only if the highlights allow.
- RAW tolerates post ISO changes but **clipping is clipping**; monitor the sensor
  clip, not the LUT's.

## 4. Monitoring: the show LUT and CDL
- Build a **show LUT** in prep with the colourist (log -> Rec.709 or P3 with the look),
  load it into the camera (SDI output LUT, never baked into the recording unless the
  pipeline says so) and all monitors; dailies use the same LUT so the editor sees the
  same picture.
- The DIT applies per-scene **CDL** (ASC CDL: slope/offset/power/saturation) on top for
  on-set adjustments and sends CDLs with the dailies - the colourist starts from them.
- Verify monitors are calibrated (Rec.709 2.4 gamma at 100 nits for a dark tent;
  brighter for daylight viewing - know the viewing condition).
- Record the **log signal**, monitor the **LUT**, measure on the log waveform. Never
  expose by eye through a LUT on an uncalibrated monitor in sunlight.

## 5. Metadata and notes for post
Camera reports per shot: EI, white balance/tint, shutter, lens, filters, LUT/CDL ID,
frame rate, and anything odd (mixed light, intentional underexposure). RAW formats
carry much of it in-file; the rest rides on the DIT's report and ALE/CSV.

## Gotchas
- Baking the LUT into the recording "to save time" - unrecoverable.
- Changing EI shot to shot for exposure; use ND/stop and keep EI per scene.
- Exposing log "to look right" on the monitor - under by 2 stops, noisy in the grade.
- Highlight clipping judged on the LUT'd image; the log signal was fine (or vice versa).
- Different white balance per shot on a log codec; the grade matches, but it costs.

## Verify
- [ ] Codec/RAW format and compression agreed with post and tested.
- [ ] EI chosen per scene with the latitude need written down.
- [ ] Show LUT loaded on camera SDI and all monitors; recording stays log/RAW.
- [ ] Waveform/false colour on the log signal used for exposure; CDLs sent with dailies.
