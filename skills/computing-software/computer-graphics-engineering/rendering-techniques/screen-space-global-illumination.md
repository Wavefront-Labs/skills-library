---
id: computing-software.computer-graphics-engineering.rendering-techniques.screen-space-global-illumination
name: screen-space-global-illumination
category: computing-software
field: computer-graphics-engineering
product: rendering-techniques
tags: [computer-graphics-engineering, rendering-techniques, global-illumination, ssgi, screen-space-gi, visibility-bitmask, gtao, denoising, ray-marching]
level: advanced
status: docs-checked
description: "Add screen-space GI: horizon-based and visibility-bitmask methods, ray-marched SSGI as in Unity HDRP, thin-surface artefacts and offscreen limits."
sources: ["https://arxiv.org/abs/2301.11376", "https://docs.unity3d.com/Packages/com.unity.render-pipelines.high-definition@17.0/manual/Override-Screen-Space-GI.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Screen-space global illumination (SSGI)

## 1. Idea
Use the screen's depth and colour buffers as the scene to compute diffuse light bounces
(Unity HDRP describes its SSGI override exactly this way).

## 2. Algorithms
- **Ray-marched SSGI**: HDRP offers Ray Marching (screen space), Ray Tracing, or Mixed. Mixed
  ray-marches on-screen geometry and ray-traces off-screen geometry; it needs Performance mode
  and Lit Shader Mode set to Deferred, and works from the GBuffer, so forward-rendered transparent
  objects do not appear in it.
- **Horizon-based (GTAO/HBIL-style)**: generates hemisphere slices and takes a fixed number of
  samples per slice to find horizon angles. They assume the depth buffer is a height field, i.e.
  infinite surface thickness, which causes haloing and cannot let light pass behind thin surfaces.
- **Visibility bitmask (Therrien, Levesque, Gilet, "Screen Space Indirect Lighting with Visibility
  Bitmask")**: replaces the two horizon angles with a bit field of Nb sectors distributed uniformly
  around the hemisphere slice, each recording occluded or un-occluded. Each depth sample is treated as
  local thin geometry of constant thickness t, so light can pass behind surfaces. All occluded sectors are
  set at once, so cost is O(1) in the sector count. One pass yields both ambient occlusion and indirect
  lighting. The thickness t strongly affects fidelity; a fixed world-space t over-attenuates
  occlusion on distant objects, so the paper offers growing t linearly with distance.

## 3. Fallbacks and engine behaviour
Screen space cannot see offscreen or hidden sources. In HDRP, SSGI and RTGI replace all lightmap and
Light Probe data: with the override on a Volume affecting the Camera, Light Probes and the ambient
probe stop contributing to lighting, and SSGI is not compatible with Reflection Probes. Plan
any hybrid with probes accordingly (or use the Mixed mode for offscreen hits).

## Gotchas
- Depth buffers have no thickness: horizon methods assume infinite thickness; use a thickness
  heuristic or the visibility bitmask.
- HDRP Mixed tracing needs deferred geometry; forward-rendered transparents are absent.

## Verify
- [ ] Colour bleeding visible near bright coloured walls; no haloing around foreground objects.
- [ ] Probe/lightmap contribution behaviour matches the engine mode you chose.

## Checked
Method: docs-checked 2026-11-09 against the full text of arXiv 2301.11376 (abstract, introduction, algorithm section; downloaded PDF) and the Unity HDRP 17.0 Screen Space Global Illumination manual page. Removed unconfirmed pipeline steps (half-res, blue noise, a-trous), the 32-bit sector claim and the Activision source (download failed).
