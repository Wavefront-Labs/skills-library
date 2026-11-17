---
id: creative-arts.animation.blender.spot-light-shape-blend
name: spot-light-shape-blend
category: creative-arts
field: animation
product: blender
tags: [blender, lighting, spot-shape, spot-blend, spot-size, spot-light]
level: practitioner
status: verified
description: "Shape Blender spot lights: Angle cone, Blend softness, Show Cone, Radius, spot power meaning, and pattern and IES alternatives."
sources:
  - https://docs.blender.org/manual/en/latest/render/lights/light_object.html
  - https://projects.blender.org/blender/blender/src/branch/blender-v5.2-release/source/blender/makesrna/intern/rna_light.cc
  - https://docs.blender.org/manual/en/latest/render/eevee/light_settings.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---
# spot-light-shape-blend

Goal: controlled pools of light (stage spots, flashlights, practical downlights).

## Beam Shape panel
- **Angle** (`spot_size`): size of the outer cone, 1 to 180 degrees (default 45; out-of-range values clamp: 0 became 1 degree, 4 rad became 180). Smaller gives a narrow focused beam, larger a wider spread.
- **Blend** (`spot_blend`, default 0.15; 2.0 clamped to 1.0): 0.0 to 1.0, the inner cone as a proportion of the outer cone. Larger values blur the edge more and shrink the inner cone; 0.0 gives very sharp edges.
- **Show Cone**: draws a transparent cone in the viewport to see which objects it contains.
- **Radius**: emitter size; it softens shadows. Angle and Blend only control the cone aperture and edge softness, not the shadow softness.
- **Power**: the energy the light would emit over its entire area if it were not limited by the spot angle, in watts, so narrowing the cone does not make it brighter (test: a 1000 W Cycles spot 3 m above a plane gave the same centre pixel, 2.2504, at 30 and 90 degrees).

## Patterns
- Patterned lights: in Cycles, vary the light colour or intensity with Texture nodes in the light's node tree, or use an IES profile (`creative-arts.animation.blender.ies-lights`).

## Gotchas
- Spot power does not concentrate as the cone narrows.
- In EEVEE, Light > Influence > Volume Scatter multiplies the light's contribution to volumes.

## Verify
Show Cone in a top view lines up with the pool on the floor in Rendered view.

## Checked

2026-10-27. Documentation release: Blender 5.2 manual (blender-v5.2-release branch) and the 5.2 source UI scripts. Confirmed: Angle range, Blend meaning, Show Cone and the note that Blend/Size do not control shadow softness (Light Objects page); spot Power meaning and Angle 1-180 degree range (rna_light.cc); Volume Scatter influence (EEVEE light settings page). Removed unsupported claims (elliptical scaling, aiming gizmo, flashlight numbers, EEVEE cut-out pattern).

Run check, 2026-11-01, Blender 4.5.14 LTS headless: SpotLight properties spot_size, spot_blend, show_cone, shadow_soft_size (UI source label Radius), energy; ranges, defaults and clamping; the power test above. Unrun (documentation only): Show Cone drawing, texture-node patterns, IES, EEVEE Volume Scatter influence effect (the volume_factor property and its label exist).

Method: manual text confirmed from documentation; spot properties run headless in Blender 4.5.14.
