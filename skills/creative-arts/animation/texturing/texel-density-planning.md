---
id: creative-arts.animation.texturing.texel-density-planning
name: texel-density-planning
category: creative-arts
field: animation
product: texturing
tags: [texel-density, uv-layout, texture-resolution, pixels-per-metre, consistency, texturing, uv]
level: practitioner
status: draft
description: "Plan and check texel density so textures look equally sharp across assets: formula, choosing a target, hero versus background ratios, measuring and setting in DCCs."
sources:
  - https://helpx.adobe.com/substance-3d-painter
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Texel density

**Texel density** is the number of texture pixels per unit of surface: for example pixels per metre. Consistent density makes assets in a shot look equally sharp; mismatches show immediately (a blurry table next to a crisp cup).

## Formula
`density (px/m) = texture size in px x UV island share of the side / real size in m`

Example: an object whose island fills a full 2048 px tile and which is 2 m long has about 1024 px/m (about 10 px per cm) along that axis, if UV scale is uniform.

## Choosing a target
1. Decide from the **closest camera distance** and the output resolution: the texture needs about one texel per screen pixel at the nearest view.
2. Set a **base density** for the project, then multipliers: hero assets and close-up props higher (for example 2x), distant sets lower.
3. Pick texture sizes by powers of two (`texture-resolution-planning.md`) and fit the UV scale to the density target.
4. Write the targets in the style guide. Game-style budgets might use a few hundred to a thousand-plus px/m; the exact figure is project-specific.

## Measuring and setting
- Use a **checker pattern** of fixed UV size: squares should appear the same real size on every asset.
- Some DCCs have texel-density tools: Maya's UV Toolkit has a texel density section; Blender has add-ons for this, and 3D tools such as RizomUV include texel density controls. Check the tool you use.
- Normalise density **before** packing; packing may scale all islands together by a uniform factor, which is fine.

## Special cases
- **UDIM** assets keep the same density across tiles (`udim-tiles-and-workflow.md`).
- **Tiling materials** use their own scale; match their real-world size to the asset density.
- **Mirrored** islands save space but need identical density.

## Verify
- [ ] Checker squares match across neighbouring assets.
- [ ] Hero vs background ratios are as specified.
- [ ] Final texture size matches the plan.
