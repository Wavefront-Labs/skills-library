---
id: creative-arts.animation.blender.fire-settings
name: fire-settings
category: creative-arts
field: animation
product: blender
tags: [blender, fire, smoke, fire-settings, flame-rate, fuel, ignition-temperature]
level: practitioner
status: docs-checked
description: "Tune Mantaflow fire: flow fuel, flame reaction speed, flame smoke, vorticity, flame temperature range and smoke colour from fire."
sources:
  - https://docs.blender.org/manual/en/latest/physics/fluid/type/flow.html
  - https://docs.blender.org/manual/en/latest/physics/fluid/type/domain/settings.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---

# fire-settings

## Flow side

- **Flow Type**: Fire or Fire + Smoke. **Fuel**: amount of fuel burned per second; larger values give larger flames.
- **Smoke Color** on the flow for Fire + Smoke (the domain also has a Smoke Color for smoke from burning fuel).
- **Initial Temperature**: difference between the emitted gas temperature and the domain's ambient temperature; its effect depends on the domain's Buoyancy Heat.

## Domain > Fire panel

- **Reaction Speed**: how fast fuel burns. Larger values give smaller flames (fuel burns before it travels far); smaller values give larger flames.
- **Flame Smoke**: amount of extra smoke created automatically for burnt fuel, best visible with Fire + Smoke flows.
- **Vorticity**: extra vorticity for flames in addition to the global Vorticity.
- **Temperature Maximum / Minimum**: maximum and minimum temperature of flames; larger values give faster rising flames.
- **Smoke Color**: colour of the smoke emitted from burning fuel.

## Recipes

- Torch: a small flow with Fuel, a moderate Reaction Speed and some Flame Smoke, plus Noise upres.
- Large bonfire: smaller Reaction Speed, more fire Vorticity and positive Buoyancy Heat in the domain.

## Gotchas

- Fire renders black or invisible: the shader must use the flame/temperature data (smoke-shader).
- Fire looks soft at low resolution: raise Resolution Divisions or use Noise upres.

## Verify

In Domain > Viewport Display, set Grid Display to show the flame field; the render should show the fire colours.

## Checked

Checked 2026-10-27 against the Blender 5.2 manual (physics/fluid/type/flow, physics/fluid/type/domain/settings (Fire) and gas/viewport_display; branch blender-v5.2-release) and the 5.2 source (rna_fluid.cc). Confirmed: Fuel, Smoke Color, Initial Temperature, Reaction Speed, Flame Smoke, Vorticity, Temperature Maximum/Minimum (both raise flames faster), domain Smoke Color, and Grid Display fields.

Method: documentation only; no commands were run.
