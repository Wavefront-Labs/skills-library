---
id: creative-arts.animation.blender.cycles-caustics-settings
name: cycles-caustics-settings
category: creative-arts
field: animation
product: blender
tags: [blender, cycles, caustics-settings, filter-glossy, shadow-caustics, caustics]
level: practitioner
status: docs-checked
description: "Control caustics in Cycles: reflective/refractive caustic toggles, filter glossy, MNEE shadow caustics setup on caster, receiver and light, and its documented limits."
sources:
  - https://docs.blender.org/manual/en/latest/render/cycles/render_settings/light_paths.html
  - https://docs.blender.org/manual/en/latest/render/cycles/object_settings/object_data.html
  - https://docs.blender.org/manual/en/latest/render/cycles/light_settings.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# cycles-caustics-settings

Goal: get believable caustics (light focused through glass or water) or switch them off cleanly.

## Global toggles (Render Properties > Light Paths > Caustics)

- **Filter Glossy**: any value above 0.0 blurs glossy reflections after blurry bounces, trading accuracy for less noise. The manual suggests 1.0 as a starting value to tweak.
- **Reflective / Refractive** caustics: untick to disable that kind of caustic. Path-traced caustics can be too inefficient (too noisy) to be practical.

## MNEE shadow caustics

Manifold Next Event Estimation (MNEE) speeds up refractive caustics that fall in the shadows of objects. Three settings work together:
1. Light: Object Data > Settings > **Shadow Caustics** on (the World shader has the same option).
2. Caster (the glass or water): Object Properties > Shading > Caustics > **Cast Shadow Caustics**.
3. Receiver (floor, pool bottom): **Receive Shadow Caustics**.

Documented limitations:
- Only refractive caustics inside shadows are rendered; reflective caustics and caustics outside shadows are not.
- It is an approximation: brightness can be wrong, and rough or curved surfaces are not represented correctly.
- Only one BSDF is used when a material has several refractive BSDFs.
- Filter Glossy is ignored for MNEE refractive caustics.
- A ray may pass through up to 6 caster surfaces between receiver and light.
- Ambient Occlusion and Bevel nodes give invalid results on casters/receivers while the scene has an active caster, receiver and Shadow Caustics light.
- Casters need smooth normals. Volumes are ignored. Bump and normal maps are ignored.
- GPU rendering on Radeon RX 6000 series HIP devices on Windows is not supported.

## Faking

For stylised or fast work: render with the caustic toggles off and add the caustic look separately (a projected texture from a light, or in compositing).

## Gotchas

- Mark the refractive surface as the caster and the surface the light lands on as the receiver; a missing flag on either gives no MNEE caustic.
- Filter Glossy also softens genuine glossy-on-glossy reflections. Check chrome objects.

## Verify

Render the floor under the glass with MNEE on and off at the same samples and compare.

## Checked

Date: 2026-10-27. Documentation: Blender 5.2 manual (Cycles Light Paths, Object settings, Light settings). Confirmed: Caustics panel toggles and Filter Glossy behaviour, Shadow Caustics on light and world, Cast/Receive Shadow Caustics under Object Properties > Shading, and the MNEE limitation list. Removed unconfirmed: version gate, default Filter Glossy effect sizes, transparent-shadow trick, HDRI sun advice.
Method: documentation only; no commands were run.
