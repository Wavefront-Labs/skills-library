---
id: creative-arts.animation.texturing.channel-packing-orm
name: channel-packing-orm
category: creative-arts
field: animation
product: texturing
tags: [channel-packing, texture-export, orm, mask-map, occlusion-roughness-metallic, rgba-packing, unreal, unity, gltf, game-engine]
level: practitioner
status: draft
description: "Pack grayscale maps into RGBA channels (ORM, Unity mask maps, glTF metallicRoughness) to save memory and samplers, and unpack correctly in shaders."
sources:
  - https://registry.khronos.org/glTF/specs/2.0/glTF-2.0.html#metallic-roughness-material
  - https://docs.unity3d.com/Packages/com.unity.render-pipelines.high-definition@17.0/manual/Mask-Map-and-Detail-Map.html
  - https://helpx.adobe.com/substance-3d-painter/texturing/export/export-settings.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Channel packing (ORM and friends)

**Goal:** fewer texture files and samplers by storing several grayscale maps in the R, G, B, A channels
of one texture. Standard for real-time engines and glTF; also useful for offline to reduce file counts.

## Common layouts

| Convention | R | G | B | A |
|---|---|---|---|---|
| ORM (Unreal common) | Ambient Occlusion | Roughness | Metallic | (free) |
| glTF 2.0 metallicRoughnessTexture | (unused, or occlusion) | Roughness | Metallic | - |
| Unity HDRP Mask Map | Metallic | Ambient Occlusion | Detail mask | Smoothness (1 - roughness) |
| Unity URP/Built-in Metallic | Metallic | - | - | Smoothness |

Note Unity uses **smoothness** (inverted roughness): invert in the export preset (Painter offers
"Glossiness"/converted channels) or in the shader.

## Painter export

In the export preset, create one output map (e.g. `$textureSet_ORM`), set it to RGB (or RGBA) and drag
Ambient Occlusion into R, Roughness into G, Metallic into B. Save as 8-bit PNG/TGA (data, linear).

## Shader side

- Import the packed texture as **linear/Non-Color** (sRGB off). An sRGB-flagged ORM shifts roughness
  values badly.
- In Blender: Image Texture (Non-Color) - Separate Color (RGB) - G to Roughness, B to Metallic, R to an
  AO mix if used.
- Engines: assign to the packed slot (Unreal material: split channels with component masks).

## Gotchas

- Compression: BC1/DXT1 compresses RGB channels together and blurs between channels; BC7 keeps packed
  data cleaner (`creative-arts.animation.texturing.texture-compression-formats`).
- Do not pack maps with different resolutions needs (a 4K roughness with a 1K AO wastes space).
- Alpha channel in PNG may be premultiplied by some tools, destroying packed data; use TGA/TIFF or check
  the writer.

## Verify

Open the packed texture and view each channel separately: each is the intended map; in the engine the
material looks the same as with separate maps.
