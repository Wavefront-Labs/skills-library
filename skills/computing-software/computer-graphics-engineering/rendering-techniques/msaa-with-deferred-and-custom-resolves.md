---
id: computing-software.computer-graphics-engineering.rendering-techniques.msaa-with-deferred-and-custom-resolves
name: msaa-with-deferred-and-custom-resolves
category: computing-software
field: computer-graphics-engineering
product: rendering-techniques
tags: [computer-graphics-engineering, rendering-techniques, antialiasing, custom-resolve, msaa, deferred-shading, per-sample-shading, edge-detection, tonemapped-resolve]
level: advanced
status: draft
description: "Use MSAA with deferred shading and custom resolves: edge detection to shade per-sample only at edges, multisampled G-buffers, tonemap-aware resolves, and depth resolve choices."
sources: ["https://therealmjp.github.io/posts/msaa-overview/", "https://www.intel.com/content/www/us/en/developer/articles/technical/deferred-rendering-for-current-and-future-rendering-pipelines.html", "https://mynameismjp.wordpress.com/2012/10/24/msaa-overview/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# MSAA with deferred and custom resolves

## 1. Why it's hard
MSAA stores N samples per pixel but runs the pixel shader once; resolving a G-buffer (averaging
normals, depth) before lighting is wrong. Deferred lighting must happen per sample, which costs N x
unless you restrict it to edges.

## 2. Multisampled G-buffer + edge classification
1. Render the G-buffer into MSAA targets (`sampler2DMS` / `Texture2DMS`).
2. Classify pixels: compare samples' depth/normal/material ID; if all equal, it's an interior
   pixel; otherwise an edge (typically 5-15% of pixels).
3. Lighting: interior pixels shade sample 0 once; edge pixels shade every sample (compute shader
   with a per-tile list of edge pixels, or stencil-masked per-sample pass with `gl_SampleID` /
   `SV_SampleIndex`).
4. Write per-sample lit colour, then resolve.

## 3. Custom (tonemap-aware) resolve
The hardware resolve averages linear HDR values; a very bright sample dominates and edges alias
again after tonemapping. Better:
```glsl
vec3 sum = vec3(0); float wsum = 0.0;
for (int s = 0; s < N; s++) {
    vec3 c = texelFetch(hdrMS, p, s).rgb;
    float w = 1.0 / (1.0 + luminance(c) * exposure);   // Karis/Reinhard weight
    sum += c * w; wsum += w;
}
vec3 resolved = sum / wsum;
```
Or tonemap each sample, average, and inverse-tonemap. MJP's MSAA overview also covers wider
reconstruction filters (B-spline, Blackman-Harris) across neighbouring pixels.

## 4. Depth resolve
For post effects needing depth, choose sample 0, min, or max depth (Vulkan
`VK_RESOLVE_MODE_MIN_BIT` via `VkSubpassDescriptionDepthStencilResolve`; D3D12 doesn't resolve depth,
do it in a shader). Max/min depends on what the consumer needs (SSAO usually nearest).

## 5. Alternatives
Forward+ with MSAA is simpler; deferred with TAA is the industry default. Use MSAA+deferred where
TAA blur is unacceptable (VR, CAD-like content).

## Gotchas
- Per-sample shading triggered accidentally (reading `gl_SampleID` in the main pass) multiplies cost.
- MSAA G-buffers are huge (4x targets); bandwidth and memory may be prohibitive.

## Verify
- [ ] Edge mask debug view shows only geometric edges.
- [ ] Bright-highlight edges remain anti-aliased after tonemapping.
