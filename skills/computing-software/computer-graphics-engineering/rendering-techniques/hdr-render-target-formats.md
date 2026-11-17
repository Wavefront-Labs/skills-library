---
id: computing-software.computer-graphics-engineering.rendering-techniques.hdr-render-target-formats
name: hdr-render-target-formats
category: computing-software
field: computer-graphics-engineering
product: rendering-techniques
tags: [computer-graphics-engineering, rendering-techniques, hdr-tonemapping, hdr-render-target, r11g11b10f, rgba16f, pre-exposure, floating-point-formats, bandwidth]
level: practitioner
status: docs-checked
description: "Choose HDR render target formats: RGBA16F vs R11G11B10F vs RGB9E5 precision and bandwidth, pre-exposure to avoid fp16 overflow, and alpha/storage limitations."
sources: ["https://github.com/KhronosGroup/Vulkan-Docs/blob/main/chapters/formats.adoc", "https://github.com/KhronosGroup/Vulkan-Docs/blob/main/chapters/fundamentals.adoc"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# HDR render target formats and precision

## 1. Options
| Format | Bits | Range | Precision | Alpha | Notes |
|---|---|---|---|---|---|
| RGBA16F | 64 | +-65504 | 10-bit mantissa | yes | common HDR target; Vulkan mandates colour attachment and blend support |
| R11G11B10F | 32 | 0..65024 (R,G), 0..64512 (B) | 6/6/5-bit mantissa | no | half the size of RGBA16F; no sign bit; Vulkan does not mandate attachment support, so query it |
| RGB9E5 | 32 | 0..65408 | 9-bit mantissa, shared 5-bit exponent | no | Vulkan's mandatory table lists it for sampling, linear filtering and blit source only, not as an attachment |
| RGBA32F | 128 | huge | 23-bit | yes | accumulation/path tracing only |
| RGB10A2 unorm | 32 | 0..1 | 10-bit | 2-bit | fixed-point, display-referred; not a scene-referred HDR format |

## 2. Choosing
- Lighting buffer: R11G11B10F if you don't need alpha or negative values and bandwidth matters
  (consoles, mobile high-end); RGBA16F otherwise.
- TAA history: RGBA16F (or R11G11B10F with care; precision loss shows as colour drift in dark areas
  with many accumulations).
- Bloom chain: R11G11B10F.
- Mobile: check `VK_FORMAT_B10G11R11_UFLOAT_PACK32` support as COLOR_ATTACHMENT and blendable.

## 3. Pre-exposure
fp16 max is 65504; sunlit specular highlights in physical units can overflow to
inf. Multiply lighting by the camera exposure (from the previous frame) when writing the lighting
buffer, so stored values are near display range:
```glsl
outColor = vec4(radiance * preExposure, 1.0);   // preExposure = exposure of last frame
```
Then tonemap without re-applying that factor. Also helps R11G11B10F precision.

## 4. Pitfalls with R11G11B10
- No sign bit: subtractive effects (negative lobes, sharpen overshoot) clamp to 0.
- 5-bit mantissa in blue (the 10-bit component): blue gradients can band; add dither before storing.
- Vulkan lists storage-image support for B10G11R11 with caveats in its mandatory-format table; query the format features.

## Gotchas
- NaN/inf in HDR targets spreads through bloom/TAA; clamp inputs (`min(x, 65000)`, NaN guard)
  before writing.
- MSAA RGBA16F is expensive on bandwidth; resolve early or use R11G11B10F.

## Verify
- [ ] No inf/NaN in the lighting buffer in bright scenes (debug view `isinf`).
- [ ] Banding test on a dark gradient for the chosen format.

## Checked

2026-10-26: Vulkan-Docs chapters formats.adoc and fundamentals.adoc (main as of 2026-10-23), read 2026-10-26. Confirmed: B10G11R11_UFLOAT is a 10-bit B and 11-bit G/R unsigned float and E5B9G9R9 a 5-bit shared exponent with 9-bit mantissas; the mandatory-format table lists R16G16B16A16_SFLOAT with colour attachment and blend, E5B9G9R9 only as sampled/filterable/blit source, and B10G11R11 without mandatory attachment support and with storage-image caveats. Ranges computed: fp16 65504, 11-bit float 65024, 10-bit float 64512, RGB9E5 65408. Wrong claim fixed: R11G11B10F maximum is 65024/64512, not 0..65000 (and Vulkan does not guarantee it as a colour attachment). Removed the blendable/UAV claim for RGBA16F outside Vulkan, the hue-shift claim, and the HDR10/PQ claim for RGB10A2.

Method: documentation only; no commands were run.
