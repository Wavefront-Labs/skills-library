---
id: computing-software.computer-graphics-engineering.rendering-techniques.deferred-vs-forward-rendering
name: deferred-vs-forward-rendering
category: computing-software
field: computer-graphics-engineering
product: rendering-techniques
tags: [rendering-techniques, deferred-rendering, forward-rendering, forward-plus, g-buffer, transparency, msaa, many-lights, bandwidth, overdraw, mobile-rendering, render-architecture]
level: advanced
status: draft
description: "Choose and implement deferred vs forward (and Forward+) rendering: G-buffer layout, many-light handling, the transparency/MSAA problems deferred has, and when each wins."
sources: ["https://www.realtimerendering.com/", "https://www.3dgep.com/forward-plus/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Deferred vs forward rendering

**Goal:** pick a render architecture based on actual light count and platform
constraints, not fashion — both have real, structural weaknesses the other
doesn't.

## Forward rendering
Shade each object immediately as it's drawn, looping over all relevant lights
per fragment. Simple, works naturally with MSAA and transparency (blending
happens inline, in draw order).
- Cost scales with **lights × fragments** per object if done naively — many
  dynamic lights means either a per-object light list (the engine decides which
  lights affect which object, culled on CPU) or a long per-pixel loop that wastes
  work on lights that don't actually touch that pixel.
- **Forward+ / tiled forward**: compute-shader light culling per screen tile
  (bin lights into a per-tile list based on tile depth bounds) before the forward
  pass, so each fragment only loops over the lights actually relevant to its
  tile — gets most of deferred's many-light scalability while keeping forward's
  easy MSAA/transparency. The modern default for "forward but with lots of lights."

## Deferred rendering
Split into two passes: (1) render all opaque geometry into a **G-buffer**
(albedo, normal, roughness/metallic, depth — typically 3-4 RGBA8/16F targets),
(2) a full-screen lighting pass reads the G-buffer and accumulates lighting per
light, per pixel, without re-rasterising geometry.
- Cost scales with **lights × screen pixels**, independent of scene geometric
  complexity — the classic win for scenes with many dynamic lights and lots of
  overlapping geometry (overdraw doesn't multiply shading cost the way forward's does).
- **G-buffer bandwidth is the new bottleneck**: writing and reading back 3-4
  full-screen targets every frame costs real memory bandwidth — at high
  resolution/high refresh this can dominate over the actual lighting math. Packing
  (octahedral-encoded normals into 2 channels, shared exponent encodings) reduces this.
- **Transparency doesn't fit the model**: a G-buffer stores one surface per
  pixel — there's no slot for "what's behind the transparent surface." Standard
  fix: render transparents in a **separate forward pass** after the deferred
  opaque+lighting result, composited on top; loses deferred's many-light benefit
  for just the transparent objects (usually acceptable — transparents are
  typically a minority of scene pixels).
- **MSAA is expensive**: G-buffer MSAA multiplies every G-buffer target's memory
  and bandwidth by the sample count; most engines instead use a post-process
  anti-aliasing technique (TAA) with deferred rather than true G-buffer MSAA.
- **Material variety is constrained**: every pixel runs the same lighting pass
  shader — exotic per-material BRDFs need a material-ID buffer and branching
  (or multiple lighting passes), unlike forward where each object's shader can
  differ freely.

## Picking one
- Few lights, need MSAA/varied materials/transparency-heavy scenes, or mobile
  bandwidth-constrained targets: forward (or Forward+ if light count grows).
  Mobile tile-based GPUs in particular favour forward — deferred's G-buffer
  read-back can defeat tile memory optimisations the hardware is built around.
- Many dynamic lights, opaque-dominated scenes, desktop/console bandwidth
  budget: deferred (or a hybrid: deferred for opaque + forward for transparents,
  which is what most shipped AAA engines actually do).

## Verify
- [ ] Light count and overdraw profiled on the actual target scene before
      picking an architecture, not decided from a tutorial's recommendation.
- [ ] G-buffer bandwidth measured (bytes/pixel × targets × resolution) against the
      target platform's available bandwidth before committing to deferred.
- [ ] Transparency handling explicitly designed (separate forward pass) if using
      deferred — not discovered as a gap after the opaque pipeline is built.
- [ ] Mobile/tile-based target explicitly benchmarked for deferred's G-buffer
      pattern before assuming desktop results transfer.
