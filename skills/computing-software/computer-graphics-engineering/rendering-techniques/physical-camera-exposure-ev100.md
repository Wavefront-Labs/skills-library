---
id: computing-software.computer-graphics-engineering.rendering-techniques.physical-camera-exposure-ev100
name: physical-camera-exposure-ev100
category: computing-software
field: computer-graphics-engineering
product: rendering-techniques
tags: [computer-graphics-engineering, rendering-techniques, hdr-tonemapping, ev100, physical-camera, exposure-value, aperture-shutter-iso, photometric-units]
level: advanced
status: docs-checked
description: "Expose a renderer like a real camera: EV100 from aperture, shutter and ISO, photometric light units, exposure compensation and matching depth of field and motion blur."
sources: ["https://github.com/google/filament/blob/main/docs/Filament.md.html", "https://en.wikipedia.org/wiki/Exposure_value"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Physical camera exposure (EV100)

## 1. Formulas
```
EV100    = log2(N^2 / t * 100 / S)        // N = f-number, t = shutter seconds, S = ISO
exposure = 1 / (1.2 * 2^EV100)            // saturation-based speed, S = 100, lens attenuation q = 0.65
pixel    = sceneLuminance (cd/m^2) * exposure
```
Example: f/16, 1/125 s, ISO 100 gives EV100 about 15 (sunny day). EV100 from auto-exposure:
`log2(avgLum * 100 / 12.5)` (K = 12.5 is the reflected-light meter constant used by Canon, Nikon and Sekonic; some manufacturers use 14).

## 2. Lights in physical units
- Sun: about 100,000 lux illuminance at midday, sky about 20,000 lux (Filament's table).
- Point/spot: luminous power in lumens, intensity `I = Phi / (4 pi)` cd for
  points, `Phi / pi` for spots (Filament keeps spot intensity independent of cone angle).
- Emissive surfaces in nits (cd/m^2).
With units consistent, exposure is the only "brightness knob", and day/night transitions work.

## 3. Precision
Values up to 1e5 overflow half floats (max 65504) before exposure. Pre-expose: multiply light
intensities by the previous frame's exposure in the shader, so the HDR buffer holds near-1 values.

## 4. Matching camera effects
Use the same N, t and focal length to drive depth of field (circle of confusion) and motion blur
(shutter angle), so changing aperture changes both exposure and blur consistently.

## Gotchas
- Mixing artistic light intensities with physical sun values makes interiors black; convert
  everything or none.
- Auto exposure should work in EV space and add compensation in EV stops.

## Verify
- [ ] A scene metered at f/16, 1/125 s, ISO 100 (EV100 about 15) shows daylight-lit surfaces at sensible brightness.

## Checked

2026-10-26: Filament materials/lighting document (google/filament docs/Filament.md.html), read 2026-10-26. Confirmed: EV100 = log2(N^2 / t * 100 / S), exposure = 1 / (2^EV100 * 1.2) from H_sat with S = 100 and q = 0.65, EV = log2(L * 100 / 12.5) with K = 12.5 (Canon, Nikon, Sekonic; 14 for others), and the sun and sky illuminance table. f/16, 1/125 s, ISO 100 evaluates to 14.97 by arithmetic. Wrong claim fixed: the sky value of about 20,000 is an illuminance in lux, not a luminance in cd/m^2. Removed the 60 W bulb lumen figure, the monitor 200 nit figure, the Frostbite attribution and the 18 percent grey check.

Method: documentation only; no commands were run.
