---
id: creative-arts.animation.texturing.delighting-source-photos
name: delighting-source-photos
category: creative-arts
field: animation
product: texturing
tags: [delighting, de-lighting, albedo, photo-textures, photogrammetry, shadow-removal, texturing]
level: advanced
status: draft
description: "Remove baked-in light and shadow from source photos to get usable albedo: capture to avoid it, divide-by-blur, tool options, validating against albedo ranges."
sources:
  - https://helpx.adobe.com/substance-3d-painter
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Delighting source photos

Photographs include the lighting of the moment: shadows, gradients, highlights and reflections. Used as an albedo/base colour, that lighting is double-counted when the material is lit again by the renderer. **Delighting** removes it.

## Best: avoid it at capture
- Cross-polarised photography removes specular highlights, and flat overcast light or a diffuse softbox removes hard shadows (`capturing-texture-photos-cross-polarised.md`).
- Shoot perpendicular to the surface to limit perspective and gradient.

## Techniques
1. **Divide by blur** (low-frequency removal): duplicate the photo, apply a large Gaussian blur (radius larger than the biggest detail), put it above the original and set the blend to Divide, then restore mean brightness with a Levels or Curves adjustment. The slow brightness gradient is removed while detail stays. Works on flat, fairly uniform surfaces.
2. **Clone and heal** out strong shadows, reflections and stains manually in an image editor.
3. **Highlight and shadow tools** (Shadows/Highlights, high-pass) for mild cases.
4. **Dedicated tools**: some tools have delighting functions, for example the AI-powered filters in Adobe Substance 3D Sampler, and photogrammetry software such as Agisoft Metashape provides a delighting tool for textures; features and quality vary by version, so test on your material.
5. **Reprojection**: for photogrammetry, bake out the lighting (ambient occlusion and shading from the geometry) and divide it out.

## Validate
- Compare the average luminance with realistic albedo ranges (`pbr-albedo-ranges.md`): avoid pure black or white.
- View the result under a neutral and a harsh light in the renderer; baked shadows will show as mismatched shadows.
- Check **tiling** if it needs to repeat (`seamless-tiling-textures.md`).

## Gotchas
- Divide-by-blur flattens real large-scale colour variation; keep a masked amount.
- AI delighting can hallucinate detail; check hero areas.

## Verify
- [ ] No visible directional light or shadow in the albedo.
- [ ] Brightness sits in a plausible albedo range.
