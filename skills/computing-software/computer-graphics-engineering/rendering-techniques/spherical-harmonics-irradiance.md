---
id: computing-software.computer-graphics-engineering.rendering-techniques.spherical-harmonics-irradiance
name: spherical-harmonics-irradiance
category: computing-software
field: computer-graphics-engineering
product: rendering-techniques
tags: [computer-graphics-engineering, rendering-techniques, local-illumination, spherical-harmonics, sh-l2, irradiance-environment-map, light-probes, cosine-lobe, ringing, sh-projection]
level: advanced
status: docs-checked
description: "Store and evaluate diffuse lighting with order-2 spherical harmonics: 9 coefficients from an environment map, cosine-lobe constants, error bounds, and ringing."
sources: ["https://graphics.stanford.edu/papers/envmap/envmap.pdf", "https://www.ppsloan.org/publications/StupidSH36.pdf"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Spherical harmonics irradiance

**Goal:** diffuse ambient lighting from an environment or a light probe stored in 9 RGB
coefficients (27 floats), evaluated in a few operations (Ramamoorthi and Hanrahan, SIGGRAPH 2001).

## 1. Basis (bands l = 0 to 2, 9 functions), for a unit direction (x, y, z)
```
Y00 = 0.282095
Y11 = 0.488603 x   Y10 = 0.488603 z   Y1-1 = 0.488603 y
Y21 = 1.092548 xz  Y2-1 = 1.092548 yz  Y2-2 = 1.092548 xy
Y20 = 0.315392 (3z^2 - 1)
Y22 = 0.546274 (x^2 - y^2)
```
The paper's coordinate convention has +Z as the pole of the images. If your engine uses Y-up,
permute axes consistently when projecting and evaluating.

## 2. Project the environment (prefiltering)
The 9 lighting coefficients are `Llm = integral of L(theta, phi) * Ylm(theta, phi) sin(theta)`. For
an environment map this is a sum over the pixels, weighted by `Ylm` and by each pixel's solid
angle (the `sin(theta)` term), for each colour channel separately. Cost is O(9 S) for S pixels,
versus O(T x S) for building an irradiance map of T texels; the paper projects a 300x300 map in
under a second.

## 3. Cosine convolution to irradiance
`Elm = A^l * Llm`, with the clamped-cosine band constants (paper equation 9):
`A^0 = pi (3.141593)`, `A^1 = 2 pi / 3 (2.094395)`, `A^2 = pi / 4 (0.785398)`.
Irradiance is `E(n) = sum over l,m of A^l Llm Ylm(n)`, and radiosity is `B = albedo * E`. Fold the
constants into stored coefficients so the shader does only the polynomial. If your Lambert term
is `albedo / pi * E`, divide by pi once, and apply the cosine convolution only once.

## 4. Evaluate
Using the paper's matrix form, `E(n) = n^T M n` with `n = (x, y, z, 1)` and a 4x4 symmetric
matrix M per colour channel (paper equation 12):
```
c1 = 0.429043  c2 = 0.511664  c3 = 0.743125  c4 = 0.886227  c5 = 0.247708
M = | c1 L22   c1 L2-2  c1 L21   c2 L11 |
    | c1 L2-2 -c1 L22   c1 L2-1  c2 L1-1|
    | c1 L21   c1 L2-1  c3 L20   c2 L10 |
    | c2 L11   c2 L1-1  c2 L10   c4 L00 - c5 L20 |
```
This needs a matrix-vector multiply and a dot product per channel. To rotate the lighting, apply
the inverse rotation to the normal. The paper tabulates Llm for three light probes (Grace
Cathedral, Eucalyptus Grove, St. Peter's Basilica) that can be used to check an implementation.

## 5. Accuracy
- Order 2 (9 coefficients) approximates irradiance with a worst-case error of 9 percent of total
  illumination at any pixel, and under 3 percent on average over normals for any physical
  lighting. For the paper's natural environment maps the average error was under 1 percent and the
  maximum pixel error under 5 percent.
- This is diffuse lighting only; the same low-frequency argument does not hold for specular.
- Sloan's "Stupid Spherical Harmonics Tricks" notes that order 3 (bands 0 to 2) approximates the
  clamped cosine kernel well, but overestimates by 1/16 at the pole and has a spurious lobe of
  1/16 at the opposite pole. A directional light that reflects 17 pointing at it would reflect 1
  in the opposite direction. With HDR light sources consider order 5 (the order 4 band is zero),
  which has its own negative lobe (about -1 against 31).

## 6. Ringing
Truncating SH series causes ringing (Gibbs phenomenon) with strong directional sources. Sloan's
fixes:
- Window the coefficients with a kernel that tapers to zero at the cut-off band (Lanczos sigma
  factors or a Hanning window); this trades ringing against blurring, and the choice of window
  matters less than being able to tune that trade-off.
- Extract the dominant lights from the probe and treat them as analytic lights, which have no
  negative lobes.
- For irradiance environment maps windowing is rarely necessary, because the clamped-cosine
  convolution already attenuates high frequencies.

## Verify
- [ ] A constant environment of radiance 1 gives irradiance pi (or 1 after your 1/pi convention) for every normal.
- [ ] The paper's tabulated Llm values for a probe reproduce plausible lighting on a sphere.
- [ ] An axis-coloured test environment lights each side of a sphere with the expected colour (checks axis conventions).

## Checked
2026-11-09. Read: Ramamoorthi and Hanrahan, "An Efficient Representation for Irradiance
Environment Maps" (basis constants, A^l values, projection integral and cost, matrix form and
constants c1 to c5, error bounds) and Sloan, "Stupid Spherical Harmonics Tricks" (order 3 and 5
kernel approximation, windowing, light extraction, rotation as block matrices). Corrected: the
error statement (the skill said 1 to 3 percent average; the paper gives under 3 percent worst
case on average, under 1 percent on its examples, 9 percent maximum). Removed: the texel
solid-angle formula, the 7 vec4 packing, linear blending of probe coefficients, the claim that
SH rotation is costly with re-projection as the alternative, the Filament and RTR4 sources
(not read), and the specific sigma-factor formulas.
Method: docs-checked 2026-11-09 against the Ramamoorthi and Hanrahan paper and Sloan's SH tricks paper.
