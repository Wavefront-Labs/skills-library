---
id: computing-software.game-programming.unity.urp-asset-and-renderer-settings
name: urp-asset-and-renderer-settings
category: computing-software
field: game-programming
product: unity
tags: [unity, unity-urp, unity-render-pipeline, urp-asset, universal-renderer, quality-levels, forward-plus, render-scale, shadow-cascades, hdr, game-programming]
level: practitioner
status: draft
description: "Configure Unity URP for performance and quality: URP Asset per quality level, Universal Renderer (Forward/Forward+/Deferred), render scale, shadows, HDR and per-platform tiers."
sources: ["https://docs.unity3d.com/Packages/com.unity.render-pipelines.universal@17.0/manual/universalrp-asset.html", "https://docs.unity3d.com/Packages/com.unity.render-pipelines.universal@17.0/manual/urp-universal-renderer.html", "https://docs.unity3d.com/Manual/class-QualitySettings.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# URP Asset and renderer settings

**Goal:** a URP setup with explicit quality tiers so the same project hits frame rate on low-end
mobile and looks good on PC.

## Two assets, two roles
- **URP Asset** (pipeline asset): global quality knobs (render scale, HDR, MSAA, shadows, lights,
  additional features). Assign one per **Quality level** (Project Settings > Quality > Render Pipeline
  Asset) so Low/Medium/High switch pipeline settings at runtime with
  `QualitySettings.SetQualityLevel(i, true)`.
- **Universal Renderer Data**: rendering path, renderer features, layer filtering, depth/opaque
  texture needs. Referenced by URP Assets (several renderers allowed; cameras pick by index).

## Settings that matter most
| Setting | Guidance |
|---|---|
| Rendering Path | Forward (few lights per object, cheap), **Forward+** (many real-time lights, clustered, Unity 2022.2+), Deferred (many lights, no MSAA, more bandwidth: avoid on tile-based mobile GPUs). |
| Render Scale | <1.0 renders 3D at lower res, UI stays sharp. 0.7-0.85 on mobile; combine with FSR/STP upscaling filter. |
| HDR | Needed for bloom/tonemapping; costs bandwidth. HDR precision 32-bit (R11G11B10) on mobile. |
| Anti-aliasing | MSAA 2x/4x on mobile forward is cheap-ish; FXAA/SMAA/TAA per camera as post AA. |
| Depth Texture / Opaque Texture | Off unless a shader or effect needs them (soft particles, refraction): they add copies. |
| Main light shadows | Resolution 1024-2048, cascades 1-2 on mobile, 4 on PC; set Max Distance tight (e.g. 50 m), it matters more than resolution. |
| Additional lights | Per-object limit (Forward), shadows only when needed. |
| SRP Batcher | On (default). |

## Per-platform tiers
Create e.g. `URP-Mobile-Low`, `URP-Mobile-High`, `URP-PC`. Quality levels per platform in Project
Settings > Quality (the default quality per platform column). Expose quality options in settings
menus by switching Quality levels, not by editing the asset at runtime (asset edits persist in the
Editor and are shared).

## Camera stack
Base camera + Overlay cameras (e.g. weapon/UI) share the pipeline; each overlay costs. Prefer
rendering layers or one camera when possible on mobile.

## Verify
- [ ] Each quality level has its own URP Asset; switching at runtime changes shadows/render scale.
- [ ] Frame Debugger shows no unneeded CopyDepth/CopyColor passes.
- [ ] Profile on lowest target device: GPU time within budget at the Low tier.
