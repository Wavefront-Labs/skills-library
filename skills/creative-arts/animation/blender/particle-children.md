---
id: creative-arts.animation.blender.particle-children
name: particle-children
category: creative-arts
field: animation
product: blender
tags: [blender, particles, particle-children, children-interpolated, child-particles, clump, kink]
level: practitioner
status: docs-checked
description: "Use Blender particle children (Simple and Interpolated): Display/Render Amount, Clumping, Roughness, Kink types and Parting for hair and fluffy effects."
sources:
  - https://docs.blender.org/manual/en/5.2/physics/particles/emitter/children.html
  - https://docs.blender.org/manual/en/5.2/physics/particles/emitter/render.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# particle-children

## Child Type (Particle System > Children)

Children are Hair or Emitter particles originating from individual parents; physics is calculated for the parents and the children follow. Number and look of children can change without recalculating physics.

- **None**, **Simple** (children emitted from the parent position), **Interpolated** (children placed between parents on the mesh faces, interpolating adjacent parents; some become virtual parents). Interpolated is especially useful for fur and even distribution.
- Parents are not rendered when children are on; enable Render > Extra > **Parents** to render them too.

## Common options

- **Display Amount** (viewport) and **Render Amount**, **Length**, **Threshold** (amount of particles left untouched by child path length), **Seed**.

## Clumping, Roughness, Kink

- **Clumping**: Use Clump Curve, **Clump** (1.0 children meet at the tip, -1.0 start together at the root), **Shape**, plus **Clump Noise** with Size.
- **Roughness**: Use Roughness Curve; *Uniform* (based on child location), *Endpoint* (rough end), *Random* (random vector, optional Threshold).
- **Kink Type**: Nothing, Curl, Radial, Wave, Braid, Spiral; with Amplitude, Clump, Flatness, Frequency, Shape (Spiral also has Radius and Resolution). Spirals may not show on hair pointing straight up along the spiral axis.

## Simple and Interpolated settings

- Simple: **Size**, **Random Size**, **Radius** (3D distribution around the parent), **Roundness** (1.0 sphere, 0.0 in-plane).
- Interpolated: **Virtual Parents**, **Long Hair** (children suited to long hair), **Parting** with Min/Max angles.
- Vertex Groups panel can control child Density, Length, Clump, Kink, Roughness and Twist.

## Gotchas

- Render Amount multiplied by the parent count can get very large: keep Display Amount low in the viewport.
- Interpolated children follow their parents, so edit the parents.

## Verify

Set a low Display Amount for speed; render with Render Amount to check full density and that children do not detach from the surface.

## Checked

Date: 2026-10-27. Documentation: Blender 5.2 manual (Particle Children, Render > Extra, Vertex Groups). Confirmed: child types, Display/Render Amount, Clump, Roughness, Kink types and options, Simple and Interpolated settings, Parents render option. Removed as unconfirmed: memory arithmetic example, "legacy particle hair replaced by node groups" statement, and the "Parting Factor" label (the manual lists Parting with Min/Max).
Method: documentation only; no commands were run.
