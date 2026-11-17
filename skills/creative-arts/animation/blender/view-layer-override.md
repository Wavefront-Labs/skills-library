---
id: creative-arts.animation.blender.view-layer-override
name: view-layer-override
category: creative-arts
field: animation
product: blender
tags: [blender, view-layer, view-layer-override, material-override, samples-override, clay-render]
level: practitioner
status: docs-checked
description: "Use view layer overrides: material and world override for clay or isolated passes, per view layer sample counts and the Cycles Layer Samples modes, and layer toggles."
sources:
  - https://docs.blender.org/manual/en/latest/render/layers/override.html
  - https://docs.blender.org/manual/en/latest/render/layers/view_layer.html
  - https://docs.blender.org/manual/en/latest/render/cycles/render_settings/sampling.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---
# view-layer-override

Goal: render variants of one scene (clay, isolated background, utility passes) without copying the scene.

## Override panel (View Layer Properties > Override)

Overrides apply only when rendering that view layer and do not change the scene globally.
- **Material Override**: replaces all materials in the view layer with one material. Typical for clay renders and lighting passes; the manual suggests a neutral diffuse material.
- **World Override**: replaces the scene's world for this layer (different lighting, or a flat background for compositing).
- **Samples**: a different sample count than the scene.

Typical clay material: a grey Principled BSDF. Wireframe or utility looks need a material built for it (for example a Wireframe node, or an emission material showing a position or normal). Objects whose look depends on displacement or alpha cut-outs lose that look under a material override; exclude those collections on that layer or accept the difference.

## Samples override

Cycles: the override is controlled by Render Properties > Sampling > Advanced > **Layer Samples**: Use (per-layer sample counts override the scene), Bounded (overrides allowed as long as they do not exceed the scene sample count), Ignore. The default in the Cycles add-on source is Use. EEVEE: the Samples override is always used. Use it to render cheap utility layers at lower samples next to a high-sample beauty layer.

## Workflow

- Name layers by purpose: `beauty`, `clay`, `util`.
- **Use for Rendering** (View Layer panel) decides whether the active layer is rendered. **Render Single Layer** renders only the active layer (ignored when rendering from the command line).
- Each view layer renders separately, so total render time adds up.

## Gotchas

- Setting Layer Samples to Ignore silently ignores per-layer samples.
- A material override also replaces materials on emissive meshes, so emissive panels stop emitting.

## Verify

Render all layers once. The clay layer should show the override material everywhere except excluded collections, and utility layers should look noisier than the beauty layer at equal settings.

## Checked

Date 2026-10-27. Blender manual 5.2 (blender-v5.2-release RST) and the Cycles add-on source (properties.py on main).
Confirmed: Override panel with Material Override, World Override and Samples; Layer Samples values Use, Bounded, Ignore and their meanings; default is Use (the draft said Ignore); EEVEE always uses the Samples override; Use for Rendering and Render Single Layer.
Removed as unconfirmed: the specific clay material values, and the statement that the EEVEE per-layer samples behave differently beyond the manual's note.
Method: documentation only; no commands were run.
