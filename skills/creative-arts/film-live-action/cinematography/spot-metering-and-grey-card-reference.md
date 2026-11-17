---
id: creative-arts.film-live-action.cinematography.spot-metering-and-grey-card-reference
name: spot-metering-and-grey-card-reference
category: creative-arts
field: film-live-action
product: cinematography
tags: [cinematography, film-live-action, spot-metering, spot-meter, placing-tones, grey-card, 18-percent-grey, chart-reference, zone-system, incident-metering, false-colour]
level: practitioner
status: draft
description: "Meter like a DP: incident vs reflected, spot-metering and placing tones in stops above and below key, and using grey cards and charts as exposure and grading references."
sources:
  - "American Cinematographer Manual (ASC, 11th ed.) - exposure and metering"
  - "Blain Brown, Cinematography - Theory and Practice (exposure; the zone system)"
  - "https://www.sekonic.com (Sekonic - metering guides for cine)"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Spot metering and grey-card reference

**Goal:** know where every important tone sits relative to key - before you roll -
and give post a reliable reference.

## 1. Incident vs reflected
- **Incident** meter (dome at the subject, facing camera or the key) reads the *light*:
  set the stop for correct mid-grey regardless of subject tone. Base exposure.
- **Reflected / spot** meter (1-degree) reads the *surface*: tells you how bright a
  specific tone will be relative to mid-grey. Use it for the sky, a window, a white
  shirt, dark skin, a practical lamp.

## 2. Placing tones (stops from key)
Set the camera to the incident stop (e.g. T2.8 at ISO 800, 24fps 180 degree). Spot-meter
each area and express the reading as **stops over/under** the incident stop:
- Mid-grey = 0. Caucasian skin often +1, darker skin 0 to -2 (meter the actual skin).
- Clean white shirt about +2 to +2.5; a window you want to read with detail: no more than
  the camera's highlight latitude above key (+5 to +6 for many log cameras).
- Shadows with detail down to -4/-5; black below that.
Zone system language: Zone V = mid-grey, each zone one stop.

## 3. Camera tools to cross-check
- **False colour** (ARRI, RED, Blackmagic, Sony): each colour = an IRE band; check skin
  sits in the mid-tone band and highlights aren't clipping.
- **Waveform** in the camera or on the DIT cart; **zebras** at clip warning.
Meter and false colour should agree within ~1/3 stop; if not, check the camera's EI and
the LUT the monitor shows (log vs Rec.709 LUT changes the IRE).

## 4. Grey card and charts
- Hold an **18% grey card** (and white/black patches) in the key light at the start of
  each set-up or lighting change: the grade has a known neutral and exposure reference.
- A **colour chart** (Macbeth/X-Rite ColorChecker, DSC Chroma Du Monde) at the head of
  each scene or each camera; for multi-camera matching, shoot it on every camera.
- Shoot with the chart **filling a good part of the frame**, lit evenly by the scene key,
  not a separate light.

## Gotchas
- Spot-metering a face and exposing it as mid-grey - pale skin goes muddy, dark skin too bright.
- Judging exposure from the monitor's Rec.709 LUT brightness alone.
- Grey card held in shadow or at an angle catching glare.
- Meter ISO/shutter/frame rate not matching camera settings.

## Verify
- [ ] Incident base stop set; key tones spot-metered and recorded in stops.
- [ ] False colour / waveform agrees with the meter.
- [ ] Grey card and chart shot per set-up in the key light.
- [ ] Meter settings match camera EI, shutter and frame rate.
