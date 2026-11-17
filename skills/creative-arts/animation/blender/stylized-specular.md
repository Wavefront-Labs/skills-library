---
id: creative-arts.animation.blender.stylized-specular
name: stylized-specular
category: creative-arts
field: animation
product: blender
tags: [blender, stylized-specular, toon-specular, anisotropic-highlight, hair-highlight, npr, cel-shading]
level: advanced
status: docs-checked
description: "Toon specular in Blender: Glossy to Shader to RGB ramp, Blinn-Phong half-vector highlights, anisotropic and UV-band hair highlights."
sources:
  - https://docs.blender.org/manual/en/latest/render/shader_nodes/shader/glossy.html
  - https://docs.blender.org/manual/en/latest/render/shader_nodes/color/shader_to_rgb.html
  - https://docs.blender.org/manual/en/latest/render/shader_nodes/input/geometry.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---

# stylized-specular

Goal: graphic highlight shapes (blobs, streaks, hair rings) instead of physically blurry specular.

## EEVEE: Glossy to ramp

```
Glossy BSDF (white, low Roughness) ─► Shader to RGB ─► Color Ramp (hard step) ─► highlight mask
```
Shader to RGB is EEVEE only. Add the mask times a highlight colour onto the toon result. Glossy *Roughness* is perfectly sharp at 0.0 and smoother as it rises, so it sets the highlight size; the ramp stop sets its edge.

## Light-independent Blinn-Phong

With a driven light vector `Ldir` (see `creative-arts.animation.blender.cel-light-direction`):
```
V = view vector (toward the camera)      H = normalize(Ldir + V)
spec = pow(max(dot(Normal, H), 0), shininess) ─► Color Ramp (hard step) ─► mask
```
The Geometry node gives *Normal* (shading normal, includes smooth normals and bump) and *Incoming* in world space; check in the viewport which way Incoming points and negate it if needed so V faces the camera. Build the maths from Vector Math (Add, Normalize, Dot Product) and Math (Power). The shape stays crisp and art-directable because no scene light is involved.

## Anisotropic and hair highlights

- The Glossy BSDF has *Anisotropy* (Cycles only; 0.0 = none, higher values elongate the highlight orthogonal to the tangent, negative values shape it along the tangent), *Rotation* (0.25 = 90 degrees) and a *Tangent* input (the Geometry node also outputs *Tangent*). Because Anisotropy is Cycles only, an EEVEE toon highlight needs the half-vector or UV-band method instead.
- Anime "angel ring" on hair: a band generated or painted in UV space across the hair, masked by a lighting dot product so the ring slides with the light.

## Gotchas

- Shader to RGB breaks the PBR pipeline: results are unpredictable with ambient occlusion, contact shadows, soft shadows and screen space refraction; upstream BSDFs become invisible to Screen Space Reflection, Subsurface Scattering and Alpha Clip / Alpha Hashed blend modes; and it does not give expected results in render passes.
- Effects that need several samples to converge may not turn smooth after an arbitrary ramp is applied to noisy input.
- Shininess exponents are very sensitive: drive them from a single control value.

## Verify

Move the light: the highlight moves as a clean shape without soft halos; on hair the band stays on the strand direction.

## Checked

2026-11-09. Confirmed against the Blender manual (raw RST of the Glossy BSDF, Shader To RGB and Geometry node pages, read in full): Roughness semantics, Anisotropy / Rotation / Tangent inputs and Cycles-only marking, Shader to RGB EEVEE-only status and its listed limitations, Geometry node Normal / Incoming / Tangent outputs. Removed: numeric roughness, shininess and anisotropy ranges, the Principled BSDF anisotropic and Tangent-node claims, the world-specular and light-linking advice, and the "Incoming negated" claim (the page wording on its direction is ambiguous, so the skill says to test it).
Method: documentation only; no commands were run.
