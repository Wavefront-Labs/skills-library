---
id: creative-arts.animation.blender.light-path-node
name: light-path-node
category: creative-arts
field: animation
product: blender
tags: [blender, shader, light-path-node, light-path, is-camera-ray, ray-depth]
level: practitioner
status: docs-checked
description: "Use Blender Light Path node outputs (is camera ray, shadow, diffuse, glossy, ray depth, length) for render tricks, faster glass and stylised looks."
sources:
  - https://docs.blender.org/manual/en/5.2/render/shader_nodes/input/light_path.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# light-path-node

## Outputs

Is Camera Ray, Is Shadow Ray, Is Diffuse Ray, Is Glossy Ray, Is Singular Ray, Is Reflection Ray, Is Transmission Ray, Is Volume Scatter Ray; Ray Length; Ray Depth, Diffuse Depth, Glossy Depth, Transparent Depth, Transmission Depth, Portal Depth. Is Camera, Shadow, Diffuse and Glossy and Ray Depth are not Cycles-only; the others are marked Cycles Only. The node is meant for non-physically-based tricks.

## Tricks (Cycles)

- **Camera-only colour**: Mix Fac = Is Camera Ray gives a different colour when seen directly than in bounces.
- **Glass that lights an interior cheaply**: Glass BSDF when viewed directly and Transparent BSDF when viewed indirectly (see glass-refraction-bsdf).
- **Transmission Depth**: switch from a transmissive to a diffuse shader past a certain depth to avoid black spots where rays hit the bounce limit.
- **Transparent Depth**: counts how many transparent surfaces a ray has passed through.

## EEVEE

EEVEE has no rays, so some outputs are approximated: Is Camera, Is Shadow, Is Diffuse and Is Glossy are supported; Is Singular, Is Reflection and Is Transmission are not (same as Is Glossy); Ray Length is the distance from the camera to the shading point; Ray Depth, Diffuse Depth and Glossy Depth only reflect the bounce when baking the light cache; Transparent Depth is not supported (0); Transmission Depth equals Glossy Depth. Is Glossy does not work with Screen Space Reflections or Refractions but does with reflection planes.

## Gotchas

- These are non-physical; mixing with realistic renders can break lighting consistency in compositing.
- Passing through a Transparent shader does not count as a normal bounce for Ray Depth.

## Verify

Render a floor with the Is Camera Ray colour switch: the floor looks one colour to the camera while bounce light carries the other.

## Checked

Date: 2026-10-27. Blender 5.2 manual (blender-v5.2-release branch, docs.blender.org manual en/5.2). Confirmed against input/light_path: output list including Portal Depth, Cycles-only markers, EEVEE support list, the Transmission Depth use case, and the noise-reduction page for the glass trick. Removed the fireflies-clamping and fake-absorption tricks and the Ray Visibility advice, which the manual does not state; corrected the EEVEE section (was only 'partial').

Method: documentation only; no commands were run.
