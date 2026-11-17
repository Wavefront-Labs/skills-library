---
id: creative-arts.animation.blender.mathutils-noise
name: mathutils-noise
category: creative-arts
field: animation
product: blender
tags: [blender, mathutils-noise, procedural-noise, fractal-noise, turbulence, bpy, mathutils]
level: practitioner
status: verified
description: "Generate procedural values in Python with mathutils.noise: noise bases, fractal, turbulence, ridged and hetero terrain, voronoi, random vectors and seeding."
sources:
  - https://docs.blender.org/api/current/mathutils.noise.html
  - https://docs.blender.org/api/current/mathutils.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---

# mathutils-noise

Goal: procedural displacement, jitter and terrain in scripts without NumPy noise libraries.

## Core calls

```python
from mathutils import Vector, noise
noise.seed_set(42)                                    # deterministic random_* results
p = Vector((x * 0.2, y * 0.2, 0.0))                   # scale the input = frequency
n  = noise.noise(p, noise_basis='PERLIN_ORIGINAL')    # float
v  = noise.noise_vector(p)                            # 3D vector noise (for displacement directions)
f  = noise.fractal(p, 1.0, 2.0, 6, noise_basis='PERLIN_NEW')   # H, lacunarity, octaves
t  = noise.turbulence(p, 4, False)                    # octaves, hard (sharp transitions if True)
rm = noise.ridged_multi_fractal(p, 1.0, 2.0, 6, 1.0, 2.0)      # H, lacunarity, octaves, offset, gain
ht = noise.hetero_terrain(p, 1.0, 2.0, 6, 0.5)
d, pts = noise.voronoi(p, distance_metric='DISTANCE', exponent=2.5)  # distances to the four closest features, and their locations
c  = noise.cell(p)                                    # constant per cell (stepped random)
r  = noise.random_unit_vector(size=3)
```

Noise bases: `BLENDER`, `PERLIN_ORIGINAL` (default), `PERLIN_NEW`, `VORONOI_F1` to `VORONOI_F4`, `VORONOI_F2F1`, `VORONOI_CRACKLE`, `CELLNOISE`. Other functions: `multi_fractal`, `hybrid_multi_fractal`, `variable_lacunarity`, `cell_vector`, `random`, `random_vector`.

## Example: displace a grid

```python
import bpy
me = bpy.context.object.data
for v in me.vertices:
    v.co.z = noise.fractal(v.co * 0.5, 1.0, 2.0, 5) * 0.8
me.update()
```
For large meshes, read coordinates with `foreach_get`, loop over the noise calls in Python, and write back with `foreach_set` (practice).

## Gotchas

- `seed_set(seed)` sets the seed for `random`, `random_vector` and `random_unit_vector` only (seed 0 means use the current time); for the noise functions add an offset vector per seed instead (the docs list no seed for them).
- Output ranges differ by function and the docs do not state them; normalise empirically (sample min/max) before remapping.
- `random_unit_vector(size=)` takes a size from 2 to 4; `random_vector(size=)` needs 2 or more.

## Verify

Run the same script twice with the same seed and offset: identical vertex positions; change the offset and get a new pattern.

## Checked

Blender Python API 5.2 (docs.blender.org/api/current/mathutils.noise.html), read 2026-10-27.
- Signatures and defaults of noise, noise_vector, fractal(position, H, lacunarity, octaves), turbulence(position, octaves, hard, *, noise_basis, amplitude_scale, frequency_scale), ridged_multi_fractal, hetero_terrain, voronoi(position, *, distance_metric, exponent=2.5), cell, random_unit_vector(*, size=3), seed_set; the list of noise basis strings.
- seed_set scope (random, random_vector, random_unit_vector; zero uses the time).
- Removed as unconfirmed: output ranges, the claim that the bases match legacy texture types, the integer-lattice remark, the no-vectorised-form claim.

Run check, 2026-11-01, Blender 4.5.14 LTS headless: every function in the example (noise, noise_vector, fractal, turbulence, ridged_multi_fractal, hetero_terrain, voronoi returning four distances and four points, cell, random_unit_vector) plus multi_fractal, hybrid_multi_fractal, variable_lacunarity, cell_vector, random and random_vector ran with the arguments shown; all ten noise basis names were accepted and an unknown one raised ValueError; `random_unit_vector(size=)` accepted 2 to 4 and rejected 1 and 5, `random_vector(size=)` rejected 1 and accepted 5; `seed_set(42)` made `random` and `random_unit_vector` repeat while `noise.noise` ignored the seed; `noise.noise` without a basis equals `PERLIN_ORIGINAL`; sampled ranges were about -0.83 to 0.83 for noise and -1.05 to 0.95 for fractal. Unrun: the seed 0 uses the current time statement (documentation only).

Method: documentation checked against the manual and API pages; the code was run headless in Blender 4.5.14.
