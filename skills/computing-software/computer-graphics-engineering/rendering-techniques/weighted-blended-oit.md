---
id: computing-software.computer-graphics-engineering.rendering-techniques.weighted-blended-oit
name: weighted-blended-oit
category: computing-software
field: computer-graphics-engineering
product: rendering-techniques
tags: [computer-graphics-engineering, rendering-techniques, transparency, alpha-blending, order-independent-transparency, oit, weighted-blended, accumulation-buffer, revealage, sorting-free]
level: advanced
status: docs-checked
description: "Render overlapping transparent surfaces without sorting using weighted blended order-independent transparency: accumulation and revealage targets, blend states."
sources: ["https://jcgt.org/published/0002/02/09/paper.pdf", "https://casual-effects.blogspot.com/2015/03/implemented-weighted-blended-order.html", "https://learnopengl.com/Guest-Articles/2020/OIT/Weighted-Blended"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Weighted blended order-independent transparency

**Goal:** many intersecting transparent layers (particles, glass, foliage cards, CAD
x-ray views) without per-object sorting artefacts, in one pass (McGuire & Bavoil 2013).

## 1. Targets
- **accum**: RGBA16F, cleared to (0,0,0,0) — weighted premultiplied colour sum + weighted alpha.
- **revealage**: R8 (or R16F), cleared to 1 — product of (1 − α).
Opaque depth buffer bound read-only (depth test on, depth write off).

## 2. Blend states
| target | src factor | dst factor |
|---|---|---|
| accum (RGBA) | ONE | ONE |
| revealage (R) | ZERO | ONE_MINUS_SRC_COLOR |
The two targets need different blend factors, so the API must support independent blend state per render target.

## 3. Transparent pass shader
```glsl
layout(location = 0) out vec4 accum;
layout(location = 1) out float reveal;
void main() {
    vec4 c = shade();                                     // premultiplied: c.rgb *= c.a
    float z = gl_FragCoord.z;                             // or view depth
    float w = clamp(pow(min(1.0, c.a * 10.0) + 0.01, 3.0) * 1e8 * pow(1.0 - z * 0.9, 3.0), 1e-2, 3e3);
    accum = vec4(c.rgb * w, c.a * w);
    reveal = c.a;                                         // blended as dst *= (1 - a)
}
```
The weight downweights very-low-coverage and distant surfaces; the paper and presentation describe several alternative weight functions best for different kinds of content. The one above is the general-purpose one from the casual-effects article.

## 4. Composite over opaque
```glsl
vec4 a = texelFetch(accumTex, p, 0); float r = texelFetch(revealTex, p, 0).r;
if (r == 1.0) discard;                                    // nothing transparent here
vec3 avg = a.rgb / max(a.a, 1e-5);
fragColor = vec4(avg, 1.0 - r);                           // blend: SRC_ALPHA, ONE_MINUS_SRC_ALPHA over opaque
```

## 5. Limits
- An approximation: ordering is guessed by weights — very different colours at similar alpha
  can look "averaged"; fully opaque-ish layers (α ≈ 1) are where it struggles most.
- No refraction or per-layer effects that need the exact layer below.
- Exact alternatives: per-pixel linked lists / k-buffers (memory-heavy), depth peeling (N
  passes), moment-based OIT (better approximation), or sorting + standard blending when object
  counts are small.

## Gotchas
- Shading must output **premultiplied** colour.
- Accum target is RGBA16F in the reference implementation; revealage is R8 (R16F gives slightly better precision at 2x the bandwidth).

## Checked
2026-11-01. Confirmed against the casual-effects article: target formats and clears, blend factors, weight function, composite step and blend, and that depth is tested but not written. Removed: the RTR4 section citation, the per-API support list, the MSAA advice, and the 8-bit overflow claim (not stated in the fetched pages).
Method: documentation only; no commands were run.

## Verify
- [ ] Intersecting transparent planes: no popping when the camera moves (vs sorted reference).
- [ ] Composite matches sorted blending within acceptable tolerance in test scenes.
- [ ] Bandwidth/time of the two targets measured at target resolution.
