---
id: computing-software.computer-graphics-engineering.webgl-threejs.threejs-webxr-performance-foveation
name: threejs-webxr-performance-foveation
category: computing-software
field: computer-graphics-engineering
product: webgl-threejs
tags: [computer-graphics-engineering, threejs, webxr, xr-foveation, framebuffer-scale, fixed-foveated-rendering, foveated-rendering, quest-browser, ovr-multiview2, xr-frame-rate, mobile-vr-performance]
level: advanced
status: draft
description: "Hit 72-90 fps in three.js WebXR on standalone headsets: foveation level, framebuffer scale, multiview, draw-call and overdraw budgets."
sources: ["https://threejs.org/docs/#api/en/renderers/webxr/WebXRManager", "https://developers.meta.com/horizon/documentation/web/webxr-perf-workflow/", "https://immersive-web.github.io/webxr/#dom-xrwebgllayer-fixedfoveation", "https://developers.meta.com/horizon/documentation/web/webxr-ffr/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# three.js WebXR performance and foveation

**Goal:** stable native refresh (72/90/120 Hz) on Quest-class mobile GPUs — dropped frames
in VR cause discomfort, not just stutter.

## 1. Resolution levers
```js
renderer.xr.setFramebufferScaleFactor(0.8);   // BEFORE session start; 1 = recommended res
renderer.xr.setFoveation(1);                  // 0 none .. 1 max fixed foveation (default 1 in recent three)
renderer.setPixelRatio(1);                    // devicePixelRatio is irrelevant in XR
```
- Fixed foveated rendering lowers resolution at the lens periphery where optics blur
  anyway: large fill-rate savings, artefacts mostly invisible at level 0.5–1 (visible on
  high-contrast text near edges).
- Framebuffer scale below ~0.7 becomes noticeably blurry; trade with foveation first.

## 2. Multiview
Three.js uses `OVR_multiview2` automatically when available (WebXR layers + multiview) —
one draw renders both eyes, halving CPU draw cost. Custom ShaderMaterials must be
multiview-compatible (use built-in matrices; three injects `VIEW_ID` handling).

## 3. Budgets (Quest 2/3 class, ballpark)
| item | target |
|---|---|
| draw calls | 50–200 |
| triangles | 300k–1M per frame |
| overdraw / transparency | minimal; avoid full-screen transparent layers |
| post-processing | none or merged into materials |
| shadows | baked or one small shadow map |
| textures | KTX2 (ASTC/ETC via Basis) to save bandwidth |

## 4. Frame rate selection
```js
const session = renderer.xr.getSession();
if (session.supportedFrameRates) await session.updateTargetFrameRate(72);
```
Pick the rate you can hold; consistent 72 beats fluctuating 90.

## 5. Profile on device
- Meta Quest: OVR Metrics Tool overlay (GPU %, app GPU time, foveation level), Chrome
  remote devtools via `adb` for JS profiling.
- `renderer.info.render.calls/triangles` logged in-session.
- GPU-bound vs CPU-bound: if lowering framebuffer scale doesn't help, you're CPU/draw-call bound.

## Gotchas
- Settings made after the session starts (framebuffer scale) are ignored until re-entry.
- MSAA: WebXR layers default to 4x on many devices; costs bandwidth but transparent on tilers
  — keep it, avoid extra AA passes.
- Big transparent particles/UI panels near the face = overdraw spikes.

## Verify
- [ ] OVR Metrics shows stable target fps over a 5-minute session.
- [ ] Foveation level verified in metrics overlay.
- [ ] Worst-case scene view stays within draw-call/triangle budget.
