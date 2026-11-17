---
id: computing-software.computer-graphics-engineering.shader-programming.post-processing-chain-order
name: post-processing-chain-order
category: computing-software
field: computer-graphics-engineering
product: shader-programming
tags: [computer-graphics-engineering, shader-programming, post-processing-shaders, post-processing-order, post-processing, tonemapping, taa, bloom, colour-grading, render-pipeline]
level: advanced
status: draft
description: "Order a post-processing chain correctly: HDR vs LDR stages, where TAA, DoF, motion blur, bloom, exposure, tonemapping, grading, sharpening, grain and UI belong and why."
sources: ["https://docs.unrealengine.com/5.3/en-US/post-process-effects-in-unreal-engine/", "https://docs.unity3d.com/Packages/com.unity.render-pipelines.high-definition@17.0/manual/Post-Processing-Execution-Order.html", "https://www.iryoku.com/next-generation-post-processing-in-call-of-duty-advanced-warfare/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Ordering a post-processing chain

## 1. Reference order (scene-referred HDR first)
| # | Stage | Space | Why here |
|---|---|---|---|
| 1 | Opaque lighting, transparents, fog | linear HDR | produce scene radiance |
| 2 | TAA / upscaler (DLSS, FSR, XeSS) | linear HDR, pre-exposed | needs jittered input + motion vectors before any blur |
| 3 | Depth of field | linear HDR | physical blur of radiance; after TAA so it uses stable input (some engines do DoF before TAA at render res) |
| 4 | Motion blur | linear HDR | blur radiance along velocity |
| 5 | Bloom / lens flare | linear HDR | energy-based glow needs values > 1 |
| 6 | Exposure (auto-exposure applied) | linear HDR | scale before tonemap |
| 7 | Tonemapping + colour grading (LUT) | HDR -> display | one combined LUT in log/ACEScct space |
| 8 | Sharpening (CAS/RCAS) | display-referred | expects [0,1] |
| 9 | Chromatic aberration, vignette | display or HDR | stylistic; vignette often before tonemap |
| 10 | Film grain, dithering | display | last so it isn't blurred or sharpened |
| 11 | UI composite, sRGB/PQ encode | display | UI unaffected by grading |

Unity HDRP and Unreal document their exact orders; they match this shape.

## 2. Principles
- **Anything physical in HDR, anything perceptual after tonemap.**
- **Temporal before spatial blurs**: TAA must see unblurred, jittered pixels.
- **Combine fullscreen passes**: tonemap + grading LUT + vignette + grain + chromatic aberration in
  one "uber" post pass saves bandwidth; separate only where a blur/neighbourhood is required.
- **Pre-exposure**: multiply by last frame's exposure in the lighting pass so HDR values fit fp16
  and TAA history stays consistent.
- **Upscaler placement**: effects before the upscaler run at render res (cheaper); effects after run
  at display res. DoF/motion blur before, grain/sharpen after.

## Gotchas
- Bloom after tonemapping looks like a cheap glow and loses highlights.
- Applying grain before TAA turns into smeared noise.
- Separate tonemap and grading passes in 8-bit targets band; use one LUT pass from HDR.
- Motion vectors must be the un-jittered velocity; TAA jitter leaking into motion blur jitters edges.

## Verify
- [ ] RenderDoc/PIX event list shows passes in the documented order.
- [ ] Toggle each effect: no unexpected interaction (sharpen amplifying grain, bloom clipping).
