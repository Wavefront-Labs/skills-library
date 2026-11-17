---
id: creative-arts.animation.blender.cryptomatte-setup
name: cryptomatte-setup
category: creative-arts
field: animation
product: blender
tags: [blender, cryptomatte, cryptomatte-setup, cryptomatte-levels, render-passes, view-layer]
level: practitioner
status: docs-checked
description: "Render Cryptomatte from Blender: View Layer Passes for Object, Material and Asset, Levels and the number of output images, naming for clean picking, output metadata and limits."
sources:
  - https://docs.blender.org/manual/en/latest/render/layers/passes.html
  - https://docs.blender.org/manual/en/latest/compositing/types/mask/cryptomatte.html
  - https://github.com/Psyop/Cryptomatte
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# cryptomatte-setup

Goal: ID mattes for objects and materials without planning masks ahead.

## Enabling (Properties > View Layer > Passes > Cryptomatte)

- **Object**: isolates objects.
- **Material**: isolates materials.
- **Asset**: isolates groups of objects with the same parent. The manual notes this is not related to Blender's asset feature.
- **Levels**: the maximum number of objects distinguished per pixel (range 2 to 16 in the 5.2 source). The Render Layers node outputs half this many Cryptomatte images, named for example *CryptoObject00*, *CryptoObject01*, because one image references two objects per pixel. The first image holds the two objects contributing most to the pixel, the next image the next two, and so on.
- The standard works with transparency, and with motion blur and depth of field when using Cycles. Unlike Object Index and Material Index, objects to isolate are chosen in compositing.
- There is also an **Accurate** option (`use_pass_cryptomatte_accurate`, described in the source as generating a more accurate pass).

## Make picking work

- Cryptomatte matches by name, so name objects and materials meaningfully and keep names consistent across shots so compositing setups can be reused (practice).
- Mattes can be typed or picked in the Cryptomatte node's Matte ID field (see `creative-arts.animation.blender.cryptomatte-node-picking`).

## Output

Blender stores per-layer metadata (name, hash `MurmurHash3_32`, conversion `uint32_to_float32`, manifest) with the render result. The conversion shows IDs are float32 bit patterns, so write Cryptomatte layers as 32-bit float EXR (Float (Full)); a half-float file cannot hold a 32-bit pattern. See `creative-arts.animation.blender.cryptomatte-handoff` for what to check on the written file.

## Limits (Blender manual)

- Cryptomatte sidecar (metadata) files are not supported.
- Volume objects are not supported.
- The Cryptomatte node cannot be used in node groups.
- Other limits (refraction, emission-only objects, texture areas inside one object) are not covered by the manual; use Material Index or AOV passes where Cryptomatte has no ID for what you need.

## Verify

In the compositor add a Cryptomatte node, pick an object, and view the Matte output.

## Checked

Checked 2026-10-27 against the Blender 5.2 manual (blender-v5.2-release branch: render/layers/passes, compositing/types/mask/cryptomatte) and the 5.2 source (rna_scene.cc Cryptomatte properties, blenkernel cryptomatte.cc metadata keys). Fixed: Levels default and the suggestion of 8 to 10 levels are not documented (range is 2 to 16), the image count is Levels divided by two, and the manual lists sidecar, volume and node-group limits. Removed unconfirmed claims about refraction, library overrides and emission-only objects.
Method: documentation only; no commands were run.
