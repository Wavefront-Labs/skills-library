---
id: computing-software.computer-graphics-engineering.graphics-math.spectral-upsampling
name: spectral-upsampling
category: computing-software
field: computer-graphics-engineering
product: graphics-math
tags: [computer-graphics-engineering, graphics-math, colour-science, spectral-upsampling, spectral-rendering, rgb-to-spectrum, metamerism, jakob-hanika]
level: advanced
status: draft
description: "Convert RGB colours to plausible spectra for spectral rendering: Smits basis, Jakob-Hanika sigmoid polynomial tables, energy conservation limits, and wide-gamut/emissive handling."
sources: ["https://rgl.epfl.ch/publications/Jakob2019Spectral", "https://pbr-book.org/4ed/Radiometry,_Spectra,_and_Color/Color", "https://www.cs.utah.edu/~bes/papers/color/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Spectral upsampling

Spectral renderers need spectra, but assets are RGB. Many spectra map to the same RGB (metamers);
upsampling chooses a smooth, physically valid one.

## Requirements
- Round trip: upsampled spectrum rendered under the working-space illuminant must reproduce the RGB.
- Reflectances must stay within [0,1] at every wavelength (energy conservation).
- Smooth spectra (natural materials are smooth) so results under other illuminants are plausible.

## Methods
- **Smits (1999)**: combination of 7 precomputed basis spectra (white, cyan, magenta, yellow, red,
  green, blue). Simple and fast; spectra are piecewise constant-ish and round trip is approximate.
- **Jakob and Hanika (2019)**: spectrum `s(lambda) = sigmoid(c0 lambda^2 + c1 lambda + c2)`, with
  the 3 coefficients precomputed in a 3D table over RGB (per colour space). Smooth, always in [0,1],
  exact round trip for all valid reflectances; used by PBRT-v4 (`RGBAlbedoSpectrum`,
  `RGBUnboundedSpectrum`) and Mitsuba 3.
- Mallett and Yuksel (2019): convex combination of three sRGB-primary spectra; guaranteed bounded
  for in-gamut sRGB.

## Emission and unbounded values
Illuminant spectra are not bounded by 1: scale a bounded shape by a factor (PBRT's
`RGBUnboundedSpectrum`), and multiply by the colour space's illuminant spectrum (e.g. D65) for
emissive RGB so white emitters reproduce white.

## Wide gamut limits
Saturated colours near the spectral locus need very peaky spectra; colours outside the
reflectance-feasible (MacAdam) limits cannot be represented as reflectances at all; clamp or map.

## Verify
For a grid of RGB values: upsample, integrate against CMFs under the reference illuminant, convert
back; max delta E below about 0.1 for in-gamut colours, and min/max of each spectrum within [0,1].
