---
id: computing-software.computer-graphics-engineering.rendering-techniques.xr-passthrough-mixed-reality-compositing
name: xr-passthrough-mixed-reality-compositing
category: computing-software
field: computer-graphics-engineering
product: rendering-techniques
tags: [computer-graphics-engineering, rendering-techniques, xr-rendering, passthrough, mixed-reality, environment-blend-mode, alpha-blend, occlusion]
level: advanced
status: docs-checked
description: "Render mixed reality over camera passthrough: blend modes, alpha-clear rules, premultiplied output, depth-based occlusion, lighting estimation, and OpenXR/WebXR setup."
sources: ["https://registry.khronos.org/OpenXR/specs/1.1/html/xrspec.html", "https://github.com/KhronosGroup/OpenXR-Docs/tree/main/specification/sources/chapters/extensions/fb/fb_passthrough.adoc", "https://github.com/immersive-web/webxr-ar-module", "https://github.com/immersive-web/depth-sensing", "https://github.com/immersive-web/lighting-estimation"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Passthrough and mixed reality compositing

## 1. Blend modes
- `OPAQUE`: VR, your frame replaces the world. VR apps generally choose it.
- `ADDITIVE`: the composited image is added to the environment, so black appears transparent: a black shadow cannot be seen
  (the spec suggests a glow around it).
- `ALPHA_BLEND`: your layer alpha composites over the environment; alpha you leave as garbage becomes a visible artefact.
Not every system supports every mode: query with `xrEnumerateEnvironmentBlendModes` (WebXR: `session.environmentBlendMode`,
values `opaque`, `additive`, `alpha-blend`) and pass the chosen mode in `XrFrameEndInfo::environmentBlendMode` every frame.

## 2. Alpha rules for ALPHA_BLEND
- Clear to `(0, 0, 0, 0)`; anything you draw writes alpha 1 (or partial for fades).
- OpenXR layer blending is `CompositeColor = LayerColor + CompositeColor * (1 - LayerColor.A)`: colour is treated as premultiplied.
  Set `XR_COMPOSITION_LAYER_BLEND_TEXTURE_SOURCE_ALPHA_BIT` or the layer alpha is initialised to 1, and set
  `XR_COMPOSITION_LAYER_UNPREMULTIPLIED_ALPHA_BIT` if your colour is not premultiplied.
- Post-processing and tone mapping must preserve alpha, or passthrough is hidden.
- Skyboxes and fog must be disabled in MR or they paint over the room.

## 3. Vendor passthrough layers
`XR_FB_passthrough` adds a passthrough layer (`XrCompositionLayerPassthroughFB`) that you place in the `xrEndFrame`
layer array like any other layer, so order it before your projection layer. You can style it (edge rendering with
`edgeColor`, disabled when its alpha is 0; colour maps `XrPassthroughColorMapMonoToRgbaFB` / `...MonoToMonoFB`) or
project it onto geometry you supply for windows into reality.

## 4. Making it believable
- **Occlusion**: depth APIs (OpenXR `XR_META_environment_depth`, WebXR Depth Sensing Module): compare virtual depth
  against environment depth with a soft edge band to hide noise.
- **Shadows**: shadow-catcher materials (draw only darkening, alpha = shadow strength) on detected planes or scene mesh.
- **Lighting**: light estimation (WebXR `XRLightProbe`) for environment maps and main light direction.
- **Scale and anchoring**: scene understanding planes/mesh and anchors so content sits on real surfaces.

## Gotchas
- Fast head motion can make content swim against the camera feed; keep content anchored in the world.
- Additive displays: black is transparent, so dark UI disappears.

## Verify
- [ ] Room visible everywhere nothing virtual is drawn (alpha correct after post).
- [ ] Real objects occlude virtual ones within a few centimetres.

## Checked

2026-10-26: OpenXR specification source (KhronosGroup/OpenXR-Docs, main as of 2026-10-16) and the WebXR AR module draft. Confirmed: the three environment blend modes and their behaviour (rendering.adoc), layer blend equation and the alpha and unpremultiplied flag bits (rendering.adoc, xr.xml), XR_FB_passthrough edge colour (alpha 0 disables) and colour map structures, layer ordering by array position, XR_META_environment_depth listed in the Meta extensions, WebXR environmentBlendMode with alpha-blend, XRLightProbe and the depth-sensing module repositories. Removed device names, ARCore references, the claim that raw camera access is restricted, and the passthrough-latency claim, which were not confirmed.

Method: documentation only; no commands were run.
