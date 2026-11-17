---
id: creative-arts.animation.blender.osl-noise-functions
name: osl-noise-functions
category: creative-arts
field: animation
product: blender
tags: [blender, osl-noise-functions, osl-noise, osl, procedural-texture, pnoise, cellnoise]
level: advanced
status: docs-checked
description: "Use OSL noise in Cycles: noise and pnoise types (perlin, uperlin, simplex, usimplex, cell, hash, gabor), fBm loops and the OptiX limits on noise types."
sources:
  - https://open-shading-language.readthedocs.io/en/main/stdlib.html#pattern-generation
  - https://docs.blender.org/manual/en/latest/render/cycles/osl/index.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---

# osl-noise-functions

Goal: custom procedural patterns beyond the built-in Noise/Voronoi nodes.

## The noise function

```c
float n  = noise("perlin", p);       // signed
float u  = noise("uperlin", p);      // unsigned 0..1 (also plain noise(p))
float s  = noise("simplex", p);      // signed simplex, range -1..1; "usimplex" is unsigned 0..1
float c  = noise("cell", p);         // constant per integer cell
color h  = noise("hash", p);         // uncorrelated, deterministic value at every input coordinate
float g  = noise("gabor", p);        // Gabor impulse noise
float pp = pnoise("perlin", p, point(4,4,4));   // periodic, tiles every 4 units
```
`noise` takes a float, two floats, a point, or a point plus a float (time); `pnoise` takes the matching period arguments. The return type follows the assigned variable (float, color, vector).

Cycles on the **OptiX** GPU backend does not provide every noise type: the Blender manual names Cell, Simplex and Gabor as unavailable there.
## fBm

```c
shader fbm(point Vector = P, float Scale = 4.0, int Octaves = 6, float Lacunarity = 2.0,
           float Gain = 0.5, output float Fac = 0)
{
    point p = Vector * Scale;
    float amp = 0.5, sum = 0.0, norm = 0.0;
    for (int i = 0; i < Octaves; i++) {
        sum += amp * noise("perlin", p);
        norm += amp;
        p *= Lacunarity;
        amp *= Gain;
    }
    Fac = 0.5 + 0.5 * sum / norm;
}
```

## Coordinate spaces

A `point Vector = P` input defaults to the shading point unless connected; connect a Texture Coordinate node output when you need object-locked patterns, or convert with `transform("object", P)` (OSL standard library) and check the result as the object moves.

## Gotchas

- `noise("cell", p)` steps at integer boundaries; scale the input to set cell size.
- Signed variants average about 0; remap before using as a colour (the fBm above does).
- High octave counts cost more per shading sample; clamp Octaves.

## Verify

Plug Fac into an Emission shader: changing Octaves visibly adds detail and the pnoise version tiles at the period. Check that the pattern stays fixed on the object when it moves.

## Checked

2026-10-27 against the OSL standard library documentation (noise types perlin, uperlin, simplex, usimplex, cell, hash, gabor; pnoise signatures) and the Blender 5.2 manual, Cycles > Open Shading Language (Cell, Simplex and Gabor unavailable on OptiX). Removed unconfirmed claims (world-space meaning of P, noise speed, comparison with the Noise Texture node, numeric range for Perlin). Method: documentation only; no commands were run.
