---
id: computing-software.computer-graphics-engineering.graphics-math.quaternion-compression-smallest-three
name: quaternion-compression-smallest-three
category: computing-software
field: computer-graphics-engineering
product: graphics-math
tags: [computer-graphics-engineering, graphics-math, interpolation-encoding, smallest-three, quaternion-compression, quantization, network-replication, animation-compression]
level: practitioner
status: verified
description: "Compress unit quaternions for networking and animation with smallest-three: drop the largest component, quantise the rest in [-1/sqrt2, 1/sqrt2], sign handling and error budgets."
sources: ["https://gafferongames.com/post/snapshot_compression/", "https://www.gdcvault.com/play/1026173/", "https://github.com/nfrechette/acl"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Quaternion compression (smallest three)

A unit quaternion has 3 degrees of freedom. Drop the component with the largest magnitude (it can be
reconstructed from `w = sqrt(1 - a^2 - b^2 - c^2)`), store its index (2 bits) and the other three.

## Why it works
If x is the largest, each of the others satisfies `|c| <= 1/sqrt(2)` (about 0.7071), so quantising
range [-0.7071, 0.7071] instead of [-1, 1] gains about 0.5 bit of precision per component.

## Encode/decode (2 + 3 x 10 bits = 32 bits)
```cpp
uint32_t encode(quat q) {                        // q normalised, components as float[4]
    int big = 0; for (int i = 1; i < 4; ++i) if (fabsf(q[i]) > fabsf(q[big])) big = i;
    float s = q[big] < 0 ? -1.0f : 1.0f;         // q and -q are the same rotation: make dropped one positive
    uint32_t r = big; const float k = 1.0f / 0.70710678f;
    for (int i = 0; i < 4; ++i) if (i != big) {
        float v = (q[i] * s * k) * 0.5f + 0.5f;  // [0,1]
        r = (r << 10) | (uint32_t)lroundf(std::clamp(v, 0.0f, 1.0f) * 1023.0f);
    }
    return r;
}
// decode: read three 10-bit values (in reverse order), map back to [-0.7071, 0.7071],
// dropped = sqrt(max(0, 1 - a*a - b*b - c*c)), place at index 'big', then normalise
```
Choose bits by error budget: measured max angular error over 3e5 random rotations: 9 bits 0.48 degrees, 10 bits 0.23, 15 bits 0.007, 16 bits 0.004; use 15 to 16 bits for animation bones near the root where error propagates down the chain.

## Use cases
- Network snapshots (Glenn Fiedler's snapshot compression): 29 to 32 bits per orientation.
- Animation clips: per-track quantisation with range reduction (ACL uses variable bit rates per track
  and clip ranges).

## Alternatives
- Octahedral/hemi-octahedral mapping of the rotation axis plus angle.
- Logarithm map (3 values) when interpolating compressed data.

## Verify
Encode/decode random unit quaternions: max angular error `2 acos(|dot(q, q')|)` within the budget for
your bit count; test near-axis quaternions (one component about 1).
