---
id: computing-software.computer-graphics-engineering.rendering-techniques.integrating-dlss-fsr-upscalers
name: integrating-dlss-fsr-upscalers
category: computing-software
field: computer-graphics-engineering
product: rendering-techniques
tags: [computer-graphics-engineering, rendering-techniques, antialiasing, upscaler-integration, reactive-mask, dlss, fsr, xess, temporal-upscaling, motion-vectors]
level: advanced
status: gated
description: "Integrate DLSS, FSR or XeSS: required inputs (jittered colour, depth, motion vectors, exposure), negative mip bias, reactive/transparency masks, resets, and pipeline placement."
sources: ["https://github.com/GPUOpen-LibrariesAndSDKs/FidelityFX-SDK/blob/main/Kits/FidelityFX/docs/techniques/super-resolution-upscaler.md", "https://github.com/NVIDIA-RTX/Streamline/blob/main/docs/ProgrammingGuideDLSS.md", "https://github.com/intel/xess"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Integrating DLSS / FSR / XeSS

## 1. Inputs (similar across upscalers; the FSR column is from the FidelityFX documentation)
| Input | Notes |
|---|---|
| Colour (render res, jittered) | FSR: every render-resolution input except motion vectors is rendered with jitter; HDR input needs `FFX_UPSCALE_ENABLE_HIGH_DYNAMIC_RANGE` |
| Depth (render res) | FSR strongly recommends an inverted, infinite depth buffer and takes a flag (`FFX_UPSCALE_ENABLE_DEPTH_INVERTED`) for its configuration |
| Motion vectors | FSR: not jittered unless the jitter-cancellation flag is set. Streamline/DLSS: scale to the expected range with `mvecScale` ({1,1} for [-1,1], {1/renderWidth, 1/renderHeight} for pixel-space vectors) |
| Jitter offset | in pixels (Streamline troubleshooting and the FSR jitter helpers both use pixel units); do not bake jitter into matrices passed to Streamline |
| Exposure | FSR: optional 1x1 R32_FLOAT texture, or the auto-exposure flag. Streamline/DLSS: exposure tag, or `useAutoExposure` |
| Reactive mask (FSR) | per-pixel [0, 1] "trust the current frame" for alpha-blended objects; write the blend alpha and clamp to about 0.9 |
| Transparency & composition mask (FSR) | R8_UNORM; for areas without matching motion vectors (reflections, animated textures); softer than the reactive mask |
| DLSS bias-current-colour mask | (gated: unconfirmed, source is paywalled or blocked) |
| Reset flag | on camera jump cuts the history should be cleared (documented for FSR; for DLSS see its programming guide, (gated: unconfirmed, source is paywalled or blocked)) |

Streamline wraps NVIDIA features (DLSS, DLSS frame generation, Reflex and others have programming guides in its repository), the FidelityFX
API wraps FSR, and Intel ships the XeSS SDK; they are separate APIs, not one unified interface.

## 2. Pipeline placement
Opaques -> transparents -> upscaler -> post -> UI. The FSR documentation puts screen-space reflections, SSAO, denoisers and (optionally)
exposure before the upscaler, and film grain, chromatic aberration, vignette, tonemapping, bloom, depth of field and motion blur after it;
it calls this guidance that depends on your implementation.

## 3. Mip bias
FSR documentation: `mipBias = log2(renderResolution / displayResolution) - 1.0` (for example -1.58 at 1.5x, -2.0 at 2x, -2.58 at 3x
per dimension); it also suggests adjusting bias for specific high-frequency textures. DLSS and XeSS bias guidance (gated: unconfirmed, source is paywalled or blocked).
Recreate samplers when the ratio changes.

## 4. Motion vectors for everything
- Skinned meshes, vertex-animated foliage, particles and UV-scrolling materials need correct motion
  (previous-frame positions) or they ghost.
- Objects without motion vectors (sky, far background): write camera-only motion.
- Transparent objects: either write motion where dominant or add them to the reactive mask.

## 5. Reactive mask generation (FSR)
Write the alpha used to composite an alpha-blended object into the reactive mask, and clamp the maximum to about 0.9 (values near 1
rarely look good). Alternatively call `ffxDispatchDescUpscaleGenerateReactiveMask`, passing one colour buffer with opaque geometry only and
one with opaque and alpha-blended geometry; it derives the masks with a luminance-based heuristic.

## Gotchas
- Jitter belongs in the render-resolution inputs; FSR motion vectors are not jittered unless the cancellation flag is set.
- Telling the upscaler HDR from LDR input wrongly gives bad results; set the HDR flag to match your colour input.
- Forgetting the reset on a camera cut leaves previous-frame history in play.

## Verify
- [ ] No ghosting on particles, scrolling textures or skinned characters.

## Checked

2026-10-26: FidelityFX SDK docs (GPUOpen-LibrariesAndSDKs/FidelityFX-SDK, Kits/FidelityFX/docs/techniques/super-resolution-upscaler.md, pushed 2026-06-24) and Streamline docs/ProgrammingGuideDLSS.md (NVIDIA-RTX/Streamline), plus the XeSS repository README, read 2026-10-26. Confirmed for FSR: inputs, jitter, inverted depth recommendation, exposure texture, reactive mask clamp near 0.9, helper API, T&C mask, jump-cut reset, mip bias formula and table, post-processing placement table. Confirmed for Streamline/DLSS: required resources, mvecScale, pixel-space jitter, exposure and auto-exposure. Wrong claims fixed: the old text gave the -1.0 term to DLSS and omitted it for FSR (the FSR formula includes -1.0), said depth of field and motion blur could go before the upscaler (FSR places them after), described the reactive mask as max alpha times 0.9, and called the vendor SDKs a unified API. The DLSS programming guide PDF could not be read as text, so DLSS mip bias, bias-current-colour mask and reset behaviour are marked gated. The dynamic-resolution claim was removed.

Method: documentation only; no commands were run.
