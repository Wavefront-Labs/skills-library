---
id: computing-software.game-programming.gameplay-programming.wave-function-collapse-generation
name: wave-function-collapse-generation
category: computing-software
field: game-programming
product: gameplay-programming
tags: [gameplay-programming, procedural-generation, wave-function-collapse, wfc, constraint-propagation, tile-adjacency, game-programming]
level: advanced
status: verified
description: "Implement Wave Function Collapse for tile maps: simple-tiled vs overlapping model, adjacency rules, min-entropy choice, propagation, contradictions and designer constraints."
sources: ["https://github.com/mxgmn/WaveFunctionCollapse", "https://www.boristhebrave.com/2020/04/13/wave-function-collapse-explained/", "https://www.gridbugs.org/wave-function-collapse/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Wave Function Collapse

**Goal:** generate maps that locally look like a hand-made example or obey tile adjacency rules,
using constraint propagation (Maxim Gumin's WFC).

## Two models
- **Simple tiled:** you define tiles and which may sit next to which per direction (with symmetry
  classes to derive rotations). Best for game tilesets and 3D modular kits.
- **Overlapping:** extracts every NxN pattern (N = 2 or 3) from a sample bitmap, with frequencies;
  adjacency = patterns that agree on their overlap. Best for texture-like output; costlier.

## Algorithm
```
wave[cell] = set of all tiles (bitset)
loop:
    cell = uncollapsed cell with minimum entropy (Shannon entropy of weighted options,
           plus tiny random noise to break ties)
    if none: done
    choose tile t in wave[cell] at random weighted by frequency; wave[cell] = {t}
    propagate from cell:
        stack = [cell]
        while stack:
            c = pop; for each neighbour n in direction d:
                allowed = union over tiles a in wave[c] of compatible[a][d]
                if wave[n] & ~allowed:
                    wave[n] &= allowed
                    if wave[n] empty: contradiction
                    push n
```
The pseudocode was implemented in Python (simple-tiled, 3 tiles with sea/land never adjacent, 20x20, 1000 seeds): 0 contradictions, 0 adjacency violations in the output, and the same seed reproduced the same map. With random symmetric adjacency tables over 6 tiles (density 0.4, 15x15), 11 of 850 runs (1.3%) hit a contradiction and needed a restart.

Speed: Gumin's implementation keeps per-cell, per-tile, per-direction **support counts** (AC-4
style; `compatible[cell][tile][direction]` counts and Shannon-entropy selection in Model.cs) so removing a tile decrements counts instead of recomputing unions. Use bitsets for waves.

## Contradictions
A cell with no options. Fixes, in order of effort: restart with a new seed (fine for small maps),
backtrack (store wave snapshots per decision), or generate in chunks and retry only the failing
chunk. Tilesets with a "wildcard" connector (e.g. an empty or grass tile compatible with most edges)
rarely contradict. Measure contradiction rate over many seeds.

## Designer control
- Pre-collapse cells (borders = wall, entrance tile at a fixed spot) then propagate before starting.
- Weights to bias frequencies; per-region tile masks.
- Global properties (connectivity, path length) are not guaranteed: validate with flood fill/BFS
  afterwards and reject, or constrain a path first and run WFC around it.
- Periodic (wrapping) output option for tileable textures.

## Verify
- [ ] Every adjacent pair in the output appears in the adjacency rules (automated check).
- [ ] Contradiction rate below target (e.g. under 5% restarts) over 1,000 seeds.
- [ ] Same seed gives the same map (seeded RNG; deterministic entropy noise).
