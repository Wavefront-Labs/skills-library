---
id: creative-arts.animation.blender.shader-authoring-lookdev
name: shader-authoring-lookdev
category: creative-arts
field: animation
product: blender
tags: [blender, shader, lookdev, npr, node-group, toon-ramp, gradient, glass, metal, emissive, skin, crt, screen-material, material-library, eevee-next, cel]
level: advanced
status: docs-checked
description: "NPR materials in Blender EEVEE: Shader to RGB toon ramps and limits, render method for toon glass, unsupported nodes."
sources:
  - https://docs.blender.org/manual/en/latest/render/eevee/material_settings.html
  - https://docs.blender.org/manual/en/latest/render/eevee/limitations/nodes_support.html
  - https://docs.blender.org/manual/en/latest/render/shader_nodes/input/geometry.html
  - https://docs.blender.org/manual/en/latest/render/shader_nodes/color/shader_to_rgb.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---

# Shader authoring and look-dev for NPR (Blender EEVEE)

Goal: toon materials beyond the base cel shader (layered ramps, glass, metal, emissive screens) that stay consistent across a cast and set. The base recipe is in `creative-arts.animation.blender.cel-shading`; this skill covers what the EEVEE manual says about the building blocks and their limits.

## The Shader to RGB foundation

- The **Shader to RGB** node is EEVEE only. It converts a BSDF's lighting result to a colour (plus the alpha of any Transparent BSDF), so a Color Ramp on a diffuse BSDF makes a toon shader.
- It breaks the PBR pipeline: results are unpredictable with ambient occlusion, contact shadows, soft shadows and screen space refraction, and noisy input may not convert to a smooth result.
- Any BSDF upstream of the node is invisible to Screen Space Reflection, Subsurface Scattering and the Alpha Clip and Alpha Hashed blend modes. The node does not give expected results in render passes.
- It evaluates lighting like a Blended material and inherits its limits. Through it, a Transparent BSDF can expose the radiance behind an object depending on the material's render method and the Raytraced Transmission setting.

## Layered ramps and painted looks (craft)

Keep one hard-stepped ramp for the band mask and use it to mix between authored colours, so each band can be hue shifted independently. Extra hard-banded terms (a facing/Fresnel rim band, an occlusion contact band) can be mixed over the base. Keep the number of distinct values small. Gradient textures into a Color Ramp feed Base Color for painted tints, and a small noise term into the band input can break the terminator line.

For edge and crevice tint, the Geometry node's Pointiness output is Cycles only and is not supported in EEVEE; the EEVEE nodes-support page also lists the Bevel node as unsupported and notes the Ambient Occlusion node's Only Local option is not supported. Use a baked curvature or edge map or a Geometry Nodes attribute instead.

## Special toon materials

- **Glass and transparency:** in Material > Settings, the **Render Method** is Dithered (grayscale hashed transparency, compatible with render passes and raytracing) or Blended (coloured transparency, incompatible with render passes and raytracing, and sorted per object by origin only). Blended offers a *Transparency Overlap* option to help with sorting problems. Use flat tinted transparency and hard highlight shapes rather than real refraction when you want a drawn look.
- **Metal:** the manual lists Toon BSDF, Anisotropic BSDF and Sheen BSDF as unsupported in EEVEE, and Glossy supports GGX and Multiscatter GGX only. Build banded metal from a ramp over a view-dependent vector instead.
- **Emissive:** use Emission for anything that must ignore scene light; mind compositor glare so intentional glows are the only things that bloom.
- **Backface Culling** (Camera, Shadow, Light Probe Volume) hides back faces and should be on whenever possible for performance. Pass Index feeds the Material Index pass for masks in the compositor (ID Mask node).

## Shared node-group library (practice)

Author materials once as node groups in a shared library file with a clean input interface (colour, a few controls) and reuse them, so a note on a look is one edit. Use consistent names, link library groups so edits propagate, and append only when an asset needs a divergent variant.

## Checked

2026-11-09. Confirmed against the EEVEE Materials, Supported Nodes (limitations), Geometry node and Shader to RGB manual pages: Shader to RGB behaviour and limits, render methods and their compatibility, Transparency Overlap, Backface Culling, Pass Index, unsupported nodes (Toon, Anisotropic, Sheen BSDF, Bevel, Pointiness, Only Local). The library and layered-ramp sections are craft practice, not documented in the manual. Removed: show-specific materials (CRT screen, skin recipes), scanline, vignette and glitch recipes, numeric strengths, and the lookdev file layout.
Method: documentation only; no commands were run.

## Verify

1. Every material traces back to a named library group.
2. Glass, metal and skin still quantize to hard bands under the chosen view transform.
3. Glass uses the intended Render Method and is checked for sorting in a moving camera.
4. Emissive and screen materials do not bloom unless intended.
5. Changing a library group updates two different shots identically.

See also: `cel-shading.md`, `lighting.md`, `compositing-grade.md`, `render-optimization.md`.
