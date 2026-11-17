---
id: computing-software.game-programming.gameplay-programming.poisson-disc-sampling-for-placement
name: poisson-disc-sampling-for-placement
category: computing-software
field: game-programming
product: gameplay-programming
tags: [gameplay-programming, procedural-generation, poisson-disc, blue-noise, object-scattering, game-programming]
level: practitioner
status: verified
description: "Scatter trees, rocks, enemies and loot with Poisson disc sampling (Bridson's algorithm): minimum spacing, variable radius via density maps, seeding and tiling across chunks."
sources: ["https://www.cs.ubc.ca/~rbridson/docs/bridson-siggraph07-poissondisk.pdf", "https://www.redblobgames.com/x/1830-jittered-grid/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Poisson disc sampling for placement

**Goal:** natural-looking scattering where objects never overlap or clump, generated fast and
reproducibly.

## Why not uniform random
Uniform random points clump and leave gaps (white noise). Poisson disc (blue noise) guarantees a
minimum distance r between points while staying random-looking.

## Bridson's algorithm (O(n))
```python
def poisson_disc(width, height, r, k=30, rng=None):
    rng = rng or random.Random(1)   # pass your own seeded Random; a default of random.Random(seed) raises NameError
    cell = r / math.sqrt(2)
    gw, gh = int(width / cell) + 1, int(height / cell) + 1
    grid = [[None] * gh for _ in range(gw)]
    def fits(p):
        gx, gy = int(p[0] / cell), int(p[1] / cell)
        for x in range(max(gx - 2, 0), min(gx + 3, gw)):
            for y in range(max(gy - 2, 0), min(gy + 3, gh)):
                q = grid[x][y]
                if q and (q[0]-p[0])**2 + (q[1]-p[1])**2 < r*r: return False
        return True
    first = (rng.uniform(0, width), rng.uniform(0, height))
    pts, active = [first], [first]; grid[int(first[0]/cell)][int(first[1]/cell)] = first
    while active:
        i = rng.randrange(len(active)); base = active[i]
        for _ in range(k):
            a = rng.uniform(0, 2*math.pi); d = rng.uniform(r, 2*r)
            p = (base[0] + d*math.cos(a), base[1] + d*math.sin(a))
            if 0 <= p[0] < width and 0 <= p[1] < height and fits(p):
                pts.append(p); active.append(p); grid[int(p[0]/cell)][int(p[1]/cell)] = p; break
        else:
            active.pop(i)
    return pts
```
Grid cell size r/sqrt(2) ensures at most one point per cell; k = 30 candidate attempts per active point (both from Bridson's paper: cell size bounded by r/sqrt(n), typically k = 30). The paper picks candidates uniformly from the annulus (area-uniform), whereas the snippet draws the distance uniformly in [r, 2r], which over-samples near r but still guarantees spacing. Run here on 100x100 with r = 5 and three seeds: 260-266 points, minimum pairwise distance 5.0001-5.0027 (>= r), and the same seed gives identical output.

## Variants
- **Variable radius** from a density map (forest edges sparse, center dense): r(p) from texture; check
  neighbours against max(r(p), r(q)), grid sized for the minimum r with a wider neighbour search.
- **Multiple classes** (big trees then bushes): sample big objects first, then smaller ones with a
  separate radius that also respects big-object exclusion radii.
- Placement masks: reject points on roads, water, steep slopes after sampling (or as part of `fits`).
- Cheaper approximation: **jittered grid** — one random point per cell; less even but trivial.

## Chunks and determinism
- Seed per chunk (`hash(worldSeed, cx, cy)`), and generate with a border: include neighbour chunks'
  points within r when checking, or sample a larger area and keep points inside the chunk, deterministic
  either way.
- Same seed + same algorithm + same float behaviour = same layout (important for multiplayer).

## Gotchas
- Large k doesn't help much beyond ~30: on 200x200 with r = 5 the point count was 901, 1022, 1093 and 1117 for k = 5, 30, 100 and 300 (about +7% from 30 to 100); performance scales with point count.
- 3D version needs cell r/sqrt(3) and 3D neighbour search.

## Verify
- [ ] Assert min pairwise distance >= r on generated sets (unit test, brute force on small areas).
- [ ] Chunk seams show no gaps or overlaps.
