---
id: computing-software.computer-graphics-engineering.graphics-math.g-buffer-normal-encodings
name: g-buffer-normal-encodings
category: computing-software
field: computer-graphics-engineering
product: graphics-math
tags: [computer-graphics-engineering, graphics-math, interpolation-encoding, gbuffer-normal-encoding, octahedral-encoding, deferred-shading, normal-compression, render-targets]
level: practitioner
status: verified
description: "Pick a normal encoding for G-buffers: RGB10A2 xyz, octahedral, spheremap, view-space xy reconstruction pitfalls, precision vs bandwidth, blending and filtering behaviour."
sources: ["https://jcgt.org/published/0003/02/01/", "https://aras-p.info/texts/CompactNormalStorage.html", "https://knarkowicz.wordpress.com/2014/04/16/octahedron-normal-vector-encoding/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# G-buffer normal encodings compared

| Encoding | Storage | Error | Notes |
|---|---|---|---|
| xyz in RGB10A2 (`n*0.5+0.5`) | 30 bits | ~0.1 deg | Wastes precision (stores 3 values for 2 DOF), trivial decode, hardware blending works |
| xyz in RGBA8 | 24 bits | visible banding on smooth specular | Avoid for PBR |
| View-space xy, reconstruct z = sqrt(1-x²-y²) | 2 channels | Broken | z sign can be negative with perspective/normal maps; do not use |
| Spheremap (Lambert azimuthal) | 2 x 16 or 2 x 8 | Good | View-space only, singular at -z |
| **Octahedral** | 2 x 16 (RG16_SNORM/UNORM) or 2 x 12 | Excellent, uniform | Standard choice; world or view space |
| Stereographic | 2 channels | OK | Non-uniform precision |
| Oct + 10/10/2 or 11/11/10 packing | 32 bits with spare bits | Good | Pack extra flags/material id |

## Octahedral encode/decode
```hlsl
float2 octWrap(float2 v) { return (1.0 - abs(v.yx)) * (v.xy >= 0.0 ? 1.0 : -1.0); }
float2 encodeOct(float3 n) {
    n /= (abs(n.x) + abs(n.y) + abs(n.z));
    n.xy = n.z >= 0.0 ? n.xy : octWrap(n.xy);
    return n.xy * 0.5 + 0.5;
}
float3 decodeOct(float2 f) {
    f = f * 2.0 - 1.0;
    float3 n = float3(f.x, f.y, 1.0 - abs(f.x) - abs(f.y));
    float t = saturate(-n.z);
    n.xy += n.xy >= 0.0 ? -t : t;
    return normalize(n);
}
```
With SNORM targets skip the `*0.5+0.5`. Measured over random normals: 12+12 bits gives 0.021 degree average (0.059 max), 8+8 gives 0.34 average (0.95 max), 16+16 gives 0.0013 average; xyz in RGB10A2 gives 0.04 average (0.095 max) and RGBA8 xyz 0.17 average (0.38 max).

## Blending and filtering
Encoded normals cannot be hardware-blended (decals) or bilinearly filtered correctly: octahedral
wrap regions interpolate to garbage. Decals must read-modify-write (or use a separate decal buffer),
and upsampling passes must decode first.

## Precision checks
Smooth spheres with sharp GGX highlights reveal banding; test with roughness about 0.05 under a point
light.
