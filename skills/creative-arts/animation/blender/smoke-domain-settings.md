---
id: creative-arts.animation.blender.smoke-domain-settings
name: smoke-domain-settings
category: creative-arts
field: animation
product: blender
tags: [blender, smoke, gas-sim, smoke-domain-settings, buoyancy, heat-density, mantaflow]
level: practitioner
status: docs-checked
description: "Set Mantaflow gas domain settings: buoyancy density and heat, gravity, border collisions, empty space and timing for smoke behaviour."
sources:
  - https://docs.blender.org/manual/en/latest/physics/fluid/type/domain/gas/index.html
  - https://docs.blender.org/manual/en/latest/physics/fluid/type/domain/settings.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# smoke-domain-settings

## Gas panel (Domain type Gas)

- **Buoyancy Density**: buoyant force based on gas density. Values above 0 make gas rise, values below 0 make it sink (heavy fog, dry ice flowing down).
- **Buoyancy Heat**: how much temperature affects the gas. It works together with each flow object's **Initial Temperature** (the temperature difference to the domain's ambient): with a positive value, positive temperatures rise and negative temperatures sink; a negative value reverses this. Gas from flows with different temperatures mixes toward an equilibrium.
- **Vorticity** (smoke-vorticity) and **Dissolve** (smoke-dissolve) shape curls and fading.

## Settings panel

- Resolution Divisions, Time Scale, CFL Number and Adaptive Time Steps work as for liquids (fluid-domain-resolution).
- **Border Collisions**: which domain sides deflect gas and which let it pass through and disappear (leave the top open to let smoke out).
- **Empty Space** (gas only): voxels with values under this are treated as empty; more empty space optimises rendering and, with OpenVDB caching, reduces cache size.
- **Delete in Obstacle**: removes gas that intersects an obstacle.
- Gravity follows the scene unless global gravity is disabled in the scene settings.

## Recipe ideas

- Campfire smoke: positive Buoyancy Density and Heat, a hot Initial Temperature on the flow, some Vorticity, Dissolve so the domain does not fill.
- Dry ice fog: negative Buoyancy Density, cold flow, Border Collisions on the floor side.

## Gotchas

- Keep the domain tight around the effect: large domains need higher resolutions and longer bakes.
- Buoyancy Heat has no effect unless flow objects have a non-zero Initial Temperature.

## Verify

The plume rises (or the fog sinks) in the direction set by the buoyancy signs; compare speed with reference footage at your frame rate.

## Checked

Checked 2026-10-27 against the Blender 5.2 manual (physics/fluid/type/domain/settings (Gas section); branch blender-v5.2-release) and the 5.2 source (rna_fluid.cc). Confirmed: Buoyancy Density and Buoyancy Heat semantics including sign behaviour and the Initial Temperature interaction, Border Collisions, Empty Space, Delete in Obstacle, gravity behaviour, and Domain Type.

Method: documentation only; no commands were run.
