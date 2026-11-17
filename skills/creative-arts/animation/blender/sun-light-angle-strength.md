---
id: creative-arts.animation.blender.sun-light-angle-strength
name: sun-light-angle-strength
category: creative-arts
field: animation
product: blender
tags: [blender, lighting, sun-angle, sun-strength, sun-direction, sun-light]
level: practitioner
status: docs-checked
description: "Configure Blender sun lights: Strength in W/m2, Angle as angular diameter, direction from rotation only, the manual's typical sun strengths, and matching Sky Texture or HDRI suns."
sources:
  - https://docs.blender.org/manual/en/latest/render/lights/light_object.html
  - https://docs.blender.org/manual/en/latest/render/shader_nodes/textures/sky.html
  - https://docs.blender.org/manual/en/latest/render/cycles/render_settings/film.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# sun-light-angle-strength

Goal: believable daylight from the sun light.

## Properties

- **Strength**: with Normalize enabled, sun power is specified in Watts per square metre (point, spot and area lights use Watts). The manual's typical values: clear sky 1000 W/m2, cloudy sky 500, overcast sky 200, moonlight 0.001.
- **Angle**: the size of the sun as its angular diameter seen from Earth.
- **Direction**: the sun light's location does not affect the render; change direction by rotating it (for example with a Track To constraint on an empty).

## Pairing

- **Sky Texture** (World): the node has Sun Direction, Sun Disc (Cycles only), Sun Size, Sun Intensity, Sun Elevation and Sun Rotation. Match the sun light's rotation to the sky's sun, and decide whether the sky's sun disc or the light provides the sun to avoid doubling it.
- **HDRI**: rotate the environment mapping and aim the sun light along the brightest region, or use EEVEE's world **Sun** threshold, which converts the excess world contribution into a sun light.

## Exposure

The manual says real-world values look much brighter or dimmer than expected because eyes adapt and a render engine does not; compensate with **Exposure** in Render Properties > Film (a different setting from the Color Management exposure).

## Verify

Shadow direction matches the sky or HDRI, and the sun's apparent size follows the Angle setting.

## Checked
2026-10-27, Blender 5.2 manual (blender-v5.2-release RST) render/lights/light_object (Sun Light: location ignored, Angle as angular diameter, Power of Lights table, W/m2 with Normalize, Film Exposure advice), render/shader_nodes/textures/sky (Sun Disc, Size, Intensity, Elevation, Rotation) and render/cycles/render_settings/film (Film Exposure distinct from Color Management Exposure). Removed unconfirmed artist ranges, real-sun angle, EEVEE shadow and exposure values.
Method: documentation only; no commands were run.
