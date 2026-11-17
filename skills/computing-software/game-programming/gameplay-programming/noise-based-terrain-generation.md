---
id: computing-software.game-programming.gameplay-programming.noise-based-terrain-generation
name: noise-based-terrain-generation
category: computing-software
field: game-programming
product: gameplay-programming
tags: [gameplay-programming, procedural-generation, perlin-noise, simplex-noise, fbm, octaves, domain-warping, heightmap, biomes, fastnoiselite, game-programming]
level: practitioner
status: verified
description: "Generate terrain with gradient noise: Perlin/simplex/OpenSimplex basics, fBm octaves (lacunarity, gain), domain warping, redistribution curves, biomes and chunk-seamless sampling."
sources: ["https://www.redblobgames.com/maps/terrain-from-noise/", "https://iquilezles.org/articles/fbm/", "https://github.com/Auburn/FastNoiseLite"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Noise-based terrain generation

**Goal:** natural-looking heightmaps and biome maps from seeded noise, infinite and chunkable.

## Base noise
Gradient noise (Perlin, simplex, OpenSimplex2) returns smooth values in roughly [-1, 1] for any
coordinate (OpenSimplex noise sampled here stayed within about -0.86 to 0.86, and the normalised 5-octave fBm below within about -0.59 to 0.57, so rescale to [0, 1] by the observed or theoretical range, not by assuming the full [-1, 1]). Use a library rather than writing your own: **FastNoiseLite** (portable, a source file per language including C, C++, C#, Java and JavaScript/TypeScript per its README; seeds, fractal modes, domain warp), Godot `FastNoiseLite` resource, Unity
`Mathematics.noise.snoise` / `Mathf.PerlinNoise`. Value noise looks blockier; avoid for terrain.

## fBm (fractal Brownian motion)
```
height(x, y):
    amp = 1, freq = baseFrequency, sum = 0, norm = 0
    for i in 0..octaves-1:
        sum  += amp * noise(x * freq, y * freq)
        norm += amp
        freq *= lacunarity      # ~2.0
        amp  *= gain            # ~0.5 (persistence)
    return sum / norm
```
- `baseFrequency` sets feature size (e.g. 1/500 per world unit for continents).
- Octaves 4-8: more = finer detail, more cost.
- Variants: **ridged** (`1 - abs(n)`, squared) for mountain ridges; **billow** (`abs(n)`) for hills.

## Shaping
- Redistribution: `h = pow(h01, exponent)` on a height already remapped to [0, 1] (`pow` of a negative noise value is NaN in most languages). Red Blob Games: higher exponents push middle elevations down into valleys, lower ones pull them up towards peaks.
- Islands: `h = h - distanceFromCenter^2 * k` or blend with a radial falloff mask.
- Terraces: `round(h * n) / n` blended with original.
- **Domain warping**: offset the input coordinates by another noise
  (`h = fbm(p + 4 * fbm2(p))`) for swirly, eroded-looking shapes (Inigo Quilez).
- Real erosion (hydraulic/thermal simulation) as a post-process for hero terrain.

## Biomes
Second and third noise fields for **moisture** and **temperature** (temperature also falls with
height and latitude). Biome = lookup table on (elevation, moisture) bands (Whittaker-style diagram,
Red Blob Games' approach). Blend materials at borders by distance in that 2D space.

## Chunking and seeds
- Sample noise in **world coordinates** (chunk origin + local index * spacing) so chunk borders match
  exactly (tested here: adjacent 16-sample chunks sharing an edge matched exactly when sampled in world coordinates and differed when each chunk sampled from local indices). Include one extra row/column for normals.
- Different seeds per layer (`seed + 1`, `seed + 2`) or coordinate offsets so fields are not correlated.
- Floating-point precision degrades far from origin (a float32 coordinate in metres has a step of about 7.8 mm at 100 km and 6.3 cm at 1,000 km): use doubles for
  sampling coordinates or rebase.
- Generate chunks on worker threads; noise is pure and thread-safe.

## Verify
- [ ] Same seed produces byte-identical heightmaps across runs and platforms (or accept float diffs only for visuals).
- [ ] No seams at chunk borders (render normals across borders).
- [ ] Histogram of heights matches design intent (e.g. 30% water) after redistribution.
