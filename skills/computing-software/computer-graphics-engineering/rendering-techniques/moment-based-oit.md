---
id: computing-software.computer-graphics-engineering.rendering-techniques.moment-based-oit
name: moment-based-oit
category: computing-software
field: computer-graphics-engineering
product: rendering-techniques
tags: [computer-graphics-engineering, rendering-techniques, transparency, moment-based-oit, order-independent-transparency, transmittance, wboit, power-moments]
level: advanced
status: draft
description: "Approximate OIT with moment-based OIT: generating power moments of optical depth, reconstructing transmittance per fragment, and precision settings."
sources: ["https://momentsingraphics.de/I3D2018.html", "https://jcgt.org/published/0007/02/02/", "https://casual-effects.blogspot.com/2014/03/weighted-blended-order-independent.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Moment-based OIT (MBOIT)

Munstermann, Krumpen, Klein, Peters (I3D 2018). Two geometry passes over transparent surfaces,
no per-pixel lists, much more accurate than weighted blended OIT.

## 1. Idea
Transmittance at depth z is `T(z) = exp(-sum of optical depths of surfaces in front)`. MBOIT stores
a few **moments** of the distribution of absorbance over depth per pixel, then reconstructs an
approximate `T(z)` for any fragment depth.

## 2. Passes
1. **Moment generation pass**: for each transparent fragment with alpha a, compute
   `absorbance = -log(1 - a)` and add `absorbance * (1, z, z^2, z^3)` (4 power moments) plus the
   total absorbance `b0` into float render targets with additive blending. Depth warped to [-1,1]
   (log depth helps).
2. **Resolve/shading pass**: render transparent geometry again; per fragment reconstruct the
   transmittance in front of its depth from the moments (Hamburger 4-moment reconstruction, a small
   closed-form solve), and accumulate `color * a * T_front(z)` additively plus total weight.
3. **Composite**: normalise and blend with the opaque background using total transmittance
   `exp(-b0)`.

## 3. Settings
- 4 power moments in RGBA32F (or 16-bit with trigonometric moments and careful bias) + b0 in
  R32F. 6/8 moment variants improve accuracy.
- A small bias (e.g. 5e-5 for 32-bit, larger for 16-bit) stabilises reconstruction.
- Accuracy degrades with many layers of similar depth and high alpha; fine for smoke, glass, foliage
  mixes.

## 4. Comparison
| Method | Passes | Memory | Accuracy |
|---|---|---|---|
| Sorted blending | 1 | none | exact if sortable |
| Weighted blended OIT | 1 + composite | 2 targets | heuristic weights, colour bleeding |
| MBOIT | 2 + composite | 2-3 targets | good, slight light leaking |
| Linked lists | 1 + resolve | unbounded | exact (up to cap) |

## Gotchas
- 16-bit moment targets need the trigonometric variant or quantisation; plain power moments in fp16
  break down.
- Alpha = 1 gives infinite absorbance; clamp alpha to < 1 (e.g. 0.9999).

## Verify
- [ ] Compare with a sorted reference on layered test scenes; error acceptable.
- [ ] No negative or > 1 transmittance (clamp checks).
