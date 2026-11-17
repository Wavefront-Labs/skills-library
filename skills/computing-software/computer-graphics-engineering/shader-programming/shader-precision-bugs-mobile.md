---
id: computing-software.computer-graphics-engineering.shader-programming.shader-precision-bugs-mobile
name: shader-precision-bugs-mobile
category: computing-software
field: computer-graphics-engineering
product: shader-programming
tags: [computer-graphics-engineering, shader-programming, shader-debugging, precision-bugs, mediump, fp16, mobile-gpu, floating-point, shader-artifacts]
level: practitioner
status: docs-checked
description: "Find and fix shader precision bugs: mediump overflow, large UV and time values, depth/position reconstruction errors, and artefacts that appear only on mobile GPUs."
sources: ["https://registry.khronos.org/OpenGL/specs/es/3.0/GLSL_ES_Specification_3.00.pdf"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Precision bugs and mobile artefacts

## 1. fp16 facts
- fp16 `half`: 10-bit mantissa, max 65504, ~3 decimal digits; integers are exact only to 2048. GLSL ES `mediump` guarantees
  only a range of (-2^14, 2^14) and relative precision 2^-10, and an implementation may use more.
- At value 1024, the step between representable halves is 1.0. At 64, it's 1/16.
- Hardware that implements `mediump` as fp32 hides these bugs, so they can appear only on some devices.

## 2. Classic bugs
| Artefact | Cause | Fix |
|---|---|---|
| Texture becomes blocky/jittery after the app runs a while | `time` in mediump grows large | `highp` time, wrap with `mod(time, period)` on CPU |
| Textures swim/pixelate on large meshes | mediump UVs with large or tiled textures | `highp` UVs or tile UVs per mesh |
| Specular "blocks" or black spots | `pow(NdotH, 256)` underflows / `NdotH^n` in half | highp for specular or clamp exponent |
| Banding in gradients/fog | half precision distances | highp for world positions and distances |
| Shimmering shadows | depth comparisons in mediump | highp for shadow coordinates |
| NaN black pixels | `normalize(0)` in half, `sqrt(negative)` from rounding | guard: `max(dot, 1e-4)` |
| World positions jitter far from origin | fp32 at 10 km has ~1 mm steps; matrices large | camera-relative rendering |

## 3. Debugging technique
- Force everything to highp on device (`#define mediump highp` hack) - if the bug vanishes, it's
  precision.
- Then re-enable mediump per variable to find the culprit.
- Visualise suspect values `fract(value * k)`; quantisation steps become visible as bands.

## 4. Camera-relative rendering
Subtract camera position from object positions on the CPU (in double) before building matrices;
the GPU only sees small numbers. Fixes jitter in large worlds on all GPUs.

## Gotchas
- Interpolated varyings in mediump lose precision across big triangles; compute UVs per pixel from
  highp where needed.
- fp16 denormals may flush to zero depending on hardware; small values (e.g. tiny roughness^4) can become 0 and cause a divide by zero.

## Verify
- [ ] Test on devices from more than one GPU vendor for long sessions (time-dependent bugs).
- [ ] Visual parity with desktop at far distances and large UV values.

## Checked

Checked 2026-10-26 against GLSL ES 3.00 specification (section 4.5.1 range and precision table), IEEE-754 binary16 arithmetic computed by hand. Confirmed: mediump minimum range (-2^14, 2^14) and relative precision 2^-10; binary16 facts (max 65504, integers exact to 2048, step 1.0 at 1024, step 1/16 at 64, computed from the 10-bit mantissa); single-precision step at 10 km is 2^-10 m (about 1 mm, computed). Removed as unconfirmed: the Mali Offline Compiler remark, the 'UV > ~16' threshold, the claim that desktop GPUs ignore mediump, and the video and Arm links (not readable).

Method: documentation only; no commands were run.
