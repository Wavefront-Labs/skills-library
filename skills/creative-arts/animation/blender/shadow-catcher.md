---
id: creative-arts.animation.blender.shadow-catcher
name: shadow-catcher
category: creative-arts
field: animation
product: blender
tags: [blender, render-passes, shadow-catcher, compositing, camera-tracking, film-transparent]
level: practitioner
status: docs-checked
description: "Composite CG onto footage with the Cycles shadow catcher: object setup, transparent film, the Shadow Catcher pass, and the comp graph that multiplies it into the plate."
sources:
  - https://docs.blender.org/manual/en/latest/render/cycles/object_settings/object_data.html
  - https://docs.blender.org/manual/en/latest/render/layers/passes.html
  - https://docs.blender.org/manual/en/latest/render/cycles/render_settings/film.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---
# shadow-catcher

Goal: CG objects cast shadows onto real footage.

## Setup (Cycles)

1. Model the ground (and any walls) that the CG touches, matching the plate (from camera tracking or by hand).
2. Ground object: Object Properties > Visibility > Mask > **Shadow Catcher**. Per the manual this makes the object only receive shadow rays, while it still interacts with other CG objects through indirect light.
3. Render Properties > Film > **Transparent** on.
4. View Layer Properties > Passes > Light > Other > **Shadow Catcher** on. The manual says that with the pass enabled all indirect light interactions are captured; with it disabled a simple approximation is used (also in viewport rendering).

## Comp

Simple: Alpha Over the render on the plate.

Better: the manual says the Shadow Catcher pass "can be multiplied with existing footage to (for example) have a rendered object cast a shadow on recorded ground":
```
plate x ShadowCatcher pass  -> plate with CG shadows
Alpha Over (render Image over that result)
```
Multiply the plate by the Shadow Catcher pass with a Mix Color node set to Multiply, then Alpha Over the Image pass.

## Tips

- Contact shadows need catcher geometry that closely matches the real surface, otherwise CG looks like it floats. This is a compositing practice.
- Light the CG to match the plate, for example with the plate's HDRI and a light aligned to the real shadow direction.

## Gotchas

- This skill covers the Cycles Shadow Catcher option and pass. EEVEE has its own Shadow pass (black where no direct light arrives, white where it does) which the manual says is mostly useful for compositing objects with shadow into footage.
- A Holdout shader makes a hole with zero alpha, which is the other tool for putting CG behind real objects.
- Indirect light from the catcher onto CG still happens, so check that the catcher's colour is sensible.

## Verify

Toggle the comp: with the catcher, the CG object has a shadow on the plate that matches the direction and softness of the real shadows in the footage.

## Checked

Date 2026-10-27. Blender manual 5.2 (blender-v5.2-release RST) and the Cycles add-on source (properties.py on main).
Confirmed: Mask > Shadow Catcher option and its behaviour, pass-enabled versus approximation note, Film > Transparent, Shadow Catcher pass location and use, EEVEE Shadow pass description, Holdout node description.
Removed as unconfirmed: the claim that shadows appear in the alpha as darkening, glossy-catcher reflections guidance, centimetre accuracy figure, and the statement that EEVEE has no shadow catcher in many versions.
Method: documentation only; no commands were run.
