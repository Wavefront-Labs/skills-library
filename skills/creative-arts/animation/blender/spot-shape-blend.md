---
id: creative-arts.animation.blender.spot-shape-blend
name: spot-shape-blend
category: creative-arts
field: animation
product: blender
tags: [blender, lights, spot-light, spot-shape, spot-blend, spot-size, show-cone]
level: practitioner
status: docs-checked
description: "Shape Blender spot lights with Spot Size, Blend and Show Cone, square or stretched cones via object scale, and radius for softness."
sources:
  - https://docs.blender.org/manual/en/latest/render/lights/light_object.html
  - https://docs.blender.org/api/current/bpy.types.SpotLight.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# spot-shape-blend

## Settings (Light > Beam Shape)

- **Angle** (Python `spot_size`): size of the outer cone, from 1 to 180 degrees. Smaller gives a narrow focused beam, larger a wider area.
- **Blend** (`spot_blend`, 0.0 to 1.0): the inner cone as a proportion of the outer cone. 0.0 gives very sharp edges with no transition; larger values blur the edge and shrink the full-strength inner cone. Blend and Angle only control the cone's radial falloff, not shadow softness.
- **Show Cone** (`show_cone`): draws a transparent cone in the 3D viewport to see which objects are inside it.
- **Radius** (`shadow_soft_size`): larger than zero emits from a spherical surface; larger lights give softer shadows and specular highlights.
- **Soft Falloff**: avoids sharp edges where the light geometry intersects other objects.
- **Power**: in Watts.

## Aiming

Rotate the light like any object, or use a Track To constraint aimed at an empty.

```python
import bpy, math
sp = bpy.data.lights.new("Key", 'SPOT')
sp.spot_size = math.radians(35)
sp.spot_blend = 0.15
sp.show_cone = True
sp.energy = 800
```

## Gotchas

- Shadow softness comes from Radius and the renderer's shadow settings; the manual's example shows soft spot edges with a sharp object shadow.

## Verify

Show Cone on, look through the camera: the cone footprint matches the intended pool of light and the render matches.

## Checked
2026-10-27, Blender 5.2 manual (blender-v5.2-release RST) render/lights/light_object (Spot Light: Angle 1 to 180 degrees, Blend 0 to 1 and what it controls, Show Cone, Radius, Soft Falloff). Removed unconfirmed example angles, scale-based cones, aiming shortcut, energy and IES/volume gotchas.
Method: documentation only; no commands were run.
