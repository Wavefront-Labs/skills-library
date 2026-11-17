---
id: computing-software.computer-graphics-engineering.gpu-optimisation.frame-generation-integration
name: frame-generation-integration
category: computing-software
field: computer-graphics-engineering
product: gpu-optimisation
tags: [computer-graphics-engineering, gpu-optimisation, frame-pacing, frame-generation, dlss-frame-generation, fsr-frame-generation, optical-flow, latency, ui-composition]
level: advanced
status: draft
description: "Integrate frame generation (DLSS Frame Generation, FSR Frame Generation): required inputs, UI handling, latency mitigation, pacing, and when generated frames hurt more than help."
sources: ["https://github.com/NVIDIAGameWorks/Streamline/blob/main/docs/ProgrammingGuideDLSS_G.md", "https://gpuopen.com/fidelityfx-super-resolution-3/", "https://github.com/GPUOpen-LibrariesAndSDKs/FidelityFX-SDK"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Frame generation (DLSS FG, FSR FG)

## 1. What it does
Interpolates an extra frame between two rendered frames using motion vectors (and optical flow on
NVIDIA), roughly doubling displayed frame rate. It increases smoothness, **not** responsiveness:
the next real frame must be rendered before the interpolated one is shown, adding latency.

## 2. Inputs
Same family as upscalers plus:
- Depth and motion vectors (camera + object), un-jittered or with jitter info.
- **HUD-less colour** (scene before UI) and final colour, or a UI buffer/alpha so UI isn't warped.
- Camera matrices, near/far, FOV, reset flags on camera cuts.
- Integration via Streamline (DLSS-G) or the FidelityFX SDK (FSR 3 frame generation, which can be
  combined with any upscaler or native AA).

## 3. UI handling
Interpolating UI creates warped, ghosted text. Options:
- Provide HUD-less colour and let the library composite the UI on both frames.
- Render UI in a separate callback/target the FG library composites (FSR's UI callback).

## 4. Latency and pacing
- Always pair with Reflex/Anti-Lag (required for DLSS FG certification).
- Base frame rate should be >= ~60 fps for good results; at 30 fps base, artefacts and latency are
  noticeable.
- Present pacing is handled by the library (its own swapchain proxy / pacing thread in FSR); don't
  add your own frame limiter on top without using the provided hooks.
- VRR displays work well; frame caps should be set below refresh accounting for doubled output.

## 5. Artefacts and mitigation
- Disocclusions and fast motion: interpolation errors around moving objects.
- Transparency and particles without motion vectors smear.
- Camera cuts: reset to avoid blending two shots.

## Gotchas
- Benchmark tools must report base and generated frame rates separately; frame-time graphs show
  the generated cadence.
- Some overlays/capture tools capture only real frames.

## Verify
- [ ] UI crisp in generated frames; no warped HUD.
- [ ] Latency with FG + Reflex comparable to native without Reflex.
