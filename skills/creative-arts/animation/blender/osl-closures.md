---
id: creative-arts.animation.blender.osl-closures
name: osl-closures
category: creative-arts
field: animation
product: blender
tags: [blender, osl-closures, closure, osl, bsdf, script-node, cycles]
level: advanced
status: docs-checked
description: "Output shading closures from OSL in Cycles: closure color outputs, the Cycles closure list (diffuse, microfacet, refraction, emission, volume) and mixing closures."
sources:
  - https://docs.blender.org/manual/en/latest/render/cycles/osl/index.html
  - https://open-shading-language.readthedocs.io/en/main/stdlib.html#material-closures
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---

# osl-closures

Goal: write a whole BSDF in OSL, not just a texture pattern.

## Output a closure

```c
shader plastic(color Base = color(0.8, 0.1, 0.1), float Roughness = 0.3, float IOR = 1.5,
               normal Normal = N, output closure color BSDF = 0)
{
    float f = 0.04;                                    // simple constant specular weight
    closure color spec = microfacet_ggx(Normal, Roughness);
    BSDF = (1.0 - f) * Base * diffuse(Normal) + f * spec;
}
```
Connect `BSDF` (a shader socket) to Material Output, Surface.

OSL has no light loop and no access to scene lights: the material must be built from closures implemented in the renderer. The Cycles closures correspond to the shader nodes and their sockets (see the shader nodes manual for what the parameters mean).

## Closures available in Cycles (5.2 manual)

| Group | Closures |
|---|---|
| BSDF | `diffuse(N)`, `oren_nayar(N, roughness)`, `diffuse_ramp(N, colors[8])`, `phong_ramp(N, exponent, colors[8])`, `diffuse_toon(N, size, smooth)`, `glossy_toon(N, size, smooth)`, `translucent(N)`, `reflection(N)`, `refraction(N, ior)`, `transparent()` |
| Microfacet | `microfacet_ggx(N, roughness)`, `microfacet_ggx_aniso(N, T, ax, ay)`, `microfacet_ggx_refraction(N, roughness, ior)`, and the `microfacet_beckmann` equivalents; `ashikhmin_shirley(N, T, ax, ay)`, `ashikhmin_velvet(N, roughness)` |
| Hair | `hair_reflection`, `hair_transmission`, `principled_hair` |
| BSSRDF | `bssrdf(method, N, radius, albedo)` with methods `burley`, `random_walk_skin`, `random_walk` |
| Volume | `henyey_greenstein(g)`, `absorption()` |
| Other | `emission()`, `ambient_occlusion()`, `holdout()`, `background()` |

Use the exact names above (for example `microfacet_ggx`, not a generic `microfacet(...)` call) and confirm in the manual for your release.

## Mixing

Closures are added and scaled by colours/floats: `BSDF = mix_weight * a + (1 - mix_weight) * b`. Keep weights within energy limits; sums above 1 brighten unrealistically.

## Gotchas

- Closures are combined, not inspected: compute weights from data first (see the OSL standard library documentation).
- Volume closures go to Material Output, Volume.
- Where the OSL documentation and the Cycles manual differ, the Cycles list above is what Cycles implements.

## Verify

Render a sphere under an HDRI: diffuse base plus a glossy highlight that sharpens as Roughness lowers.

## Checked

2026-10-27 against the Blender 5.2 manual, Cycles > Open Shading Language page (Closures section). Corrected: the generic `microfacet("ggx", ...)` form is not in the Cycles list (use `microfacet_ggx` etc.), `oren_nayar` and `ashikhmin_velvet` take `roughness`. Removed unconfirmed claims (MaterialX-style closures, roughness-squared convention). Method: documentation only; no commands were run.
