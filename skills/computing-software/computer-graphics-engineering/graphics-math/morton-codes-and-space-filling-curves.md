---
id: computing-software.computer-graphics-engineering.graphics-math.morton-codes-and-space-filling-curves
name: morton-codes-and-space-filling-curves
category: computing-software
field: computer-graphics-engineering
product: graphics-math
tags: [computer-graphics-engineering, graphics-math, interpolation-encoding, morton-code, space-filling-curve, z-order, hilbert-curve, lbvh]
level: practitioner
status: verified
description: "Encode Morton (Z-order) codes with bit interleaving and magic numbers or pdep, Hilbert curve alternatives, and uses in LBVH builds, texture swizzling and spatial sorting."
sources: ["https://fgiesen.wordpress.com/2009/12/13/decoding-morton-codes/", "https://developer.nvidia.com/blog/thinking-parallel-part-iii-tree-construction-gpu/", "https://en.wikipedia.org/wiki/Z-order_curve"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Morton codes and space-filling curves

A Morton code interleaves the bits of integer coordinates: points close in space tend to be close in
the 1D order, so sorting by code clusters data spatially.

## 3D, 10 bits per axis -> 30-bit code
```cpp
uint32_t part1By2(uint32_t x) {                 // spread 10 bits: x -> --x--x--x...
    x &= 0x000003ff;
    x = (x ^ (x << 16)) & 0xff0000ff;
    x = (x ^ (x <<  8)) & 0x0300f00f;
    x = (x ^ (x <<  4)) & 0x030c30c3;
    x = (x ^ (x <<  2)) & 0x09249249;
    return x;
}
uint32_t morton3D(uint32_t x, uint32_t y, uint32_t z) {
    return (part1By2(z) << 2) | (part1By2(y) << 1) | part1By2(x);
}
```
- 21 bits per axis fit in a 64-bit code. On x86 with BMI2: `_pdep_u64(x, 0x9249249249249249)`.
- Quantise float positions first: `q = (uint)clamp((p - boundsMin) / extent * 1024, 0, 1023)`.
- Decoding uses the inverse compaction (`compact1By2`).

## Uses
- **LBVH**: sort primitives by Morton code of centroids, build the hierarchy from common prefix
  lengths in parallel (Karras 2012); duplicate codes need tie-breaking by index.
- **GPU texture swizzling**: tiled/Z-order layouts make 2D neighbourhoods cache-friendly.
- **Spatial sorting** of particles/points for cache locality, octree construction (prefix = node),
  hashing.

## Hilbert curve
Better locality (no long jumps between quadrants), costlier to compute. Use for out-of-core layout,
database indexing, and when locality quality matters more than encode speed.

## Gotchas
- Order of axis interleaving must be consistent between encoder and consumer.
- Morton order has big jumps at power-of-two boundaries: neighbours across those boundaries are far
  apart in the order.

## Verify
(Computed: `part1By2` matches a naive bit loop for all 1024 inputs; a software PDEP with mask 0x9249249249249249 spreads a 21-bit value to bits 0,3,...,60 as expected.)
Encode-decode round trip for all 2^30 values (or random sample); compare with a naive bit loop.
