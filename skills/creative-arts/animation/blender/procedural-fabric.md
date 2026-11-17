---
id: creative-arts.animation.blender.procedural-fabric
name: procedural-fabric
category: creative-arts
field: animation
product: blender
tags: [blender, procedural-texturing, procedural-fabric, weave, cloth-shader, sheen]
level: practitioner
status: docs-checked
description: "Build procedural woven fabric in Blender: warp and weft from Wave Texture bands, thread bump, Principled sheen and fuzz for cloth close-ups."
sources:
  - https://docs.blender.org/manual/en/latest/render/shader_nodes/textures/wave.html
  - https://docs.blender.org/manual/en/latest/render/shader_nodes/shader/principled.html
  - https://docs.blender.org/manual/en/latest/render/shader_nodes/textures/noise.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# procedural-fabric

## Plain weave pattern

1. Multiply UV coordinates by the thread count so one UV unit holds many threads.
2. Warp threads: a Wave Texture with Type *Bands*, Bands Direction X, Wave Profile *Sine*. Weft threads: a second Wave Texture with Bands Direction Y, Sine. (The Wave *Factor* output is the intensity.)
3. Over/under alternation: a checker pattern with the same frequency as the thread count decides which thread set is on top; use it as the factor of a Mix between the warp and weft heights.
4. Feed the height into a Bump node for thread relief and into a Color Ramp for a colour per thread set (two-tone fabrics).
5. Twill: shift the alternation by one thread each row so the ribs run diagonally. (*Bands* also has a *Diagonal* direction option on the Wave Texture.)

## Material

The Principled BSDF has a **Sheen** layer which, per the manual, simulates very small fibres on the surface: for cloth it adds a soft velvet-like reflection near edges, and it can also simulate dust. *Weight* is the intensity, *Roughness* the roughness of the sheen reflection and *Tint* its colour. The base *Roughness* runs from 0.0 (perfectly sharp reflection) to 1.0 (diffuse), and *Alpha* (1.0 fully opaque) can come from a thread-gap mask for loose weaves.

## Fuzz

A Noise Texture at very high scale into a bump at low strength, or real curve hair fibres for hero close-ups.

## Gotchas

- Thread frequency beyond pixel resolution aliases (moire): fade the weave detail with distance.
- UV stretching distorts the weave, so cloth needs clean, undistorted UVs.

## Verify

A close-up render shows over/under threads; a mid-shot shows no moire.

## Checked

2026-11-09. Confirmed against the Blender manual Wave Texture node page (read in full), Principled BSDF page (Sheen, Roughness and Alpha lines, grep read) and Noise Texture page (read in full). Removed: all numeric values (thread count, roughness, sheen and bump figures), the Translucent mix, the Checker Scale / Brick Offset / Camera Data View Distance node recipes (pages not read), and the claim that slight subsurface suits thin cloth.
Method: documentation only; no commands were run.
