---
id: computing-software.computer-graphics-engineering.rendering-techniques.specular-antialiasing
name: specular-antialiasing
category: computing-software
field: computer-graphics-engineering
product: rendering-techniques
tags: [computer-graphics-engineering, rendering-techniques, antialiasing, specular-aliasing, toksvig, normal-map-filtering]
level: advanced
status: docs-checked
description: "Reduce specular aliasing on normal-mapped surfaces: Toksvig factor from averaged normals, baked Toksvig and CLEAN maps, LEAN cost, roughness clamping."
sources: ["https://google.github.io/filament/Filament.md.html#materialsystem/specularaliasing", "https://blog.selfshadow.com/2011/07/22/specular-showdown/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Specular antialiasing

**Problem:** sharp highlights on normal-mapped surfaces shimmer when the normal varies faster
than a pixel. Techniques below estimate normal variance and widen the highlight to match
(sources: Filament docs, Stephen Hill's "Specular Showdown in the Wild West", 2011).

## 1. Toksvig AA
Toksvig (2004) estimates bump variance from the length of the averaged (mip-filtered) normal Na
in an existing normal map; hardware MIP filtering does the averaging. For Blinn-Phong with
exponent s the Toksvig factor is f_t = |Na| / (|Na| + s(1 - |Na|)) and the exponent becomes f_t * s.
In code (HLSL):
```hlsl
float len   = length(Na);
float ft    = len / lerp(s, 1, len);
float scale = (1 + ft * s) / (1 + s);
float spec  = scale * pow(saturate(dot(Na, H)) / len, ft * s);
```
The blog argues the leading energy term looks wrong and the 1s should really be 2s; treating
Blinn-Phong as an NDF, use `(p + 2) / 8 * pow(N.H, p)` with N = Na / |Na| and p = f_t * s.
The original paper used a 2D LUT; direct evaluation in the shader avoids a LUT per exponent.

## 2. Bake it offline
Pre-compute Toksvig factors from a Gaussian-filtered version of each mip level into an
auto-generated anti-aliasing gloss map. Unlike LEAN terms it compresses well, and high precision
normals can be used in the import pipeline before compressing. A map is baked for a particular
specular power (the blog suggests around 100 gives reasonable contrast); convert to other
powers later. Alternatives: store the adjusted power as a log-space exponent of a maximum
power (Naty Hoffman), or store variance or normal length and finish the maths at runtime.

## 3. LEAN and CLEAN
- **LEAN mapping** filters highlights robustly across scales, produces anisotropic highlights
  from ridged normal maps and can combine layers of dynamic bumps, but cannot use DXT1 or DXT5
  normal maps and could cost at least 8 times the storage; deferred G-buffers and the extra
  tangent vector and maths make it harder still.
- Toksvig lacks anisotropy: it can over-broaden or under-damp. **CLEAN** baking reduces remaining
  shimmer at the cost of slightly more highlight blooming. The practical difference is the
  variance measure: sigma^2 = (1 - |Na|) / |Na| for Toksvig, M_z - (M_x^2 + M_y^2) for CLEAN,
  with p = s / (1 + s * sigma^2).
- Baked Toksvig or CLEAN is still described as much better than doing nothing.

## 4. Roughness clamping
Filament clamps roughness to a safe range in the shader (never 0), which also corrects some
aliasing at low roughness. Its note: the Frostbite engine clamps analytical-light roughness to
0.045 to reduce specular aliasing, possible in fp32.

## Gotchas
- Maps baked for one specular power need converting if the material exponent changes.
- Toksvig and CLEAN assume the Blinn-Phong exponent parameterisation; convert from GGX roughness
  carefully.

## Verify
- [ ] Moving camera over a normal-mapped glossy floor: no sparkle at distance.

## Checked

Method: docs-checked 2026-11-09 against the Specular Showdown blog post (Toksvig, baking, LEAN and CLEAN sections read) and the Filament roughness clamping note. Dropped the geometric specular AA (Kaplanyan, Tokuyoshi) shader and its constants because the JCGT paper was unreadable and Filament's page has no such section, and dropped the Unreal and Filament compositing-into-roughness claim.
