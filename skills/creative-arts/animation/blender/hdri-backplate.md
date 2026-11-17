---
id: creative-arts.animation.blender.hdri-backplate
name: hdri-backplate
category: creative-arts
field: animation
product: blender
tags: [blender, lighting, hdri, hdri-backplate, backplate, world-visibility, shadow-catcher]
level: practitioner
status: docs-checked
description: "Separate lighting from background in Blender Cycles: HDRI backplates via Is Camera Ray, World Ray Visibility, Film Transparent and the Shadow Catcher object setting."
sources:
  - https://docs.blender.org/manual/en/latest/render/cycles/world_settings.html
  - https://docs.blender.org/manual/en/latest/render/shader_nodes/input/light_path.html
  - https://docs.blender.org/manual/en/latest/render/cycles/object_settings/object_data.html
  - https://docs.blender.org/manual/en/latest/render/cycles/render_settings/film.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# hdri-backplate

## Patterns

1. **Different background than lighting** (World shader): a Mix node with the factor from Light Path **Is Camera Ray**; the first colour is the indirect (lighting) colour and the second the directly visible one. The manual suggests this for a high-resolution background image with a low-resolution image for the actual lighting. Adding **Is Glossy** rays as well makes the high-resolution image visible in reflections.
2. **World Ray Visibility** (World properties > Ray Visibility): controls which ray types can "see" the environment, so you can hide it from the camera while it still lights the scene.
3. **Render Properties > Film > Transparent**: renders the background transparent for compositing over another background. **Transparent Glass** renders transmissive surfaces as transparent, with a **Roughness Threshold** to keep rough glass opaque.

## Shadow catcher

Ground plane: Object properties > Visibility > Mask > **Shadow Catcher** (Cycles): the object only receives shadow rays and still interacts with CG via indirect light. With the Shadow Catcher pass enabled in the View Layer passes, all indirect light interactions are captured; with it disabled a simple approximation is used, which is also what viewport rendering uses.

## Recipe: object on a photo plate (practice)

Capture an HDRI at the same location for lighting, match the camera (focal length, height), add a shadow catcher ground, enable Film Transparent, and composite over the plate (Alpha Over in the Compositor or another app). Match grade and grain.

## Gotchas

- Perspective mismatch between CG and plate is the real giveaway (practice).
- With the Is Camera Ray trick, reflections show the HDRI lighting image unless you also add Is Glossy, as described above.

## Verify

Toggle the shadow catcher: the object should sit on the plate with a contact shadow; check alpha edges in the output.

## Checked

Checked 2026-10-27 against the Blender 5.2 manual (blender-v5.2-release): render/cycles/world_settings.rst (Ray Visibility panel, Is Camera Ray tricks), render/cycles/render_settings/film.rst (Transparent, Transparent Glass, Roughness Threshold), render/cycles/object_settings/object_data.rst (Shadow Catcher and pass note), render/shader_nodes/input/light_path.rst. Removed the "EEVEE 4.2+ Holdout" claim and the list of individual world visibility checkboxes (not enumerated in the manual page). Method: documentation only; no commands were run.
