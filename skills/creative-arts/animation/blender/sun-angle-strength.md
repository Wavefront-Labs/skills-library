---
id: creative-arts.animation.blender.sun-angle-strength
name: sun-angle-strength
category: creative-arts
field: animation
product: blender
tags: [blender, lights, sun-light, sun-angle, sun-strength, sun-direction]
level: practitioner
status: verified
description: "Configure Blender Sun lights: strength in W/m2, angular diameter for shadow softness, and aiming direction via rotation or a Track To target."
sources:
  - https://docs.blender.org/manual/en/latest/render/lights/light_object.html
  - https://docs.blender.org/api/current/bpy.types.SunLight.html
  - https://projects.blender.org/blender/blender/src/branch/blender-v5.2-release/source/blender/makesrna/intern/rna_light.cc
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---
# sun-angle-strength

## Key facts

- A Sun is considered infinitely far away: only its **rotation** matters, its location does not affect the render.
- **Strength** is irradiance in W/m2, not watts. Manual values: clear sky 1000, cloudy sky 500, overcast sky 200, moonlight 0.001 W/m2. These look much brighter than expected, so compensate with Exposure (Render > Film, or Color Management).
- **Angle** is the angular diameter of the sun as seen from earth, range 0 to 180 degrees (default 0.526 degrees; out-of-range values clamp: -1 became 0, 4 rad became 180 degrees); larger values blur shadows.

## Aiming

- Rotate the Sun object like any other object; the direction is set by its rotation.
- The Sun position add-on can drive the rotation (see `creative-arts.animation.blender.sun-position-addon`).
- Match an HDRI by rotating the sun until its shadow direction matches the sun in the HDRI.

```python
import bpy, math
s = bpy.data.lights.new("Sun", 'SUN'); s.energy = 4.0; s.angle = math.radians(1.0)
```

## Gotchas

- EEVEE: Light > Shadow > Resolution Limit applies to sun lights; Absolute Resolution Limit and Custom Distance do not exist for Sun lights.
- Moving a Sun object does nothing, because its location does not matter (test: the same centre pixel, 0.7639, with the sun at the origin and at (30, 40, 77)). Strength scales linearly (3 gave 0.7639, 6 gave 1.5279).

## Verify

Rotate the sun 90 degrees over 100 frames and scrub: shadows sweep around objects and length follows elevation.

## Checked

2026-10-27. Documentation release: Blender 5.2 manual (blender-v5.2-release branch) and the 5.2 source UI scripts. Confirmed: Location irrelevance, Strength in W/m2, Angle as angular diameter and the typical sun strengths (Light Objects page); Angle 0-180 degree range (rna_light.cc); no Absolute Resolution Limit or Custom Distance for Sun in EEVEE (EEVEE light settings page). Removed unsupported claims (local -Z travel, exposure -10, default angle of 0.526 degrees, Track To settings, sky double lighting, shimmer).

Run check, 2026-11-01, Blender 4.5.14 LTS headless: SunLight energy label Strength, angle range 0 to pi and default, clamping, the code snippet's properties, Cycles renders as above; light panel source: Resolution Limit is shown for Sun while the absolute-resolution toggle and the Custom Distance panel are hidden for Sun lights (SunLight has no use_absolute_resolution). Unrun (documentation only): the manual's typical strengths table, Sun position add-on, HDRI matching.

Method: manual text confirmed from documentation; Sun behaviour run headless in Blender 4.5.14.
