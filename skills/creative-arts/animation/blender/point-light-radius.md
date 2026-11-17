---
id: creative-arts.animation.blender.point-light-radius
name: point-light-radius
category: creative-arts
field: animation
product: blender
tags: [blender, lights, point-light, point-light-radius, light-radius, soft-falloff, soft-shadows]
level: practitioner
status: verified
description: "Set Blender point light Radius for soft shadows and highlight size, and use Soft Falloff when light geometry intersects objects, in Cycles and EEVEE."
sources:
  - https://docs.blender.org/manual/en/latest/render/lights/light_object.html
  - https://projects.blender.org/blender/blender/src/branch/blender-v5.2-release/source/blender/makesrna/intern/rna_light.cc
licence: Apache-2.0
version: 5
updated: 2026-11-17
aliases: []
---
# point-light-radius

## What Radius does

- Point (and Spot) lights are spheres of size **Radius** (Object Data > Light). When Radius is larger than zero, light is emitted from a spherical surface of that radius.
- Larger lights have softer shadows and specular highlights. Point lights with a larger radius also appear dimmer because their power is distributed over a larger area.
- **Normalize** (on by default) keeps the total power the same when the size changes; turn it off and a bigger light emits more light. Measured (Cycles, Blender 4.5.14, 100 W point light 1 m above a plane, centre pixel): radius 0 gave 2.02 with Normalize on and 8.07 off; radius 0.5 gave 1.60 on and 5.04 off, so the larger light was dimmer at that point in both modes and Normalize off was about 3x brighter than on at radius 0.5.

## Soft Falloff

Checkbox on point and spot lights: applies falloff to avoid sharp edges when the light geometry intersects with other objects.

## Setup

```python
import bpy
l = bpy.data.lights.new("Bulb", type='POINT')
l.energy = 40               # watts
l.shadow_soft_size = 0.03   # Radius in the UI
l.use_soft_falloff = True
ob = bpy.data.objects.new("Bulb", l); bpy.context.collection.objects.link(ob)
```

Note the API name: `shadow_soft_size` is the Radius field (default 0; `use_soft_falloff` defaults to on, `energy` to 10 W).

## Gotchas

- A bulb mesh around a point light can block its light; turn off the mesh's Shadow ray visibility or use an emissive mesh instead.
- EEVEE shadow quality depends on shadow Rays/Steps and jitter, not just radius (`creative-arts.animation.blender.light-shadow-settings`).

## Verify

Render a cube on a plane at radius 0, 0.05 and 0.5: the penumbra width grows with the radius.

## Checked

2026-10-27. Documentation release: Blender 5.2 manual (blender-v5.2-release branch) and the 5.2 source UI scripts. Confirmed: Radius behaviour, Soft Falloff description and Normalize (Light Objects page); property names shadow_soft_size, energy, use_soft_falloff (rna_light.cc, properties_data_light.py); Shadow ray visibility toggle (object settings pages). Removed unsupported claims (4.0 gate, hot-spot behaviour, example radii, perceived brightness).

Run check, 2026-11-01, Blender 4.5.14 LTS headless: properties shadow_soft_size (UI source label Radius), use_soft_falloff, energy (Power), normalize defaults as above; point lights created with that API and rendered at radius 0 and 0.5 with Normalize on and off. Unrun (documentation only): bulb-mesh shadow blocking, EEVEE shadow quality, the penumbra Verify render.

Method: manual text confirmed from documentation; light behaviour run headless in Blender 4.5.14.
