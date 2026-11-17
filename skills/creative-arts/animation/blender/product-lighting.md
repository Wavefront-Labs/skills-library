---
id: creative-arts.animation.blender.product-lighting
name: product-lighting
category: creative-arts
field: animation
product: blender
tags: [blender, lighting, product-lighting, softbox, studio-lighting, cyclorama]
level: practitioner
status: docs-checked
description: "Light products in Blender like a studio: cyclorama, large softbox area lights, strip lights, emissive cards with ray visibility off, Khronos PBR Neutral view."
sources:
  - https://docs.blender.org/manual/en/latest/render/lights/light_object.html
  - https://docs.blender.org/manual/en/latest/render/cycles/object_settings/object_data.html
  - https://docs.blender.org/manual/en/latest/render/color_management/displays_views.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# product-lighting

Studio set-up advice is practice; Blender facts are listed in Checked.

## Set

- **Cyclorama (infinity curve)**: a plane with the back edge extruded up and a large bevel, so there is no horizon line. Light grey diffuse material.
- World black or very dim neutral so the lights define the look.
- View Transform **Khronos PBR Neutral** is described in the manual as aimed at product photography: it tries to keep sRGB output colours faithful to the base colours under grey-scale lighting in well-exposed scenes.

## Lights

- **Key softbox**: Area light, Shape Rectangle, above or to the side. Area light Shape options are Square, Rectangle, Disk and Ellipse; **Spread** (Cycles) controls how widely it fans out.
- **Strip lights**: a narrow Rectangle area light at the sides or behind, to draw clean highlight lines along the edges of glossy products.
- **Top light**: large and soft for even reflections on top surfaces.
- **Reflection or fill cards**: white diffuse planes or emissive meshes. Object properties > Visibility > Ray Visibility lets you hide an emitting mesh from camera rays while it still lights and reflects; hiding by ray type is cheaper than a shader-node workaround.

## Controlling reflections

- Cycles lights are not directly visible in the render; use an emissive mesh card when you want a visible shape in the reflection.
- Texture nodes in a light's node tree (Shader Editor, Light context, Cycles) can vary the light across its surface, for graduated softboxes.
- Light linking can restrict which objects a light illuminates.

## Gotchas

- Glossy black products show mostly reflections, so the lighting is reflection design (practice).
- Prefer a few large sources to many small ones (practice).
- For compositing on a plate, a Shadow Catcher plane (Object properties > Visibility > Mask > Shadow Catcher, Cycles) receives only shadows.

## Verify

Rotate the product on a turntable: highlights stay clean lines without hot spots, and the background remains seamless.

## Checked

Checked 2026-10-27 against the Blender 5.2 manual (blender-v5.2-release): render/lights/light_object.rst (area Shape options), render/cycles/light_settings.rst (Spread, lights not directly visible, node textures), render/cycles/object_settings/object_data.rst (Ray Visibility, Shadow Catcher), color_management/displays_views.rst (Khronos PBR Neutral). Removed: stated dimensions and angles, the "visible to Glossy rays only" claim for strip lights, and the Light Path node reference. Method: documentation only; no commands were run.
