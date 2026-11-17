---
id: computing-software.computer-graphics-engineering.shader-programming.hologram-and-force-field-shaders
name: hologram-and-force-field-shaders
category: computing-software
field: computer-graphics-engineering
product: shader-programming
tags: [computer-graphics-engineering, shader-programming, surface-shading-effects, hologram-shader, force-field-shader, scanlines, intersection-highlight, depth-fade, vfx-shader]
level: practitioner
status: draft
description: "Build hologram and force-field shaders: scanlines, Fresnel glow, glitch offsets, depth-intersection highlights, and additive blending order for transparent effects."
sources: ["https://docs.unity3d.com/Packages/com.unity.shadergraph@17.0/manual/Scene-Depth-Node.html", "https://www.cyanilux.com/tutorials/forcefield-shader-breakdown/", "https://docs.godotengine.org/en/stable/tutorials/shaders/screen-reading_shaders.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Hologram, scanline and force-field effects

## 1. Hologram
```glsl
float NdotV = saturate(dot(N, V));
float fres  = pow(1.0 - NdotV, 3.0);
float scan  = step(0.5, fract(worldPos.y * lineDensity - time * speed));   // hard lines
float scanSoft = 0.5 + 0.5 * sin((worldPos.y * lineDensity - time * speed) * 6.2831);
float flicker = 0.9 + 0.1 * step(0.98, hash(floor(time * 20.0)));
vec3 col = holoColor * (fres * 2.0 + scanSoft * 0.3) * flicker;
float alpha = saturate(fres + scan * 0.2);
```
- Use world-space or object-space Y for scanlines so they don't swim with UVs.
- Glitch: offset vertex positions along X in thin horizontal bands at random times
  (`pos.x += step(0.99, hash(floor(pos.y*20.0)+floor(time*10.0))) * 0.05`).
- Blend additively (`ONE, ONE`) with depth write off; additive is order-independent.

## 2. Force field with intersection glow
Needs the opaque scene depth texture (render the shield after opaques):
```glsl
float sceneDepth = linearizeDepth(texture(depthTex, screenUV).r);
float surfDepth  = linearEyeDepth;                     // of this fragment
float diff = sceneDepth - surfDepth;                   // > 0 in front of geometry
float intersect = 1.0 - smoothstep(0.0, edgeWidth, diff);
float alpha = saturate(fres + intersect) * shieldAlpha;
```
Add hex patterns (see tiling patterns), impact ripples (distance from hit point in a uniform array,
`sin(dist*freq - t)` attenuated over time) and a scrolling noise distortion.

## 3. Render setup
- Queue after opaques; depth test on, depth write off.
- Back faces: render a second pass with `cull front` for the inside of the sphere, or two-sided
  with `gl_FrontFacing` to dim the back.
- URP/HDRP: enable the camera Depth Texture; Godot: `hint_depth_texture`; Unreal: SceneDepth node
  (translucent materials only).

## Gotchas
- Depth texture is non-linear; always linearise both depths before subtracting.
- MSAA with depth texture: use the resolved depth or the intersection edge flickers.
- Additive effects blow out in HDR with bloom; clamp emission or tune bloom threshold.

## Verify
- [ ] Intersection glow appears where the shield meets ground and props, constant width in world units.
- [ ] Scanlines stable in world space while the camera moves.
