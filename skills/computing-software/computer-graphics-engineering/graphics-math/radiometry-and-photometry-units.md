---
id: computing-software.computer-graphics-engineering.graphics-math.radiometry-and-photometry-units
name: radiometry-and-photometry-units
category: computing-software
field: computer-graphics-engineering
product: graphics-math
tags: [computer-graphics-engineering, graphics-math, colour-science, radiometry, photometry, physical-light-units, lumens-candela-lux, radiance]
level: sme
status: draft
description: "Use radiometric and photometric units correctly in renderers: flux/intensity/irradiance/radiance, lumens, candela, lux, nits, and converting light specs to shader values."
sources: ["https://pbr-book.org/4ed/Radiometry,_Spectra,_and_Color/Radiometry", "https://google.github.io/filament/Filament.html#lighting/units", "https://seblagarde.wordpress.com/wp-content/uploads/2015/07/course_notes_moving_frostbite_to_pbr_v32.pdf", "https://www.realtimerendering.com/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Radiometry and photometry units

## 1. Quantities
| Radiometric | Unit | Photometric | Unit | Used for |
|---|---|---|---|---|
| Flux (power) | W | Luminous flux | lm | bulb output |
| Intensity | W/sr | Luminous intensity | cd = lm/sr | spot/point lights, IES profiles |
| Irradiance | W/m^2 | Illuminance | lux = lm/m^2 | sun on ground, light meter |
| Radiance | W/(m^2 sr) | Luminance | cd/m^2 = nit | pixel values, sky, emissive, displays |
Photometric = radiometric weighted by the eye's luminous efficiency V(lambda), 683 lm/W at 555 nm.
Shaders integrate radiance; everything converts to it.

## 2. Converting light specs (Frostbite/Filament conventions)
- Point light from lumens: `I = Phi / (4 pi)` cd. Spot (keeping brightness with cone): `I = Phi / pi`
  (Frostbite), or physically `Phi / (2 pi (1 - cos(outer/2)))`.
- Illuminance at distance d: `E = I / d^2` (inverse square, times cos theta).
- Directional (sun): specify illuminance, e.g. ~100 000 lux clear noon; shader uses `E * BRDF * NdotL`.
- Area/sphere light from lumens: luminance `L = Phi / (A * pi)` for a Lambertian emitter of area A.
- Emissive surfaces: luminance in nits (a phone screen ~ 500 nits, a fluorescent tube ~ 10 000).
- Sky: luminance ~ 5000-10000 nits overhead on a clear day.

## 3. Pair with physical exposure
Scene values in these units span 1e-3 to 1e9, so you need physical camera exposure (EV100) before tone
mapping; pre-expose values (multiply by exposure on the CPU side) to stay in fp16 range.

## 4. Colour
Light colour should be a chromaticity with unit luminance (normalise so `dot(rgb, lumaWeights) = 1`), then
multiplied by the photometric intensity; otherwise changing colour changes brightness.

## Gotchas
- Mixing "artist intensity" lights with physical sun values: one or the other dominates; pick one system.
- Lumens to watts depends on efficacy (LED ~ 100 lm/W); do not convert bulb wattage directly.
- Inverse-square without a minimum distance blows up near the light: clamp d (e.g. 1 cm) or use sphere lights.
- 16-bit float max is 65504: unexposed sun-lit radiance overflows to inf.

## Verify
- [ ] A 800 lm point light at 1 m gives ~64 lux on a facing surface (800/4pi); sunny scene at EV100 ~15 shows mid-grey around 18% albedo.
